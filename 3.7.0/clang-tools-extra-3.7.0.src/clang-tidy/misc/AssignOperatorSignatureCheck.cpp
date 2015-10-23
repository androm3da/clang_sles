//===--- AssignOperatorSignatureCheck.cpp - clang-tidy ----------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "AssignOperatorSignatureCheck.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/ASTMatchers/ASTMatchers.h"

using namespace clang::ast_matchers;

namespace clang {
namespace tidy {
namespace misc {

void AssignOperatorSignatureCheck::registerMatchers(
    ast_matchers::MatchFinder *Finder) {
  const auto HasGoodReturnType = methodDecl(returns(lValueReferenceType(pointee(
      unless(isConstQualified()), hasDeclaration(equalsBoundNode("class"))))));

  const auto IsSelf = qualType(
      anyOf(hasDeclaration(equalsBoundNode("class")),
            referenceType(pointee(hasDeclaration(equalsBoundNode("class"))))));
  const auto IsSelfAssign =
      methodDecl(unless(anyOf(isDeleted(), isPrivate(), isImplicit())),
                 hasName("operator="), ofClass(recordDecl().bind("class")),
                 hasParameter(0, parmVarDecl(hasType(IsSelf)))).bind("method");

  Finder->addMatcher(
      methodDecl(IsSelfAssign, unless(HasGoodReturnType)).bind("ReturnType"),
      this);

  const auto BadSelf = referenceType(
      anyOf(lValueReferenceType(pointee(unless(isConstQualified()))),
            rValueReferenceType(pointee(isConstQualified()))));

  Finder->addMatcher(
      methodDecl(IsSelfAssign, hasParameter(0, parmVarDecl(hasType(BadSelf))))
          .bind("ArgumentType"),
      this);

  Finder->addMatcher(methodDecl(IsSelfAssign, isConst()).bind("Const"), this);
}


void AssignOperatorSignatureCheck::check(
    const MatchFinder::MatchResult &Result) {
  const auto* Method = Result.Nodes.getNodeAs<CXXMethodDecl>("method");
  std::string Name = Method->getParent()->getName();

  static const char *Messages[][2] = {
      {"ReturnType", "operator=() should return '%0&'"},
      {"ArgumentType", "operator=() should take '%0 const&', '%0&&' or '%0'"},
      {"Const", "operator=() should not be marked 'const'"},
  };

  for (const auto& Message : Messages) {
    if (Result.Nodes.getNodeAs<Decl>(Message[0]))
      diag(Method->getLocStart(), Message[1]) << Name;
  }
}

} // namespace misc
} // namespace tidy
} // namespace clang
