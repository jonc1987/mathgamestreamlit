import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_math_question(topic: str) -> dict:
    prompt = f"Generate a {topic} math question suitable for a quiz. Provide the question and the correct answer. Format the response as a Python dictionary with 'question' and 'answer' keys."

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        
        # Safely evaluate the string as a Python dictionary
        question_dict = eval(content)
        
        if not isinstance(question_dict, dict) or 'question' not in question_dict or 'answer' not in question_dict:
            raise ValueError("Invalid response format from OpenAI.")
        
        return question_dict
    except Exception as e:
        print(f"Error generating question: {e}")
        return {"question": "Error generating question. Please try again.", "answer": None}
