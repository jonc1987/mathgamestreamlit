import os
from replit.ai.modelfarm import ChatExample, ChatMessage, ChatModel, ChatSession

def generate_math_question(topic: str, difficulty: str, question_request: str = "") -> dict:
    return generate_math_question_modelfarm(topic, difficulty, question_request)

def generate_math_question_modelfarm(topic: str, difficulty: str, question_request: str = '') -> dict:
    model = ChatModel('chat-bison')
    context = f"You are a math teacher generating {difficulty} {topic} questions for a quiz. The topics include Addition, Subtraction, Multiplication, Division, Algebra, Geometry, Greatest Common Factor, Least Common Multiple, Fractions, Decimals, Percentages, Exponents, Square Roots, and Order of Operations. Provide a question and its answer in a dictionary format with 'question', 'answer', and 'alternative_answers' keys. The 'alternative_answers' should be a list of possible correct answers in different formats. It is crucial that the generated question strictly adheres to the specified topic and difficulty level, regardless of any additional requests."
    
    if question_request:
        user_message = f"Generate a {difficulty} {topic} math question about {question_request}. The question MUST be about {topic} and at {difficulty} level, no exceptions. Include alternative correct answers."
    else:
        user_message = f"Generate a {difficulty} {topic} math question. The question MUST be about {topic} and at {difficulty} level, no exceptions. Include alternative correct answers."
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = model.chat([
                ChatSession(
                    context=context,
                    examples=[
                        ChatExample(
                            input=ChatMessage(content="Generate an easy addition question"),
                            output=ChatMessage(content="{'question': 'What is 5 + 3?', 'answer': '8', 'alternative_answers': ['8', 'eight']}")
                        ),
                        ChatExample(
                            input=ChatMessage(content="Generate a hard Greatest Common Factor question"),
                            output=ChatMessage(content="{'question': 'What is the Greatest Common Factor of 168, 210, and 252?', 'answer': '42', 'alternative_answers': ['42', 'forty-two', 'forty two']}")
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
            
        except Exception as e:
            print(f'Attempt {attempt + 1}: Error - {str(e)}')
    
    # If all retries fail, return a default question
    return get_default_question(topic, difficulty)

def validate_answer(question: str, correct_answer: str, alternative_answers: list, user_answer: str) -> bool:
    model = ChatModel('chat-bison')
    context = 'You are a math teacher evaluating student answers. Consider alternative correct formats and minor spelling mistakes.'
    user_message = f"Question: {question}\nCorrect answer: {correct_answer}\nAlternative answers: {', '.join(alternative_answers)}\nStudent answer: {user_answer}\nIs the student's answer correct? Respond with only 'Yes' or 'No'."
    
    response = model.chat([
        ChatSession(
            context=context,
            examples=[],
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

def get_default_question(topic: str, difficulty: str) -> dict:
    default_questions = {
        'Addition': {
            'easy': {'question': 'What is 5 + 3?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
            'medium': {'question': 'What is 25 + 37?', 'answer': '62', 'alternative_answers': ['62', 'sixty-two', 'sixty two']},
            'hard': {'question': 'What is 123 + 456 + 789?', 'answer': '1368', 'alternative_answers': ['1368', 'one thousand three hundred sixty-eight']}
        },
        'Subtraction': {
            'easy': {'question': 'What is 10 - 4?', 'answer': '6', 'alternative_answers': ['6', 'six']},
            'medium': {'question': 'What is 50 - 23?', 'answer': '27', 'alternative_answers': ['27', 'twenty-seven', 'twenty seven']},
            'hard': {'question': 'What is 1000 - 567?', 'answer': '433', 'alternative_answers': ['433', 'four hundred thirty-three']}
        },
        'Multiplication': {
            'easy': {'question': 'What is 3 × 4?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
            'medium': {'question': 'What is 8 × 7?', 'answer': '56', 'alternative_answers': ['56', 'fifty-six', 'fifty six']},
            'hard': {'question': 'What is 23 × 17?', 'answer': '391', 'alternative_answers': ['391', 'three hundred ninety-one']}
        },
        'Division': {
            'easy': {'question': 'What is 8 ÷ 2?', 'answer': '4', 'alternative_answers': ['4', 'four']},
            'medium': {'question': 'What is 72 ÷ 9?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
            'hard': {'question': 'What is 256 ÷ 16?', 'answer': '16', 'alternative_answers': ['16', 'sixteen']}
        },
        'Algebra': {
            'easy': {'question': 'Solve for x: x + 5 = 10', 'answer': '5', 'alternative_answers': ['5', 'five', 'x = 5', 'x=5']},
            'medium': {'question': 'Solve for x: 2x + 5 = 15', 'answer': '5', 'alternative_answers': ['5', 'five', 'x = 5', 'x=5']},
            'hard': {'question': 'Solve for x: 3x - 7 = 2x + 5', 'answer': '12', 'alternative_answers': ['12', 'twelve', 'x = 12', 'x=12']}
        },
        'Geometry': {
            'easy': {'question': 'What is the area of a square with side length 4?', 'answer': '16', 'alternative_answers': ['16', 'sixteen', '16 square units']},
            'medium': {'question': 'What is the area of a rectangle with length 6 and width 4?', 'answer': '24', 'alternative_answers': ['24', 'twenty-four', 'twenty four', '24 square units']},
            'hard': {'question': 'What is the volume of a cylinder with radius 3 and height 5? (Use π = 3.14)', 'answer': '141.3', 'alternative_answers': ['141.3', '141.3 cubic units', 'approximately 141.3']}
        },
        'Greatest Common Factor': {
            'easy': {'question': 'What is the Greatest Common Factor of 12 and 18?', 'answer': '6', 'alternative_answers': ['6', 'six']},
            'medium': {'question': 'What is the Greatest Common Factor of 24 and 36?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
            'hard': {'question': 'What is the Greatest Common Factor of 120, 180, and 210?', 'answer': '30', 'alternative_answers': ['30', 'thirty']}
        },
        'Least Common Multiple': {
            'easy': {'question': 'What is the Least Common Multiple of 3 and 4?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
            'medium': {'question': 'What is the Least Common Multiple of 6 and 8?', 'answer': '24', 'alternative_answers': ['24', 'twenty-four', 'twenty four']},
            'hard': {'question': 'What is the Least Common Multiple of 15, 20, and 25?', 'answer': '300', 'alternative_answers': ['300', 'three hundred']}
        },
        'Fractions': {
            'easy': {'question': 'What is 1/2 + 1/4?', 'answer': '3/4', 'alternative_answers': ['3/4', '0.75', '75%']},
            'medium': {'question': 'What is 1/4 + 1/2?', 'answer': '3/4', 'alternative_answers': ['3/4', '0.75', '75%']},
            'hard': {'question': 'What is (2/3) × (3/4)?', 'answer': '1/2', 'alternative_answers': ['1/2', '0.5', '50%']}
        },
        'Decimals': {
            'easy': {'question': 'What is 0.3 + 0.4?', 'answer': '0.7', 'alternative_answers': ['0.7', '0.70']},
            'medium': {'question': 'What is 0.7 + 0.35?', 'answer': '1.05', 'alternative_answers': ['1.05', '1.050']},
            'hard': {'question': 'What is 2.45 × 1.2?', 'answer': '2.94', 'alternative_answers': ['2.94', '2.940']}
        },
        'Percentages': {
            'easy': {'question': 'What is 10% of 50?', 'answer': '5', 'alternative_answers': ['5', 'five']},
            'medium': {'question': 'What is 15% of 80?', 'answer': '12', 'alternative_answers': ['12', 'twelve']},
            'hard': {'question': 'If something increases from 200 to 250, what is the percentage increase?', 'answer': '25%', 'alternative_answers': ['25%', '25 percent', 'twenty-five percent']}
        },
        'Exponents': {
            'easy': {'question': 'What is 2^2?', 'answer': '4', 'alternative_answers': ['4', 'four']},
            'medium': {'question': 'What is 2^3?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
            'hard': {'question': 'What is 3^4?', 'answer': '81', 'alternative_answers': ['81', 'eighty-one']}
        },
        'Square Roots': {
            'easy': {'question': 'What is the square root of 9?', 'answer': '3', 'alternative_answers': ['3', 'three']},
            'medium': {'question': 'What is the square root of 64?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
            'hard': {'question': 'What is the square root of 169?', 'answer': '13', 'alternative_answers': ['13', 'thirteen']}
        },
        'Order of Operations': {
            'easy': {'question': 'What is 2 + 3 × 2?', 'answer': '8', 'alternative_answers': ['8', 'eight']},
            'medium': {'question': 'What is 2 + 3 × 4?', 'answer': '14', 'alternative_answers': ['14', 'fourteen']},
            'hard': {'question': 'What is (2 + 3) × 4 - 6 ÷ 2?', 'answer': '17', 'alternative_answers': ['17', 'seventeen']}
        }
    }
    return default_questions.get(topic, {}).get(difficulty, {'question': f'Default {difficulty} {topic} question', 'answer': 'Default answer', 'alternative_answers': ['Default answer']})
