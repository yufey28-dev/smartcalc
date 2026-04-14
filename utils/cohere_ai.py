import cohere
import os

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def explain_integral(expr, result):
    try:
        prompt = f"""
Ты преподаватель математики.

Объясни пошагово решение интеграла:
{expr} = {result}

Объясняй просто и понятно.
"""

        response = co.chat(
            model='command-light',
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )

        return response.generations[0].text.strip()

    except Exception as e:
        return f"AI ошибка: {str(e)}"
