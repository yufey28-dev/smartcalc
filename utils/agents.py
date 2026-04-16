import sympy as sp

class ParserAgent:
    def process(self, expr, var='x'):
        v = sp.symbols(var)
        return sp.sympify(expr), v

class SolverAgent:
    def process(self, expr, var):
        return sp.integrate(expr, var)

class ExplanationAgent:
    def process(self, expr, var):
        return f"Интегрируем выражение {expr} по переменной {var}"

class MultiAgentSystem:
    def __init__(self):
        self.parser = ParserAgent()
        self.solver = SolverAgent()
        self.explainer = ExplanationAgent()

    def run(self, expr, var='x'):
        parsed, v = self.parser.process(expr, var)
        result = self.solver.process(parsed, v)
        explanation = self.explainer.process(expr, var)
        return result, explanation