import os
import openai

try:
    from replit.ai.modelfarm import ChatExample, ChatMessage, ChatModel, ChatSession
    USE_MODELFARM = True
except ImportError:
    USE_MODELFARM = False

# Initialize OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_math_question(topic: str) -> dict:
    if USE_MODELFARM:
        return generate_math_question_modelfarm(topic)
    else:
        return generate_math_question_openai(topic)

def generate_math_question_modelfarm(topic: str) -> dict:
    model = ChatModel("chat-bison")
    
    try:
        response = model.chat([
            ChatSession(
                context=f"You are a math teacher generating {topic} questions for a quiz. Provide a question and its answer in a dictionary format with 'question' and 'answer' keys.",
                examples=[
                    ChatExample(
                        input=ChatMessage(content="Generate an addition question"),
                        output=ChatMessage(content="{'question': 'What is 15 + 27?', 'answer': '42'}")
                    )
                ],
                messages=[
                    ChatMessage(author="USER", content=f"Generate a {topic} math question"),
                ],
            )
        ], temperature=0.7)
        
        content = response.responses[0].candidates[0].message.content
        question_dict = eval(content)
        
        if not isinstance(question_dict, dict) or 'question' not in question_dict or 'answer' not in question_dict:
            raise ValueError("Invalid response format from ModelFarm.")
        
        return question_dict
    except Exception as e:
        print(f"Error generating question with ModelFarm: {e}")
        return {"question": "Error generating question. Please try again.", "answer": None}

def generate_math_question_openai(topic: str) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a math teacher generating {topic} questions for a quiz. Provide a question and its answer in a dictionary format with 'question' and 'answer' keys."},
                {"role": "user", "content": f"Generate a {topic} math question"}
            ],
            max_tokens=100
        )
        
        content = response.choices[0].message.content
        question_dict = eval(content)
        
        if not isinstance(question_dict, dict) or 'question' not in question_dict or 'answer' not in question_dict:
            raise ValueError("Invalid response format from OpenAI.")
        
        return question_dict
    except Exception as e:
        print(f"Error generating question with OpenAI: {e}")
        return {"question": "Error generating question. Please try again.", "answer": None}
