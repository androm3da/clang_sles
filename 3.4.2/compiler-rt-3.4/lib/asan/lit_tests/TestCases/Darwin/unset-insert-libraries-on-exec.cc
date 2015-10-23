// Make sure ASan removes the runtime library from DYLD_INSERT_LIBRARIES before
// executing other programs.

// RUN: %clangxx_asan %s -o %t
// RUN: %clangxx %p/../Helpers/echo-env.cc -o %T/echo-env
// RUN: %clangxx %p/../SharedLibs/darwin-dummy-shared-lib-so.cc \
// RUN:     -dynamiclib -o %t-darwin-dummy-shared-lib-so.dylib

// Make sure DYLD_INSERT_LIBRARIES doesn't contain the runtime library before
// execl().

// RUN: %t %T/echo-env >/dev/null 2>&1
// RUN: DYLD_INSERT_LIBRARIES=%t-darwin-dummy-shared-lib-so.dylib \
// RUN:     %t %T/echo-env 2>&1 | FileCheck %s || exit 1
#include <unistd.h>
int main(int argc, char *argv[]) {
  execl(argv[1], argv[1], "DYLD_INSERT_LIBRARIES", NULL);
  // CHECK:  {{DYLD_INSERT_LIBRARIES = .*darwin-dummy-shared-lib-so.dylib.*}}
  return 0;
}
