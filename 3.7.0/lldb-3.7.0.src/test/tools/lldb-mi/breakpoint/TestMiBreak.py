"""
Test lldb-mi -break-xxx commands.
"""

import lldbmi_testcase
from lldbtest import *
import unittest2

class MiBreakTestCase(lldbmi_testcase.MiTestCaseBase):

    mydir = TestBase.compute_mydir(__file__)

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_break_insert_function_pending(self):
        """Test that 'lldb-mi --interpreter' works for pending function breakpoints."""

        self.spawnLldbMi(args = None)

        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        self.runCmd("-break-insert -f printf")
        #FIXME function name is unknown on Darwin, fullname should be ??, line is -1
        #self.expect("\^done,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"0xffffffffffffffff\",func=\"printf\",file=\"\?\?\",fullname=\"\?\?\",line=\"-1\",pending=\[\"printf\"\],times=\"0\",original-location=\"printf\"}")
        self.expect("\^done,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"0xffffffffffffffff\",func=\"\?\?\",file=\"\?\?\",fullname=\"\?\?/\?\?\",line=\"0\",pending=\[\"printf\"\],times=\"0\",original-location=\"printf\"}")
        #FIXME function name is unknown on Darwin, fullname should be ??, line -1
        #self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"0xffffffffffffffff\",func=\"printf\",file=\"\?\?\",fullname=\"\?\?\",line=\"-1\",pending=\[\"printf\"\],times=\"0\",original-location=\"printf\"}")
        self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"0xffffffffffffffff\",func=\"\?\?\",file=\"\?\?\",fullname=\"\?\?/\?\?\",line=\"0\",pending=\[\"printf\"\],times=\"0\",original-location=\"printf\"}")

        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\".+?\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",pending=\[\"printf\"\],times=\"0\",original-location=\"printf\"}")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_break_insert_function(self):
        """Test that 'lldb-mi --interpreter' works for function breakpoints."""

        self.spawnLldbMi(args = None)

        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"\d+\",pending=\[\"main\"\],times=\"0\",original-location=\"main\"}")
        self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"\d+\",pending=\[\"main\"\],times=\"0\",original-location=\"main\"}")

        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"\d+\",pending=\[\"main\"\],times=\"0\",original-location=\"main\"}")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        # Test that -break-insert can set non-pending BP
        self.runCmd("-break-insert printf")
        #FIXME function name is unknown on Darwin
        #self.expect("\^done,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"printf\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")
        self.expect("\^done,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\".+?\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")
        #FIXME function name is unknown on Darwin
        #self.expect("=breakpoint-modified,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"printf\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")
        self.expect("=breakpoint-modified,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\".+?\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")
        # FIXME function name is unknown on Darwin
        #self.expect("=breakpoint-modified,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"printf\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")
        self.expect("=breakpoint-modified,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\".+?\",file=\".+?\",fullname=\".+?\",line=\"(-1|\d+)\",times=\"0\",original-location=\"printf\"}")

        # Test that -break-insert fails if non-pending BP can't be resolved
        self.runCmd("-break-insert unknown_func")
        self.expect("\^error,msg=\"Command 'break-insert'. Breakpoint location 'unknown_func' not found\"")

        # Test that non-pending BP was set correctly
        self.runCmd("-exec-continue")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_break_insert_file_line_pending(self):
        """Test that 'lldb-mi --interpreter' works for pending file:line breakpoints."""

        self.spawnLldbMi(args = None)

        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Find the line number to break inside main() and set
        # pending BP
        line = line_number('main.cpp', '// BP_return')
        self.runCmd("-break-insert -f main.cpp:%d" % line)
        self.expect("\^done,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"%d\",pending=\[\"main.cpp:%d\"\],times=\"0\",original-location=\"main.cpp:%d\"}" % (line, line, line))
        self.expect("=breakpoint-modified,bkpt={number=\"1\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"%d\",pending=\[\"main.cpp:%d\"\],times=\"0\",original-location=\"main.cpp:%d\"}" % (line, line, line))

        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_break_insert_file_line(self):
        """Test that 'lldb-mi --interpreter' works for file:line breakpoints."""

        self.spawnLldbMi(args = None)

        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")

        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        # Test that -break-insert can set non-pending BP
        line = line_number('main.cpp', '// BP_return')
        self.runCmd("-break-insert main.cpp:%d" % line)
        self.expect("\^done,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"%d\",times=\"0\",original-location=\"main.cpp:%d\"}" % (line, line))
        self.expect("=breakpoint-modified,bkpt={number=\"2\",type=\"breakpoint\",disp=\"keep\",enabled=\"y\",addr=\"(?!0xffffffffffffffff)0x[0-9a-f]+\",func=\"main\",file=\"main\.cpp\",fullname=\".+?main\.cpp\",line=\"%d\",times=\"0\",original-location=\"main.cpp:%d\"}" % (line, line))

        # Test that -break-insert fails if non-pending BP can't be resolved
        self.runCmd("-break-insert unknown_file:1")
        self.expect("\^error,msg=\"Command 'break-insert'. Breakpoint location 'unknown_file:1' not found\"")

        # Test that non-pending BP was set correctly
        self.runCmd("-exec-continue")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    @unittest2.expectedFailure("-break-insert doesn't work for absolute path")
    def test_lldbmi_break_insert_file_line_absolute_path(self):
        """Test that 'lldb-mi --interpreter' works for file:line breakpoints."""

        self.spawnLldbMi(args = None)

        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")

        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        import os
        path = os.path.join(os.getcwd(), "main.cpp")
        line = line_number('main.cpp', '// BP_return')
        self.runCmd("-break-insert %s:%d" % (path, line))
        self.expect("\^done,bkpt={number=\"2\"")

        self.runCmd("-exec-continue")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @lldbmi_test
    @expectedFailureWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    @skipIfFreeBSD # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_break_insert_settings(self):
        """Test that 'lldb-mi --interpreter' can set breakpoints accoridng to global options."""

        self.spawnLldbMi(args = None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Set target.move-to-nearest-code=off and try to set BP #1 that shouldn't be hit
        self.runCmd("-interpreter-exec console \"settings set target.move-to-nearest-code off\"")
        self.expect("\^done")
        line = line_number('main.cpp', '// BP_before_main')
        self.runCmd("-break-insert -f main.cpp:%d" % line)
        self.expect("\^done,bkpt={number=\"1\"")

        # Test that non-pending BP will not be set on non-existing line if target.move-to-nearest-code=off
        # Note: this increases the BP number by 1 even though BP #2 is invalid.
        self.runCmd("-break-insert main.cpp:%d" % line)
        self.expect("\^error,msg=\"Command 'break-insert'. Breakpoint location 'main.cpp:%d' not found\"" % line)

        # Set target.move-to-nearest-code=on and target.skip-prologue=on and set BP #3
        self.runCmd("-interpreter-exec console \"settings set target.move-to-nearest-code on\"")
        self.runCmd("-interpreter-exec console \"settings set target.skip-prologue on\"")
        self.expect("\^done")
        self.runCmd("-break-insert main.cpp:%d" % line)
        self.expect("\^done,bkpt={number=\"3\"")

        # Set target.skip-prologue=off and set BP #4
        self.runCmd("-interpreter-exec console \"settings set target.skip-prologue off\"")
        self.expect("\^done")
        self.runCmd("-break-insert main.cpp:%d" % line)
        self.expect("\^done,bkpt={number=\"4\"")

        # Test that BP #4 is located before BP #3
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\",disp=\"del\",bkptno=\"4\"")

        # Test that BP #3 is hit
        self.runCmd("-exec-continue")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\",disp=\"del\",bkptno=\"3\"")

        # Test that BP #1 and #2 weren't set by running to program exit
        self.runCmd("-exec-continue")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"exited-normally\"")

if __name__ == '__main__':
    unittest2.main()
