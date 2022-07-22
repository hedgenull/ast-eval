import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    debugfile = "parser.debug"

    tokens = Lexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", MUL, DIV, MOD),
        ("left", EQEQ, NTEQ, LT, GT, LTEQ, GTEQ),
    )

    # Grammar rules and actions

    @_("IDENT LPAREN expr RPAREN")
    def expr(self, p):
        if not isinstance(ENV[-1][p.IDENT], Function):
            abort(f"Not a function: {p.IDENT}")
        else:
            fn = ENV[-1][p.IDENT]
            return fn.call(p.expr.visit())

    @_("FN LPAREN IDENT RPAREN ARROW LPAREN expr RPAREN")
    def expr(self, p):
        return UserDefinedFunction(p.IDENT, expr=p.expr)

    @_("IDENT EQ expr")
    def expr(self, p):
        """Assignment expression"""
        return Assignment(p.IDENT, p.expr.visit())

    @_("LPAREN expr IF expr ELSE expr RPAREN")
    def expr(self, p):
        """If-else expression"""
        return IfNode(p.expr1, p.expr0, p.expr2)

    @_("expr PLUS expr")
    def expr(self, p):
        """Addition"""
        return BinOp("+", p.expr0, p.expr1)

    @_("expr MINUS expr")
    def expr(self, p):
        """Subtraction"""
        return BinOp("-", p.expr0, p.expr1)

    @_("expr MUL expr")
    def expr(self, p):
        """Multiplication"""
        return BinOp("*", p.expr0, p.expr1)

    @_("expr DIV expr")
    def expr(self, p):
        """Division"""
        return BinOp("/", p.expr0, p.expr1)

    @_("expr MOD expr")
    def expr(self, p):
        """Modulus"""
        return BinOp("%", p.expr0, p.expr1)

    @_("expr EQEQ expr")
    def expr(self, p):
        """Equal to"""
        return BinOp("==", p.expr0, p.expr1)

    @_("expr NTEQ expr")
    def expr(self, p):
        """Not equal to"""
        return BinOp("!=", p.expr0, p.expr1)

    @_("expr LT expr")
    def expr(self, p):
        """Less than"""
        return BinOp("<", p.expr0, p.expr1)

    @_("expr GT expr")
    def expr(self, p):
        """Greater than"""
        return BinOp(">", p.expr0, p.expr1)

    @_("expr LTEQ expr")
    def expr(self, p):
        """Less than or equal to"""
        return BinOp("<=", p.expr0, p.expr1)

    @_("expr GTEQ expr")
    def expr(self, p):
        """Greater than or equal to"""
        return BinOp(">=", p.expr0, p.expr1)

    @_("expr AND expr")
    def expr(self, p):
        """And"""
        return BinOp("&&", p.expr0, p.expr1)

    @_("expr OR expr")
    def expr(self, p):
        """Or"""
        return BinOp("||", p.expr0, p.expr1)

    @_("NUMBER")
    def expr(self, p):
        """Number"""
        return Number(p.NUMBER)

    @_("MINUS NUMBER")
    def expr(self, p):
        """Negative number"""
        n = Number(p.NUMBER)
        n.value = -n.value
        return n

    @_("STRING")
    def expr(self, p):
        """String"""
        return String(p.STRING)

    @_("IDENT")
    def expr(self, p):
        """Variable reference"""
        if val := ENV[-1].get(p.IDENT):
            return val
        else:
            abort(f"Undefined variable {p.IDENT}")

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        """Parenthesized expression"""
        return p.expr

    def error(self, tok):
        """Ruh roh"""
        print(f"Syntax error: Unexpected {tok.value}")
