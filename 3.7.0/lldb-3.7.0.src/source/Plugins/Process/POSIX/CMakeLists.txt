set(LLVM_NO_RTTI 1)

include_directories(.)
include_directories(../Utility)

add_lldb_library(lldbPluginProcessPOSIX
  CrashReason.cpp
  ProcessMessage.cpp
  ProcessPOSIXLog.cpp
  )
