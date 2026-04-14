from sympy import symbols, integrate, sympify

def solve_integral(expr):
    x = symbols('x')
    expression = sympify(expr)
    result = integrate(expression, x)
    return result