"""
Test that we can backtrace correctly with 'sigtramp' functions on the stack
"""

import os, time
import unittest2
import lldb
from lldbtest import *
import lldbutil

class SigtrampUnwind(TestBase):
    mydir = TestBase.compute_mydir(__file__)

    # On different platforms the "_sigtramp" and "__kill" frames are likely to be different.
    # This test could probably be adapted to run on linux/*bsd easily enough.
    @skipUnlessDarwin
    @dsym_test
    def test_with_dsym (self):
        """Test that we can backtrace correctly with _sigtramp on the stack"""
        self.buildDsym()
        self.setTearDownCleanup()
        self.sigtramp_unwind_tests()

    @skipUnlessDarwin
    @dwarf_test
    def test_with_dwarf (self):
        """Test that we can backtrace correctly with _sigtramp on the stack"""
        self.buildDwarf()
        self.setTearDownCleanup()
        self.sigtramp_unwind_tests()

    def sigtramp_unwind_tests (self):
        exe = os.path.join(os.getcwd(), "a.out")
        target = self.dbg.CreateTarget(exe)
        self.assertTrue(target, VALID_TARGET)


        lldbutil.run_break_set_by_file_and_line (self, "main.c", line_number('main.c', '// Set breakpoint here'), num_expected_locations=1)

        process = target.LaunchSimple (None, None, self.get_process_working_directory())

        if not process:
            self.fail("SBTarget.Launch() failed")

        if process.GetState() != lldb.eStateStopped:
            self.fail("Process should be in the 'stopped' state, "
                      "instead the actual state is: '%s'" %
                      lldbutil.state_type_to_str(process.GetState()))

        self.expect("pro handle  -n false -p true -s false SIGUSR1", "Have lldb pass SIGUSR1 signals",
            substrs = ["SIGUSR1", "true", "false", "false"])

        lldbutil.run_break_set_by_symbol (self, "handler", num_expected_locations=1, module_name="a.out")

        self.runCmd("continue")

        thread = process.GetThreadAtIndex(0)

        found_handler = False
        found_sigtramp = False
        found_kill = False
        found_main = False

        for f in thread.frames:
            if f.GetFunctionName() == "handler":
                found_handler = True
            if f.GetFunctionName() == "_sigtramp":
                found_sigtramp = True
            if f.GetFunctionName() == "__kill":
                found_kill = True
            if f.GetFunctionName() == "main":
                found_main = True

        if self.TraceOn():
            print "Backtrace once we're stopped:"
            for f in thread.frames:
                print "  %d %s" % (f.GetFrameID(), f.GetFunctionName())

        if found_handler == False:
            self.fail("Unable to find handler() in backtrace.")

        if found_sigtramp == False:
            self.fail("Unable to find _sigtramp() in backtrace.")

        if found_kill == False:
            self.fail("Unable to find kill() in backtrace.")

        if found_main == False:
            self.fail("Unable to find main() in backtrace.")

if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()
