class ASTNode:
    def __init__(self):
        pass

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def __str__(self):
        return f"Program({self.statements})"

class VarDecl(ASTNode):
    def __init__(self, var_type, name, init_value=None):
        super().__init__()
        self.var_type = var_type
        self.name = name
        self.init_value = init_value

    def __str__(self):
        return f"VarDecl({self.var_type}, {self.name}, {self.init_value})"

class Assign(ASTNode):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f"Assign({self.name}, {self.value})"

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Num(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Num({self.value})"

class Var(ASTNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Var({self.name})"

class If(ASTNode):
    def __init__(self, condition, true_body, false_body=None):
        super().__init__()
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

    def __str__(self):
        return f"If({self.condition}, {self.true_body}, {self.false_body})"

class While(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition}, {self.body})"