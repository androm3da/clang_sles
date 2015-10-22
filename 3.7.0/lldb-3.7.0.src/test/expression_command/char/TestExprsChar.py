import unittest2
import lldb
import lldbutil
from lldbtest import *

class ExprCharTestCase(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    def setUp(self):
        # Call super's setUp().
        TestBase.setUp(self)

        self.main_source = "main.cpp"
        self.main_source_spec = lldb.SBFileSpec (self.main_source)
        self.exe = os.path.join(os.getcwd(), "a.out")

    def do_test(self, dictionary=None):
        """These basic expression commands should work as expected."""
        self.buildDefault(dictionary = dictionary)

        target = self.dbg.CreateTarget(self.exe)
        self.assertTrue(target)

        breakpoint = target.BreakpointCreateBySourceRegex('// Break here', self.main_source_spec)
        self.assertTrue(breakpoint)

        # Launch the process, and do not stop at the entry point.
        process = target.LaunchSimple(None, None, self.get_process_working_directory())
        self.assertTrue(process)

        threads = lldbutil.get_threads_stopped_at_breakpoint(process, breakpoint)
        self.assertEqual(len(threads), 1)

        frame = threads[0].GetFrameAtIndex(0)

        value = frame.EvaluateExpression("foo(c)")
        self.assertTrue(value.IsValid())
        self.assertTrue(value.GetError().Success())
        self.assertEqual(value.GetValueAsSigned(0), 1)

        value = frame.EvaluateExpression("foo(sc)")
        self.assertTrue(value.IsValid())
        self.assertTrue(value.GetError().Success())
        self.assertEqual(value.GetValueAsSigned(0), 2)

        value = frame.EvaluateExpression("foo(uc)")
        self.assertTrue(value.IsValid())
        self.assertTrue(value.GetError().Success())
        self.assertEqual(value.GetValueAsSigned(0), 3)

    def test_default_char(self):
        self.do_test()

    @expectedFailureArch("arm", "llvm.org/pr23069")
    @expectedFailureArch("aarch64", "llvm.org/pr23069")
    def test_signed_char(self):
        self.do_test(dictionary={'CFLAGS_EXTRAS': '-fsigned-char'})

    @expectedFailurei386("llvm.org/pr23069")
    @expectedFailurex86_64("llvm.org/pr23069")
    def test_unsigned_char(self):
        self.do_test(dictionary={'CFLAGS_EXTRAS': '-funsigned-char'})

if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()
