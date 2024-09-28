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
    
    max_retries = 3
    for _ in range(max_retries):
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

        # Clean the content to remove markdown and unwanted syntax
        clean_content = content.strip().replace("```python", "").replace("```", "")

        try:
            question_dict = eval(clean_content)

            if not isinstance(question_dict, dict) or 'question' not in question_dict or 'answer' not in question_dict:
                raise ValueError("Invalid response format from ModelFarm.")

            # Validate that the question is related to the specified topic
            if topic.lower() in question_dict['question'].lower():
                return question_dict
        except:
            continue

    raise ValueError(f"Failed to generate a valid {topic} question after {max_retries} attempts.")
