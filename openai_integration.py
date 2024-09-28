import os
from replit.ai.modelfarm import ChatExample, ChatMessage, ChatModel, ChatSession

def generate_math_question(topic: str, question_request: str = "") -> dict:
    return generate_math_question_modelfarm(topic, question_request)

def generate_math_question_modelfarm(topic: str, question_request: str = "") -> dict:
    model = ChatModel("chat-bison")
    
    context = f"You are a math teacher generating {topic} questions for a quiz. Provide a question and its answer in a dictionary format with 'question' and 'answer' keys."
    
    if question_request:
        user_message = f"Generate a {topic} math question about {question_request}"
    else:
        user_message = f"Generate a {topic} math question"
    
    response = model.chat([
        ChatSession(
            context=context,
            examples=[
                ChatExample(
                    input=ChatMessage(content="Generate an addition question"),
                    output=ChatMessage(content="{'question': 'What is 15 + 27?', 'answer': '42'}")
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

    question_dict = eval(clean_content)

    if not isinstance(question_dict, dict) or 'question' not in question_dict or 'answer' not in question_dict:
        raise ValueError("Invalid response format from ModelFarm.")
    
    return question_dict
