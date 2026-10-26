from parser import Program,FunctionDef,Call,Number,String,Name,BinaryOp
def label(n):
 if isinstance(n,Program): return "Program"
 if isinstance(n,FunctionDef): return f"FunctionDef: {n.name} (params: {', '.join(n.parameters) or 'none'})"
 if isinstance(n,Call): return "Call: "+n.name
 if isinstance(n,Number): return "Number: "+n.value
 if isinstance(n,String): return "String: "+n.value
 if isinstance(n,Name): return "Name: "+n.identifier
 if isinstance(n,BinaryOp): return "BinaryOp: "+n.operator
 return str(n)
def children(n):
 if isinstance(n,Program): return n.functions+n.calls
 if isinstance(n,FunctionDef): return [n.return_expr]
 if isinstance(n,Call): return n.arguments
 if isinstance(n,BinaryOp): return [n.left,n.right]
 return []
def lines(n,prefix="",last=True):
 out=[prefix+("└── " if last else "├── ")+label(n)]
 ch=children(n); cp=prefix+("    " if last else "│   ")
 for i,c in enumerate(ch): out.extend(lines(c,cp,i==len(ch)-1))
 return out
def print_ast(program): print("Abstract Syntax Tree (AST):\\n"+"\\n".join(lines(program)))
