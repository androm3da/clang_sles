//===--- MiscTidyModule.cpp - clang-tidy ----------------------------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "../ClangTidy.h"
#include "../ClangTidyModule.h"
#include "../ClangTidyModuleRegistry.h"
#include "ArgumentCommentCheck.h"
#include "AssertSideEffectCheck.h"
#include "AssignOperatorSignatureCheck.h"
#include "BoolPointerImplicitConversionCheck.h"
#include "InaccurateEraseCheck.h"
#include "InefficientAlgorithmCheck.h"
#include "MacroParenthesesCheck.h"
#include "MacroRepeatedSideEffectsCheck.h"
#include "NoexceptMoveConstructorCheck.h"
#include "StaticAssertCheck.h"
#include "SwappedArgumentsCheck.h"
#include "UndelegatedConstructor.h"
#include "UniqueptrResetReleaseCheck.h"
#include "UnusedRAIICheck.h"
#include "UseOverrideCheck.h"

namespace clang {
namespace tidy {
namespace misc {

class MiscModule : public ClangTidyModule {
public:
  void addCheckFactories(ClangTidyCheckFactories &CheckFactories) override {
    CheckFactories.registerCheck<ArgumentCommentCheck>("misc-argument-comment");
    CheckFactories.registerCheck<AssertSideEffectCheck>(
        "misc-assert-side-effect");
    CheckFactories.registerCheck<AssignOperatorSignatureCheck>(
        "misc-assign-operator-signature");
    CheckFactories.registerCheck<BoolPointerImplicitConversionCheck>(
        "misc-bool-pointer-implicit-conversion");
    CheckFactories.registerCheck<InaccurateEraseCheck>(
        "misc-inaccurate-erase");
    CheckFactories.registerCheck<InefficientAlgorithmCheck>(
        "misc-inefficient-algorithm");
    CheckFactories.registerCheck<MacroParenthesesCheck>(
        "misc-macro-parentheses");
    CheckFactories.registerCheck<MacroRepeatedSideEffectsCheck>(
        "misc-macro-repeated-side-effects");
    CheckFactories.registerCheck<NoexceptMoveConstructorCheck>(
        "misc-noexcept-move-constructor");
    CheckFactories.registerCheck<StaticAssertCheck>(
        "misc-static-assert");
    CheckFactories.registerCheck<SwappedArgumentsCheck>(
        "misc-swapped-arguments");
    CheckFactories.registerCheck<UndelegatedConstructorCheck>(
        "misc-undelegated-constructor");
    CheckFactories.registerCheck<UniqueptrResetReleaseCheck>(
        "misc-uniqueptr-reset-release");
    CheckFactories.registerCheck<UnusedRAIICheck>("misc-unused-raii");
    CheckFactories.registerCheck<UseOverrideCheck>("misc-use-override");
  }
};

} // namespace misc

// Register the MiscTidyModule using this statically initialized variable.
static ClangTidyModuleRegistry::Add<misc::MiscModule>
X("misc-module", "Adds miscellaneous lint checks.");

// This anchor is used to force the linker to link in the generated object file
// and thus register the MiscModule.
volatile int MiscModuleAnchorSource = 0;

} // namespace tidy
} // namespace clang
