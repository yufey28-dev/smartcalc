import google.generativeai as genai
import os
import random

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

CACHED_EXPLANATIONS = {
    "x": [
        "Интеграл от x равен x²/2 + C. Используем правило степени: увеличиваем показатель на 1 и делим на него.",
        "∫x dx = x²/2 + C. Степень x равна 1, значит прибавляем 1 → получаем 2, затем делим: x²/2.",
    ],
    "x**2": [
        "∫x² dx = x³/3 + C. Правило степени: показатель 2 → становится 3, делим на 3.",
    ],
    "x**3": [
        "∫x³ dx = x⁴/4 + C. Увеличиваем степень 3 до 4, делим на 4.",
    ],
    "x**4": [
        "∫x⁴ dx = x⁵/5 + C. Правило степени: 4+1=5, делим на 5.",
    ],
    "sin(x)": [
        "∫sin(x) dx = -cos(x) + C. Интеграл синуса — минус косинус, это базовая формула.",
        "Интеграл от sin(x) равен -cos(x) + C. Проверить можно взяв производную: (-cos(x))' = sin(x). ✓",
    ],
    "cos(x)": [
        "∫cos(x) dx = sin(x) + C. Интеграл косинуса — синус.",
    ],
    "exp(x)": [
        "∫eˣ dx = eˣ + C. Экспонента — единственная функция, которая не меняется при интегрировании.",
    ],
    "1/x": [
        "∫(1/x) dx = ln|x| + C. Исключение из правила степени — результат натуральный логарифм.",
    ],
    "1": [
        "∫1 dx = x + C. Интеграл от константы 1 — просто x.",
    ],
    "2*x": [
        "∫2x dx = x² + C. Константа 2 выносится за знак интеграла.",
    ],
    "tan(x)": [
        "∫tan(x) dx = -ln|cos(x)| + C.",
    ],
}

def get_cached_explanation(expr, result):
    key = expr.strip().replace(" ", "")
    if key in CACHED_EXPLANATIONS:
        return random.choice(CACHED_EXPLANATIONS[key])
    return None

def explain_integral(expr, result):
    try:
        cached = get_cached_explanation(expr, result)

        if cached:
            prompt = f"""Перефразируй это математическое объяснение, сохранив все формулы и суть.
Только перефразируй, не добавляй ничего лишнего:

{cached}"""
        else:
            prompt = f"""Ты преподаватель математики.
Объясни интеграл через обычные ответы в лимите 100 слов:
{expr} = {result}
Объясняй просто и понятно на русском языке."""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        cached = get_cached_explanation(expr, result)
        if cached:
            return cached
        return f"AI ошибка: {str(e)}"