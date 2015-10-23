; RUN: llc < %s -mtriple=x86_64-unknown-unknown -mattr=+avx | FileCheck %s

;;; Shift left
define <8 x i32> @vshift00(<8 x i32> %a) {
; CHECK-LABEL: vshift00:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpslld $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpslld $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = shl <8 x i32> %a, <i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32
2>
  ret <8 x i32> %s
}

define <16 x i16> @vshift01(<16 x i16> %a) {
; CHECK-LABEL: vshift01:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsllw $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsllw $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = shl <16 x i16> %a, <i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2>
  ret <16 x i16> %s
}

define <4 x i64> @vshift02(<4 x i64> %a) {
; CHECK-LABEL: vshift02:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsllq $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsllq $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = shl <4 x i64> %a, <i64 2, i64 2, i64 2, i64 2>
  ret <4 x i64> %s
}

;;; Logical Shift right
define <8 x i32> @vshift03(<8 x i32> %a) {
; CHECK-LABEL: vshift03:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsrld $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsrld $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = lshr <8 x i32> %a, <i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32
2>
  ret <8 x i32> %s
}

define <16 x i16> @vshift04(<16 x i16> %a) {
; CHECK-LABEL: vshift04:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsrlw $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsrlw $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = lshr <16 x i16> %a, <i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2>
  ret <16 x i16> %s
}

define <4 x i64> @vshift05(<4 x i64> %a) {
; CHECK-LABEL: vshift05:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsrlq $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsrlq $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = lshr <4 x i64> %a, <i64 2, i64 2, i64 2, i64 2>
  ret <4 x i64> %s
}

;;; Arithmetic Shift right
define <8 x i32> @vshift06(<8 x i32> %a) {
; CHECK-LABEL: vshift06:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsrad $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsrad $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = ashr <8 x i32> %a, <i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32 2, i32
2>
  ret <8 x i32> %s
}

define <16 x i16> @vshift07(<16 x i16> %a) {
; CHECK-LABEL: vshift07:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsraw $2, %xmm0, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsraw $2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %s = ashr <16 x i16> %a, <i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2, i16 2>
  ret <16 x i16> %s
}

