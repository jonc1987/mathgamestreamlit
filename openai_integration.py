import os
from replit.ai.modelfarm import ChatExample, ChatMessage, ChatModel, ChatSession

def generate_math_question(topic: str, question_request: str = "") -> dict:
    return generate_math_question_modelfarm(topic, question_request)

def generate_math_question_modelfarm(topic: str, question_request: str = '') -> dict:
    model = ChatModel('chat-bison')
    context = f"You are a math teacher generating {topic} questions for a quiz. The topics include Addition, Subtraction, Multiplication, Division, Algebra, Geometry, Greatest Common Factor, Least Common Multiple, Fractions, Decimals, Percentages, Exponents, Square Roots, and Order of Operations. Provide a question and its answer in a dictionary format with 'question', 'answer', and 'alternative_answers' keys. The 'alternative_answers' should be a list of possible correct answers in different formats. It is crucial that the generated question strictly adheres to the specified topic, regardless of the difficulty level or any additional requests."
    
    if question_request:
        user_message = f"Generate a {topic} math question about {question_request}. The question MUST be about {topic}, no exceptions. Include alternative correct answers."
    else:
        user_message = f"Generate a {topic} math question. The question MUST be about {topic}, no exceptions. Include alternative correct answers."
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = model.chat([
                ChatSession(
                    context=context,
                    examples=[
                        ChatExample(
                            input=ChatMessage(content="Generate an addition question"),
                            output=ChatMessage(content="{'question': 'What is 15 + 27?', 'answer': '42', 'alternative_answers': ['42', 'forty-two', 'forty two']}")
                        ),
                        ChatExample(
                            input=ChatMessage(content="Generate a Greatest Common Factor question"),
                            output=ChatMessage(content="{'question': 'What is the Greatest Common Factor of 48 and 60?', 'answer': '12', 'alternative_answers': ['12', 'twelve']}")
                        )
                    ],
                    messages=[
                        ChatMessage(author="USER", content=user_message),
                    ],
                )
            ], temperature=0.7)

            content = response.responses[0].candidates[0].message.content
            clean_content = content.strip().replace('```python', '').replace('```', '')
            question_dict = eval(clean_content)
            
            if isinstance(question_dict, dict) and 'question' in question_dict and 'answer' in question_dict and 'alternative_answers' in question_dict:
                # Relaxed validation
                topic_keywords = get_topic_keywords(topic)
                if any(keyword in question_dict['question'].lower() for keyword in topic_keywords):
                    return question_dict
            
            print(f'Attempt {attempt + 1}: Invalid response format or unrelated question')
        except Exception as e:
            print(f'Attempt {attempt + 1}: Error - {str(e)}')
    
    # If all retries fail, return a default question
    return get_default_question(topic)

def validate_answer(question: str, correct_answer: str, alternative_answers: list, user_answer: str) -> bool:
    model = ChatModel('chat-bison')
    context = 'You are a math teacher evaluating student answers. Consider alternative correct formats and minor spelling mistakes.'
    user_message = f'Question: {question}\nCorrect answer: {correct_answer}\nAlternative answers: {", ".join(alternative_answers)}\nStudent answer: {user_answer}\nIs the student's answer correct? Respond with only "Yes" or "No".'
    
    response = model.chat([
        ChatSession(
            context=context,
            messages=[
                ChatMessage(author="USER", content=user_message),
            ],
        )
    ])
    content = response.responses[0].candidates[0].message.content.strip().lower()
    
    return content == 'yes'

def get_topic_keywords(topic: str) -> list:
    keywords = {
        'Addition': ['add', 'sum', 'plus', 'total'],
        'Subtraction': ['subtract', 'minus', 'difference', 'less'],
        'Multiplication': ['multiply', 'times', 'product'],
        'Division': ['divide', 'quotient', 'split'],
        'Algebra': ['equation', 'solve for', 'variable', 'expression'],
        'Geometry': ['shape', 'angle', 'area', 'perimeter', 'volume'],
        'Greatest Common Factor': ['gcf', 'greatest common factor', 'highest common factor'],
        'Least Common Multiple': ['lcm', 'least common multiple'],
        'Fractions': ['fraction', 'numerator', 'denominator'],
        'Decimals': ['decimal', 'point', 'tenths', 'hundredths'],
        'Percentages': ['percent', '%', 'proportion'],
        'Exponents': ['exponent', 'power', 'squared', 'cubed'],
        'Square Roots': ['square root', 'root', '√'],
        'Order of Operations': ['pemdas', 'bodmas', 'parentheses', 'brackets']
    }
    return keywords.get(topic, [topic.lower()])

def get_default_question(topic: str) -> dict:
    default_questions = {
        'Addition': {'question': 'What is 25 + 37?', 'answer': '62', 'alternative_answers': ['62', 'sixty-two', 'sixty two']},
        'Subtraction': {'question': 'What is 50 - 23?', 'answer': '27', 'alternative_answers': ['27', 'twenty-seven', 'twenty seven']},
        'Multiplication': {'question': 'What is 8 × 7?', 'answer': '56', 'alternative_answers': ['56', 'fifty-six', 'fifty six']},
        'Division': {'question': 'What is 72 ÷ 9?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
        'Algebra': {'question': 'Solve for x: 2x + 5 = 15', 'answer': '5', 'alternative_answers': ['5', 'five', 'x = 5', 'x=5']},
        'Geometry': {'question': 'What is the area of a rectangle with length 6 and width 4?', 'answer': '24', 'alternative_answers': ['24', 'twenty-four', 'twenty four', '24 square units']},
        'Greatest Common Factor': {'question': 'What is the Greatest Common Factor of 24 and 36?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
        'Least Common Multiple': {'question': 'What is the Least Common Multiple of 6 and 8?', 'answer': '24', 'alternative_answers': ['24', 'twenty-four', 'twenty four']},
        'Fractions': {'question': 'What is 1/4 + 1/2?', 'answer': '3/4', 'alternative_answers': ['3/4', '0.75', '75%']},
        'Decimals': {'question': 'What is 0.7 + 0.35?', 'answer': '1.05', 'alternative_answers': ['1.05', '1.050']},
        'Percentages': {'question': 'What is 15% of 80?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
        'Exponents': {'question': 'What is 2^3?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
        'Square Roots': {'question': 'What is the square root of 64?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
        'Order of Operations': {'question': 'What is 2 + 3 × 4?', 'answer': '14', 'alternative_answers': ['14', 'fourteen']}
    }
    return default_questions.get(topic, {'question': f'Default {topic} question', 'answer': 'Default answer', 'alternative_answers': ['Default answer']})
