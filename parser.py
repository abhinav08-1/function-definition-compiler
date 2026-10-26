from dataclasses import dataclass, field
from lexer import tokenize
@dataclass
class Number: value:str
@dataclass
class String: value:str
@dataclass
class Name: identifier:str
@dataclass
class BinaryOp: operator:str; left:object; right:object
@dataclass
class Call: name:str; arguments:list=field(default_factory=list)
@dataclass
class FunctionDef: name:str; parameters:list; return_expr:object
@dataclass
class Program: functions:list=field(default_factory=list); calls:list=field(default_factory=list)
class Parser:
 def __init__(self,tokens): self.tokens=tokens; self.position=0
 def current(self): return self.tokens[self.position] if self.position<len(self.tokens) else ("EOF","EOF",0,0)
 def peek(self,distance=1):
  i=self.position+distance
  return self.tokens[i] if i<len(self.tokens) else ("EOF","EOF",0,0)
 def advance(self):
  t=self.current()
  if self.position<len(self.tokens): self.position+=1
  return t
 def error(self,msg):
  k,v,l,c=self.current(); raise SyntaxError(f"Syntax error at line {l}, column {c}: {msg}; found {v!r} ({k})")
 def expect(self,v):
  if self.current()[1]==v: return self.advance()
  self.error(f"expected {v!r}")
 def identifier(self):
  if self.current()[0]=="IDENTIFIER": return self.advance()[1]
  self.error("expected an identifier")
 def parse_program(self):
  p=Program()
  while self.current()[0]!="EOF":
   if self.current()[1]=="def": p.functions.append(self.parse_function())
   elif self.current()[0]=="IDENTIFIER" and self.peek()[1]=="(":
    p.calls.append(self.parse_call()); self.expect(";")
   else: self.error("expected a function definition or function call")
  return p
 def parse_function(self):
  self.expect("def"); name=self.identifier(); self.expect("("); params=[]
  if self.current()[1]!=")":
   params.append(self.identifier())
   while self.current()[1]==",": self.advance(); params.append(self.identifier())
  self.expect(")"); self.expect(":"); self.expect("return"); expr=self.expression(); self.expect(";")
  return FunctionDef(name,params,expr)
 def parse_call(self):
  name=self.identifier(); self.expect("("); args=[]
  if self.current()[1]!=")":
   args.append(self.expression())
   while self.current()[1]==",": self.advance(); args.append(self.expression())
  self.expect(")"); return Call(name,args)
 def expression(self):
  n=self.term()
  while self.current()[1] in ("+","-"):
   op=self.advance()[1]; n=BinaryOp(op,n,self.term())
  return n
 def term(self):
  n=self.factor()
  while self.current()[1] in ("*","/"):
   op=self.advance()[1]; n=BinaryOp(op,n,self.factor())
  return n
 def factor(self):
  k,v,_,_=self.current()
  if k=="NUMBER": self.advance(); return Number(v)
  if k=="STRING": self.advance(); return String(v)
  if v=="(":
   self.advance(); n=self.expression(); self.expect(")"); return n
  if k=="IDENTIFIER":
   name=self.advance()[1]
   if self.current()[1]=="(":
    self.expect("("); args=[]
    if self.current()[1]!=")":
     args.append(self.expression())
     while self.current()[1]==",": self.advance(); args.append(self.expression())
    self.expect(")"); return Call(name,args)
   return Name(name)
  self.error("expected number, string, identifier, call, or parenthesized expression")
def parse_source(source_code): return Parser(tokenize(source_code)).parse_program()
