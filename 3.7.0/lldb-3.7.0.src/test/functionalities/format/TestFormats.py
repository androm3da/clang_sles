"""
Test the command history mechanism
"""

import os
import unittest2
import lldb
from lldbtest import *

class TestFormats(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    @expectedFailureFreeBSD("llvm.org/pr22784: pexpect failing on the FreeBSD buildbot")
    @expectedFailureHostWindows("llvm.org/pr22274: need a pexpect replacement for windows")
    def test_formats(self):
        """Test format string functionality."""
        self.buildDwarf ()
        import pexpect
        prompt = "(lldb) "
        child = pexpect.spawn('%s %s -x -o "b main" -o r a.out' % (lldbtest_config.lldbExec, self.lldbOption))
        # Turn on logging for what the child sends back.
        if self.TraceOn():
            child.logfile_read = sys.stdout
        # So that the spawned lldb session gets shutdown durng teardown.
        self.child = child

        # Substitute 'Help!' for 'help' using the 'commands regex' mechanism.
        child.expect_exact(prompt + 'target create "a.out"') 
        child.expect_exact(prompt + 'b main') 
        child.expect_exact(prompt + 'r') 
        child.expect_exact(prompt)
        child.sendline()
        # child.expect_exact(prompt + "target create") 
        #     
        # child.sendline("command regex 'Help__'")
        # child.expect_exact(regex_prompt)
        # child.sendline('s/^$/help/')
        # child.expect_exact(regex_prompt1)
        # child.sendline('')
        # child.expect_exact(prompt)
        # # Help!
        # child.sendline('Help__')
        # # If we see the familiar 'help' output, the test is done.
        # child.expect('Debugger commands:')
        # # Try and incorrectly remove "Help__" using "command unalias" and verify we fail
        # child.sendline('command unalias Help__')
        # child.expect_exact("error: 'Help__' is not an alias, it is a debugger command which can be removed using the 'command delete' command")
        # child.expect_exact(prompt)
        # 
        # # Delete the regex command using "command delete"
        # child.sendline('command delete Help__')
        # child.expect_exact(prompt)
        # # Verify the command was removed
        # child.sendline('Help__')
        # child.expect_exact("error: 'Help__' is not a valid command")
        # child.expect_exact(prompt)

if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()
