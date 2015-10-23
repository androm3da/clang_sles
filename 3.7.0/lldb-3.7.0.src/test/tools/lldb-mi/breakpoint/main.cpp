//===-- main.cpp ------------------------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include <cstdio>

// BP_before_main

int
main(int argc, char const *argv[])
{
    printf("Print a formatted string so that GCC does not optimize this printf call: %s\n", argv[0]);
    return 0; // BP_return
}
