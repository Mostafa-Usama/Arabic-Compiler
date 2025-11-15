import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def tokenize_arabic(input_str):
    token_spec = [
        ("VAR", r'متغير'),               # Variable declaration
        ("IF", r'اذا'),                # If keyword
        ("WHILE", r'طالما'),           # While keyword
        ("IDENT", r'[a-zA-Z_]\w*'),    # Identifiers (variable names)
        ("NUM", r'\d+'),               # Numbers
        ("PLUS", r'\+'),               # Addition
        ("MINUS", r'-'),               # Subtraction
        ("MULT", r'\*'),               # Multiplication
        ("DIV", r'/'),                 # Division
        ("EQ", r'=='),                 # Equals
        ("NEQ", r'!='),                # Not equals
        ("GTE", r'>='),                # Greater than or equal
        ("LTE", r'<='),                # Less than or equal
        ("GT", r'>'),                  # Greater than
        ("LT", r'<'),                  # Less than
        ("ASSIGN", r'='),              # Assignment operator
        ("LPAREN", r'\('),             # Left parenthesis
        ("RPAREN", r'\)'),             # Right parenthesis
        ("LBRACE", r'\{'),             # Left brace
        ("RBRACE", r'\}'),             # Right brace
        ("SEMICOLON", r';'),           # Semicolon
        ("WS", r'\s+'),                # Whitespace (ignored)
    ]
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    tokens = []
    for match in re.finditer(token_regex, input_str):
        kind = match.lastgroup
        value = match.group(kind)
        if kind != "WS":  # Skip whitespace
            tokens.append((kind, value))
    tokens.append(("EOF", None))  # End-of-file marker
    return tokens

class ArabicParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_stack = [{}]  # global scope

    def enter_scope(self):
        self.symbol_stack.append({})

    def exit_scope(self):
        self.symbol_stack.pop()

    def current_token(self):
        return self.tokens[self.pos]
    
    def declare_var(self, name):
        current_scope = self.symbol_stack[-1]
        if name in current_scope:
            raise SyntaxError(f"Semantic Error: variable '{name}' already declared in this scope")
        # Store metadata: initialized False at start
        current_scope[name] = {"initialized": False}
    
    def assign_var(self, name, value):
        # find in scopes from top to bottom
        for scope in reversed(self.symbol_stack): # عشان ندور من أصفر سكوب لأكبر سكوب (Global)
            if name in scope:
                scope[name]["initialized"] = True
                scope[name]["value"] = value
                return
        raise SyntaxError(f"Semantic Error: assignment to undeclared variable '{name}'")

    def lookup_var(self, name):
        for scope in reversed(self.symbol_stack):
            if name in scope:
                return scope[name]
        return None
    

    def match(self, expected_type):
        token = self.current_token()
        if token[0] == expected_type:
            self.pos += 1
            return token[1]
        else:
            raise SyntaxError(f"Expected {expected_type}, got {token[0]}")

    def parse(self):
        self.StatementList()
        self.match("EOF")
        print("Syntax is correct!")

    def StatementList(self):
        while self.current_token()[0] not in ["EOF", "RBRACE"]:
            self.Statement()

    def Statement(self):
        if self.current_token()[0] == "VAR":
            self.Declaration()
        elif self.current_token()[0] == "IDENT":
            self.Assignment()
        elif self.current_token()[0] == "IF":
            self.IfStmt()
        elif self.current_token()[0] == "WHILE":
            self.WhileStmt()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token()[0]}")

    def Declaration(self):
        self.match("VAR")

        var_name = self.match("IDENT")
        self.declare_var(var_name)
        self.match("ASSIGN")

        value = self.Expr()
        self.assign_var(var_name, value)
        self.match("SEMICOLON")

    def Assignment(self):
        var_name = self.match("IDENT")
        if not self.lookup_var(var_name): 
            raise SyntaxError(f"Semantic Error: variable '{var_name}' used before declaration")
        
        self.match("ASSIGN")
        value = self.Expr()
        self.assign_var(var_name, value)
        self.match("SEMICOLON")

    def IfStmt(self):
        self.match("IF")
        self.match("LPAREN")
        self.Condition()
        self.match("RPAREN")
        self.match("LBRACE")
        self.enter_scope()

        self.StatementList()

        self.exit_scope()
        self.match("RBRACE")
        
    def WhileStmt(self):
        self.match("WHILE")
        self.match("LPAREN")
        self.Condition()
        self.match("RPAREN")
        self.match("LBRACE")
        self.enter_scope()

        self.StatementList()

        self.exit_scope()
        self.match("RBRACE")

    def Condition(self):
        self.Expr()
        self.RelOp()
        self.Expr()

    def Expr(self):
        value = self.Term()
        while self.current_token()[0] in ["PLUS", "MINUS"]:
            op = (self.current_token()[0])
            self.match(op)
            right = self.Term()
            value = value + right if op == "PLUS" else value - right
        return value
    
    def Term(self):
        value = self.Factor()
        while self.current_token()[0] in ["MULT", "DIV"]:
            op = (self.current_token()[0])
            self.match(op)

            right =int(self.Factor())
            #print("Value:", value, "Right:", right, "Op:", op)
            value = value * right if op == "MULT" else value / right
        return value

    def Factor(self):
        if self.current_token()[0] == "LPAREN":
            self.match("LPAREN")
            value = self.Expr()
            self.match("RPAREN")
            return value
        elif self.current_token()[0] == "IDENT":
            var_name = self.match("IDENT")
            info = self.lookup_var(var_name)
            if not info:
                raise SyntaxError(f"Semantic Error: variable '{var_name}' used before declaration")
            if not info.get("initialized", False):
                raise SyntaxError(f"Semantic Error: variable '{var_name}' used before initialization")
            return info["value"]
        
        elif self.current_token()[0] == "NUM":
                value = self.match(self.current_token()[0])
                return int(value)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token()[0]}")

    def RelOp(self):
        if self.current_token()[0] in ["EQ", "NEQ", "GT", "GTE", "LT", "LTE"]:
            self.match(self.current_token()[0])
        else:
            raise SyntaxError(f"Expected a relational operator, got {self.current_token()[0]}")


program = """

متغير x =  3 + 5 * (3 - 1);
اذا (x > 10) {
     x = x * 2;
}
طالما (x < 20) {
}
متغير y = 5;
y = y + x;
"""
tokens = tokenize_arabic(program)
#print("Tokens:", tokens)

parser = ArabicParser(tokens)
try:
    parser.parse()
except SyntaxError as e:
    print(e)
print("Symbol Table:", parser.symbol_stack)