import sympy as sp

class ParserAgent:
    def process(self, expr):
        x = sp.symbols('x')
        return sp.sympify(expr), x


class SolverAgent:
    def process(self, expr, x):
        return sp.integrate(expr, x)


class ExplanationAgent:
    def process(self, expr):
        return f"Интегрируем выражение {expr} по переменной x"


class MultiAgentSystem:
    def __init__(self):
        self.parser = ParserAgent()
        self.solver = SolverAgent()
        self.explainer = ExplanationAgent()

    def run(self, expr):
        parsed, x = self.parser.process(expr)
        result = self.solver.process(parsed, x)
        explanation = self.explainer.process(expr)

        return result, explanation