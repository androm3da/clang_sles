"""
Test lldb data formatter subsystem.
"""

import os, time
import unittest2
import lldb
from lldbtest import *
import lldbutil

class LibcxxMultiSetDataFormatterTestCase(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    @skipUnlessDarwin
    @dsym_test
    def test_with_dsym_and_run_command(self):
        """Test data formatter commands."""
        self.buildDsym()
        self.data_formatter_commands()

    @skipIfGcc
    @skipIfWindows # libc++ not ported to Windows yet
    @dwarf_test
    def test_with_dwarf_and_run_command(self):
        """Test data formatter commands."""
        self.buildDwarf()
        self.data_formatter_commands()

    def setUp(self):
        # Call super's setUp().
        TestBase.setUp(self)

    def data_formatter_commands(self):
        """Test that that file and class static variables display correctly."""
        self.runCmd("file a.out", CURRENT_EXECUTABLE_SET)

        bkpt = self.target().FindBreakpointByID(lldbutil.run_break_set_by_source_regexp (self, "Set break point at this line."))

        self.runCmd("run", RUN_SUCCEEDED)

        # The stop reason of the thread should be breakpoint.
        self.expect("thread list", STOPPED_DUE_TO_BREAKPOINT,
            substrs = ['stopped',
                       'stop reason = breakpoint'])

        # This is the function to remove the custom formats in order to have a
        # clean slate for the next test case.
        def cleanup():
            self.runCmd('type format clear', check=False)
            self.runCmd('type summary clear', check=False)
            self.runCmd('type filter clear', check=False)
            self.runCmd('type synth clear', check=False)
            self.runCmd("settings set target.max-children-count 256", check=False)

        # Execute the cleanup function during test case tear down.
        self.addTearDownHook(cleanup)

        self.expect('image list', substrs = self.getLibcPlusPlusLibs())

        self.expect("frame variable ii",substrs = ["size=0","{}"])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ii",substrs = ["size=6","[0] = 0","[1] = 1", "[2] = 2", "[3] = 3", "[4] = 4", "[5] = 5"])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ii",substrs = ["size=7","[2] = 2", "[3] = 3", "[6] = 6"])
        self.expect("p ii",substrs = ["size=7","[2] = 2", "[3] = 3", "[6] = 6"])
        self.expect("frame variable ii[2]",substrs = [" = 2"])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ii",substrs = ["size=0","{}"])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ii",substrs = ["size=0","{}"])
        self.expect("frame variable ss",substrs = ["size=0","{}"])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ss",substrs = ["size=2",'[0] = "a"','[1] = "a very long string is right here"'])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ss",substrs = ["size=4",'[2] = "b"','[3] = "c"','[0] = "a"','[1] = "a very long string is right here"'])
        self.expect("p ss",substrs = ["size=4",'[2] = "b"','[3] = "c"','[0] = "a"','[1] = "a very long string is right here"'])
        self.expect("frame variable ss[2]",substrs = [' = "b"'])
        lldbutil.continue_to_breakpoint(self.process(), bkpt)
        self.expect("frame variable ss",substrs = ["size=3",'[0] = "a"','[1] = "a very long string is right here"','[2] = "c"'])

if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()
