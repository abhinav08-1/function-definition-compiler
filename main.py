from lexer import tokenize
from parser import parse_source
from semantic import analyze,SemanticError
from ast_tools import print_ast
def main():
 print("FUNCTION DEFINITION COMPILER - FRONT END")
 print("Example: def add(a, b): return a + b;\n         add(2, 3);")
 print("Enter END on a separate line to finish.")
 lines=[]
 while True:
  try: line=input()
  except EOFError: break
  if line.strip()=="END": break
  lines.append(line)
 source="\n".join(lines)
 if not source.strip(): print("No program entered."); return
 try:
  tokens=tokenize(source)
  print("\n[1] LEXICAL ANALYSIS: SUCCESS")
  print(f"{'TYPE':<16} {'LEXEME':<18} {'LINE':<6} COLUMN")
  for k,v,l,c in tokens: print(f"{k:<16} {v!r:<18} {l:<6} {c}")
  program=parse_source(source); print("\n[2] SYNTAX ANALYSIS: SUCCESS")
  analyze(program); print("[3] SEMANTIC ANALYSIS: SUCCESS")
  print_ast(program); print("\nCOMPILER FRONT END: SUCCESS")
 except (SyntaxError,SemanticError) as e: print("\nCOMPILER FRONT END: FAILED\n"+str(e))
if __name__=="__main__": main()
