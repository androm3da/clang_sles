//===-- SymbolVendorMacOSX.cpp ----------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "SymbolVendorMacOSX.h"

#include <string.h>

#include "lldb/Core/Module.h"
#include "lldb/Core/ModuleSpec.h"
#include "lldb/Core/PluginManager.h"
#include "lldb/Core/Section.h"
#include "lldb/Core/StreamString.h"
#include "lldb/Core/Timer.h"
#include "lldb/Host/Host.h"
#include "lldb/Host/Symbols.h"
#include "lldb/Host/XML.h"
#include "lldb/Symbol/ObjectFile.h"

using namespace lldb;
using namespace lldb_private;

//----------------------------------------------------------------------
// SymbolVendorMacOSX constructor
//----------------------------------------------------------------------
SymbolVendorMacOSX::SymbolVendorMacOSX(const lldb::ModuleSP &module_sp) :
    SymbolVendor (module_sp)
{
}

//----------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------
SymbolVendorMacOSX::~SymbolVendorMacOSX()
{
}


static bool
UUIDsMatch(Module *module, ObjectFile *ofile, lldb_private::Stream *feedback_strm)
{
    if (module && ofile)
    {
        // Make sure the UUIDs match
        lldb_private::UUID dsym_uuid;

        if (!ofile->GetUUID(&dsym_uuid))
        {
            if (feedback_strm)
            {
                feedback_strm->PutCString("warning: failed to get the uuid for object file: '");
                ofile->GetFileSpec().Dump(feedback_strm);
                feedback_strm->PutCString("\n");
            }
            return false;
        }

        if (dsym_uuid == module->GetUUID())
            return true;

        // Emit some warning messages since the UUIDs do not match!
        if (feedback_strm)
        {
            feedback_strm->PutCString("warning: UUID mismatch detected between modules:\n    ");
            module->GetUUID().Dump(feedback_strm);
            feedback_strm->PutChar(' ');
            module->GetFileSpec().Dump(feedback_strm);
            feedback_strm->PutCString("\n    ");
            dsym_uuid.Dump(feedback_strm);
            feedback_strm->PutChar(' ');
            ofile->GetFileSpec().Dump(feedback_strm);
            feedback_strm->EOL();
        }
    }
    return false;
}

void
SymbolVendorMacOSX::Initialize()
{
    PluginManager::RegisterPlugin (GetPluginNameStatic(),
                                   GetPluginDescriptionStatic(),
                                   CreateInstance);
}

void
SymbolVendorMacOSX::Terminate()
{
    PluginManager::UnregisterPlugin (CreateInstance);
}


lldb_private::ConstString
SymbolVendorMacOSX::GetPluginNameStatic()
{
    static ConstString g_name("macosx");
    return g_name;
}

const char *
SymbolVendorMacOSX::GetPluginDescriptionStatic()
{
    return "Symbol vendor for MacOSX that looks for dSYM files that match executables.";
}



