import os
from replit.ai.modelfarm import ChatExample, ChatMessage, ChatModel, ChatSession

def generate_math_question(topic: str, question_request: str = "") -> dict:
    return generate_math_question_modelfarm(topic, question_request)

def generate_math_question_modelfarm(topic: str, question_request: str = "") -> dict:
    model = ChatModel("chat-bison")
    
    context = f"You are a math teacher generating {topic} questions for a quiz. The topics include Addition, Subtraction, Multiplication, Division, Algebra, Geometry, Greatest Common Factor, Least Common Multiple, Fractions, Decimals, Percentages, Exponents, Square Roots, and Order of Operations. Provide a question and its answer in a dictionary format with 'question' and 'answer' keys. It is crucial that the generated question strictly adheres to the specified topic, regardless of the difficulty level or any additional requests."
    
    if question_request:
        user_message = f"Generate a {topic} math question about {question_request}. The question MUST be about {topic}, no exceptions."
    else:
        user_message = f"Generate a {topic} math question. The question MUST be about {topic}, no exceptions."
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = model.chat([
                ChatSession(
                    context=context,
                    examples=[
                        ChatExample(
                            input=ChatMessage(content="Generate an addition question"),
                            output=ChatMessage(content="{'question': 'What is 15 + 27?', 'answer': '42'}")
                        ),
                        ChatExample(
                            input=ChatMessage(content="Generate a Greatest Common Factor question"),
                            output=ChatMessage(content="{'question': 'What is the Greatest Common Factor of 48 and 60?', 'answer': '12'}")
                        )
                    ],
                    messages=[
                        ChatMessage(author="USER", content=user_message),
                    ],
                )
            ], temperature=0.7)

            content = response.responses[0].candidates[0].message.content
            print(f"ModelFarm response (attempt {attempt + 1}): {content}")

            clean_content = content.strip().replace("```python", "").replace("```", "")
            question_dict = eval(clean_content)

            if isinstance(question_dict, dict) and 'question' in question_dict and 'answer' in question_dict:
                topic_words = topic.lower().split()
                if any(word in question_dict['question'].lower() for word in topic_words):
                    return question_dict
                else:
                    print(f"Generated question not related to {topic}")
            else:
                print("Invalid response format from ModelFarm")
        except Exception as e:
            print(f"Error in attempt {attempt + 1}: {str(e)}")

    # If all retries fail, return a default question
    default_questions = {
        "Addition": {"question": "What is 5 + 7?", "answer": "12"},
        "Subtraction": {"question": "What is 15 - 8?", "answer": "7"},
        "Multiplication": {"question": "What is 6 × 9?", "answer": "54"},
        "Division": {"question": "What is 72 ÷ 9?", "answer": "8"},
        "Algebra": {"question": "Solve for x: 2x + 5 = 13", "answer": "4"},
        "Geometry": {"question": "What is the area of a rectangle with length 8 and width 6?", "answer": "48"},
        "Greatest Common Factor": {"question": "What is the Greatest Common Factor of 24 and 36?", "answer": "12"},
        "Least Common Multiple": {"question": "What is the Least Common Multiple of 4 and 6?", "answer": "12"},
        "Fractions": {"question": "What is 1/3 + 1/4?", "answer": "7/12"},
        "Decimals": {"question": "What is 0.7 + 0.35?", "answer": "1.05"},
        "Percentages": {"question": "What is 15% of 80?", "answer": "12"},
        "Exponents": {"question": "What is 2^5?", "answer": "32"},
        "Square Roots": {"question": "What is the square root of 81?", "answer": "9"},
        "Order of Operations": {"question": "Solve: 3 + 4 × 2 - 6 ÷ 2", "answer": "8"}
    }
    print(f"Falling back to default question for {topic}")
    return default_questions.get(topic, {"question": f"Default {topic} question", "answer": "Default answer"})
