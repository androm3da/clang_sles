#!/bin/bash -e

build_base()
{
    RELEASE_VER=3.4.2
    BUILD=llvm_${RELEASE_VER}_build/
    LLVM=${PWD}/${RELEASE_VER}/llvm/
    INSTALL_DEST=llvm+clang-${RELEASE_VER}

    mkdir -p ./${BUILD}
    cd ./${BUILD}

    CC=gcc-4.7 CXX=g++-4.7 \
        ../cmake/bin/cmake ${LLVM} \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
        -DCMAKE_INSTALL_PREFIX=./${INSTALL_DEST}/ \
        -DLLVM_TARGETS_TO_BUILD="X86" \
        -DCMAKE_CXX_FLAGS="-O3" \
        -DCMAKE_C_FLAGS="-O3" \
        -DBUILD_SHARED_LIBS=OFF \

    make -j9 all
    make install

    cd -
}

build_clang()
{
    BASE_CLANG_LOC=${1}
    RELEASE_VER=3.7.0
    BUILD=llvm_${RELEASE_VER}_build/
    LLVM=${PWD}/${RELEASE_VER}/llvm/
    INSTALL_DEST=llvm+clang-${RELEASE_VER}

    # Defeat LLVM's build requirement for Python 2.7 (AFAIK only used 
    #   for lldb and perhaps LLVM/clang's lit test suite).
    sed -e 's/2.7/2.6/g' < ${LLVM}/CMakeLists.txt > ${LLVM}/CMakeLists.txt_
    mv ${LLVM}/CMakeLists.txt_ ${LLVM}/CMakeLists.txt

    mkdir -p ./${BUILD}
    cd ./${BUILD}

    CC=${BASE_CLANG_LOC}/bin/clang CXX=${BASE_CLANG_LOC}/bin/clang++ \
        ../cmake/bin/cmake ${LLVM} \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
        -DCMAKE_INSTALL_PREFIX=./${INSTALL_DEST}/ \
        -DLLVM_TARGETS_TO_BUILD="X86" \
        -DCMAKE_CXX_FLAGS="-O3" \
        -DCMAKE_C_FLAGS="-O3" \
        -DBUILD_SHARED_LIBS=OFF \

    make -j9 all
    make install

    cd -
}


build_base
build_clang ${PWD}/${BUILD}/${INSTALL_DEST}/
#build_clang ${PWD}/llvm_3.4.2_build/llvm+clang-3.4.2_optim_static/