//----------------------------------------------------------------------
// CreateInstance
//
// Platforms can register a callback to use when creating symbol
// vendors to allow for complex debug information file setups, and to
// also allow for finding separate debug information files.
//----------------------------------------------------------------------
SymbolVendor*
SymbolVendorMacOSX::CreateInstance (const lldb::ModuleSP &module_sp, lldb_private::Stream *feedback_strm)
{
    if (!module_sp)
        return NULL;

    ObjectFile * obj_file = module_sp->GetObjectFile();
    if (!obj_file)
        return NULL;
    
    static ConstString obj_file_macho("mach-o");
    ConstString obj_name = obj_file->GetPluginName();
    if (obj_name != obj_file_macho)
        return NULL;

    Timer scoped_timer (__PRETTY_FUNCTION__,
                        "SymbolVendorMacOSX::CreateInstance (module = %s)",
                        module_sp->GetFileSpec().GetPath().c_str());
    SymbolVendorMacOSX* symbol_vendor = new SymbolVendorMacOSX(module_sp);
    if (symbol_vendor)
    {
        char path[PATH_MAX];
        path[0] = '\0';

        // Try and locate the dSYM file on Mac OS X
        Timer scoped_timer2 ("SymbolVendorMacOSX::CreateInstance () locate dSYM",
                             "SymbolVendorMacOSX::CreateInstance (module = %s) locate dSYM",
                             module_sp->GetFileSpec().GetPath().c_str());

        // First check to see if the module has a symbol file in mind already.
        // If it does, then we MUST use that.
        FileSpec dsym_fspec (module_sp->GetSymbolFileFileSpec());
            
        ObjectFileSP dsym_objfile_sp;
        if (!dsym_fspec)
        {
            // No symbol file was specified in the module, lets try and find
            // one ourselves.
            FileSpec file_spec = obj_file->GetFileSpec();
            if (!file_spec)
                file_spec = module_sp->GetFileSpec();
                
            ModuleSpec module_spec(file_spec, module_sp->GetArchitecture());
            module_spec.GetUUID() = module_sp->GetUUID();
            dsym_fspec = Symbols::LocateExecutableSymbolFile (module_spec);
            if (module_spec.GetSourceMappingList().GetSize())
                module_sp->GetSourceMappingList().Append (module_spec.GetSourceMappingList (), true);
        }
            
        if (dsym_fspec)
        {
            DataBufferSP dsym_file_data_sp;
            lldb::offset_t dsym_file_data_offset = 0;
            dsym_objfile_sp = ObjectFile::FindPlugin(module_sp, &dsym_fspec, 0, dsym_fspec.GetByteSize(), dsym_file_data_sp, dsym_file_data_offset);
            if (UUIDsMatch(module_sp.get(), dsym_objfile_sp.get(), feedback_strm))
            {
                // We need a XML parser if we hope to parse a plist...
                if (XMLDocument::XMLEnabled())
                {
                    char dsym_path[PATH_MAX];
                    if (module_sp->GetSourceMappingList().IsEmpty() && dsym_fspec.GetPath(dsym_path, sizeof(dsym_path)))
                    {
                        lldb_private::UUID dsym_uuid;
                        if (dsym_objfile_sp->GetUUID(&dsym_uuid))
                        {
                            std::string uuid_str = dsym_uuid.GetAsString ();
                            if (!uuid_str.empty())
                            {
                                char *resources = strstr (dsym_path, "/Contents/Resources/");
                                if (resources)
                                {
                                    char dsym_uuid_plist_path[PATH_MAX];
                                    resources[strlen("/Contents/Resources/")] = '\0';
                                    snprintf(dsym_uuid_plist_path, sizeof(dsym_uuid_plist_path), "%s%s.plist", dsym_path, uuid_str.c_str());
                                    FileSpec dsym_uuid_plist_spec(dsym_uuid_plist_path, false);
                                    if (dsym_uuid_plist_spec.Exists())
                                    {
                                        ApplePropertyList plist(dsym_uuid_plist_path);
                                        if (plist)
                                        {
                                            std::string DBGBuildSourcePath;
                                            std::string DBGSourcePath;
                                            
                                            plist.GetValueAsString("DBGBuildSourcePath", DBGBuildSourcePath);
                                            plist.GetValueAsString("DBGSourcePath", DBGSourcePath);
                                            if (!DBGBuildSourcePath.empty() && !DBGSourcePath.empty())
                                            {
                                                module_sp->GetSourceMappingList().Append (ConstString(DBGBuildSourcePath), ConstString(DBGSourcePath), true);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                symbol_vendor->AddSymbolFileRepresentation(dsym_objfile_sp);
                return symbol_vendor;
            }
        }

        // Just create our symbol vendor using the current objfile as this is either
        // an executable with no dSYM (that we could locate), an executable with
        // a dSYM that has a UUID that doesn't match.
        symbol_vendor->AddSymbolFileRepresentation(obj_file->shared_from_this());
    }
    return symbol_vendor;
}



//------------------------------------------------------------------
// PluginInterface protocol
//------------------------------------------------------------------
ConstString
SymbolVendorMacOSX::GetPluginName()
{
    return GetPluginNameStatic();
}

uint32_t
SymbolVendorMacOSX::GetPluginVersion()
{
    return 1;
}

