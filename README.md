
# Building
Building `clang` for an older platform like SuSE Linux Enterprise Server
11 (SLES11) is a little tricky because of its build dependencies.  This repo
is designed to gather those dependencies and automate the build.

    zypper install -y gcc47-c++ make
    ./build.sh

Also, now it's simpler still because I pushed the [binary release of 3.8.0](http://llvm.org/releases/3.8.0/clang+llvm-3.8.0-x86_64-sles11.3-linux-gnu.tar.xz) up to llvm.org.
