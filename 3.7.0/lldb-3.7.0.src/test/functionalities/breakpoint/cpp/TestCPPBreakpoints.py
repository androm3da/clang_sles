"""
Test lldb breakpoint ids.
"""

import os, time
import unittest2
import lldb
from lldbtest import *
import lldbutil

class TestCPPBreakpoints(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    @skipUnlessDarwin
    @dsym_test
    def test_with_dsym (self):
        self.buildDsym ()
        self.breakpoint_id_tests ()

    @dwarf_test
    def test_with_dwarf (self):
        self.buildDwarf ()
        self.breakpoint_id_tests ()

    def verify_breakpoint_locations(self, target, bp_dict):
        
        name = bp_dict['name']
        names = bp_dict['loc_names']
        bp = target.BreakpointCreateByName (name)
        self.assertTrue (bp.GetNumLocations() == len(names), "Make sure we find the right number of breakpoint locations")
        
        bp_loc_names = list()
        for bp_loc in bp:
            bp_loc_names.append(bp_loc.GetAddress().GetFunction().GetName())
            
        for name in names:
            found = name in bp_loc_names
            if not found:
                print "Didn't find '%s' in: %s" % (name, bp_loc_names)
            self.assertTrue (found, "Make sure we find all required locations")
        
    def breakpoint_id_tests (self):
        
        # Create a target by the debugger.
        exe = os.path.join(os.getcwd(), "a.out")
        target = self.dbg.CreateTarget(exe)
        self.assertTrue(target, VALID_TARGET)
        bp_dicts = [
            { 'name' : 'func1', 'loc_names' : [ 'a::c::func1()', 'b::c::func1()'] },
            { 'name' : 'func2', 'loc_names' : [ 'a::c::func2()', 'c::d::func2()'] },
            { 'name' : 'func3', 'loc_names' : [ 'a::c::func3()', 'b::c::func3()', 'c::d::func3()'] },
            { 'name' : 'c::func1', 'loc_names' : [ 'a::c::func1()', 'b::c::func1()'] },
            { 'name' : 'c::func2', 'loc_names' : [ 'a::c::func2()'] },
            { 'name' : 'c::func3', 'loc_names' : [ 'a::c::func3()', 'b::c::func3()'] },
            { 'name' : 'a::c::func1', 'loc_names' : [ 'a::c::func1()'] },
            { 'name' : 'b::c::func1', 'loc_names' : [ 'b::c::func1()'] },
            { 'name' : 'c::d::func2', 'loc_names' : [ 'c::d::func2()'] },
            { 'name' : 'a::c::func1()', 'loc_names' : [ 'a::c::func1()'] },
            { 'name' : 'b::c::func1()', 'loc_names' : [ 'b::c::func1()'] },
            { 'name' : 'c::d::func2()', 'loc_names' : [ 'c::d::func2()'] },
        ]
        
        for bp_dict in bp_dicts:
            self.verify_breakpoint_locations(target, bp_dict)


if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()

