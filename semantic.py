from parser import Program, FunctionDef, Call, Name, Number, String, BinaryOp
class SemanticError(Exception): pass
def walk(expr):
 if isinstance(expr,(Number,String,Name)): yield expr
 elif isinstance(expr,BinaryOp):
  yield from walk(expr.left); yield from walk(expr.right)
 elif isinstance(expr,Call):
  yield expr
  for a in expr.arguments: yield from walk(a)
def analyze(program):
 errors=[]; funcs={}
 for fn in program.functions:
  if fn.name in funcs: errors.append(f"Function {fn.name!r} is defined more than once.")
  else: funcs[fn.name]=fn
  if len(set(fn.parameters))!=len(fn.parameters): errors.append(f"Function {fn.name!r} has duplicate parameter names.")
 def check_expr(expr,scope,where):
  for n in walk(expr):
   if isinstance(n,Name) and n.identifier not in scope: errors.append(f"Undefined variable {n.identifier!r} in {where}.")
   if isinstance(n,Call):
    if n.name not in funcs: errors.append(f"Call to undefined function {n.name!r} in {where}.")
    elif len(n.arguments)!=len(funcs[n.name].parameters): errors.append(f"Function {n.name!r} expects {len(funcs[n.name].parameters)} argument(s), got {len(n.arguments)} in {where}.")
 for fn in program.functions: check_expr(fn.return_expr,set(fn.parameters),f"function {fn.name!r}")
 for call in program.calls:
  if call.name not in funcs: errors.append(f"Call to undefined function {call.name!r} in program.")
  elif len(call.arguments)!=len(funcs[call.name].parameters): errors.append(f"Function {call.name!r} expects {len(funcs[call.name].parameters)} argument(s), got {len(call.arguments)} in program.")
  for a in call.arguments: check_expr(a,set(),"program call argument")
 if errors: raise SemanticError("\\n".join("- "+e for e in errors))
 return True