define <32 x i8> @vshift09(<32 x i8> %a) {
; CHECK-LABEL: vshift09:
; CHECK:       # BB#0:
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm1
; CHECK-NEXT:    vpsrlw $2, %xmm1, %xmm1
; CHECK-NEXT:    vmovdqa {{.*#+}} xmm2 = [63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63]
; CHECK-NEXT:    vpand %xmm2, %xmm1, %xmm1
; CHECK-NEXT:    vmovdqa {{.*#+}} xmm3 = [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32]
; CHECK-NEXT:    vpxor %xmm3, %xmm1, %xmm1
; CHECK-NEXT:    vpsubb %xmm3, %xmm1, %xmm1
; CHECK-NEXT:    vpsrlw $2, %xmm0, %xmm0
; CHECK-NEXT:    vpand %xmm2, %xmm0, %xmm0
; CHECK-NEXT:    vpxor %xmm3, %xmm0, %xmm0
; CHECK-NEXT:    vpsubb %xmm3, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm1, %ymm0, %ymm0
; CHECK-NEXT:    retq
  %s = ashr <32 x i8> %a, <i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2>
  ret <32 x i8> %s
}

define <32 x i8> @vshift10(<32 x i8> %a) {
; CHECK-LABEL: vshift10:
; CHECK:       # BB#0:
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm1
; CHECK-NEXT:    vpxor %xmm2, %xmm2, %xmm2
; CHECK-NEXT:    vpcmpgtb %xmm1, %xmm2, %xmm1
; CHECK-NEXT:    vpcmpgtb %xmm0, %xmm2, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm1, %ymm0, %ymm0
; CHECK-NEXT:    retq
  %s = ashr <32 x i8> %a, <i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7, i8 7>
  ret <32 x i8> %s
}

define <32 x i8> @vshift11(<32 x i8> %a) {
; CHECK-LABEL: vshift11:
; CHECK:       # BB#0:
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm1
; CHECK-NEXT:    vpsrlw $2, %xmm1, %xmm1
; CHECK-NEXT:    vmovdqa {{.*#+}} xmm2 = [63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63]
; CHECK-NEXT:    vpand %xmm2, %xmm1, %xmm1
; CHECK-NEXT:    vpsrlw $2, %xmm0, %xmm0
; CHECK-NEXT:    vpand %xmm2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm1, %ymm0, %ymm0
; CHECK-NEXT:    retq
  %s = lshr <32 x i8> %a, <i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2>
  ret <32 x i8> %s
}

define <32 x i8> @vshift12(<32 x i8> %a) {
; CHECK-LABEL: vshift12:
; CHECK:       # BB#0:
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm1
; CHECK-NEXT:    vpsllw $2, %xmm1, %xmm1
; CHECK-NEXT:    vmovdqa {{.*#+}} xmm2 = [252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252]
; CHECK-NEXT:    vpand %xmm2, %xmm1, %xmm1
; CHECK-NEXT:    vpsllw $2, %xmm0, %xmm0
; CHECK-NEXT:    vpand %xmm2, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm1, %ymm0, %ymm0
; CHECK-NEXT:    retq
  %s = shl <32 x i8> %a, <i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2, i8 2>
  ret <32 x i8> %s
}

;;; Support variable shifts
define <8 x i32> @vshift08(<8 x i32> %a)  {
; CHECK-LABEL: vshift08:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpslld $23, %xmm0, %xmm1
; CHECK-NEXT:    vmovdqa {{.*#+}} xmm2 = [1065353216,1065353216,1065353216,1065353216]
; CHECK-NEXT:    vpaddd %xmm2, %xmm1, %xmm1
; CHECK-NEXT:    vcvttps2dq %xmm1, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpslld $23, %xmm0, %xmm0
; CHECK-NEXT:    vpaddd %xmm2, %xmm0, %xmm0
; CHECK-NEXT:    vcvttps2dq %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %bitop = shl <8 x i32> <i32 1, i32 1, i32 1, i32 1, i32 1, i32 1, i32 1, i32 1>, %a
  ret <8 x i32> %bitop
}

; PR15141
define <4 x i32> @vshift13(<4 x i32> %in) {
; CHECK-LABEL: vshift13:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpmulld {{.*}}(%rip), %xmm0, %xmm0
; CHECK-NEXT:    retq
  %T = shl <4 x i32> %in, <i32 0, i32 1, i32 2, i32 4>
  ret <4 x i32> %T
}

;;; Uses shifts for sign extension
define <16 x i16> @sext_v16i16(<16 x i16> %a)  {
; CHECK-LABEL: sext_v16i16:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpsllw $8, %xmm0, %xmm1
; CHECK-NEXT:    vpsraw $8, %xmm1, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpsllw $8, %xmm0, %xmm0
; CHECK-NEXT:    vpsraw $8, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %b = trunc <16 x i16> %a to <16 x i8>
  %c = sext <16 x i8> %b to <16 x i16>
  ret <16 x i16> %c
}

define <8 x i32> @sext_v8i32(<8 x i32> %a)  {
; CHECK-LABEL: sext_v8i32:
; CHECK:       # BB#0:
; CHECK-NEXT:    vpslld $16, %xmm0, %xmm1
; CHECK-NEXT:    vpsrad $16, %xmm1, %xmm1
; CHECK-NEXT:    vextractf128 $1, %ymm0, %xmm0
; CHECK-NEXT:    vpslld $16, %xmm0, %xmm0
; CHECK-NEXT:    vpsrad $16, %xmm0, %xmm0
; CHECK-NEXT:    vinsertf128 $1, %xmm0, %ymm1, %ymm0
; CHECK-NEXT:    retq
  %b = trunc <8 x i32> %a to <8 x i16>
  %c = sext <8 x i16> %b to <8 x i32>
  ret <8 x i32> %c
}
