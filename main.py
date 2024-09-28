import streamlit as st
import pandas as pd
import os
from openai_integration import generate_math_question, validate_answer
from score_tracker import ScoreTracker
from question_cache import QuestionCache

# Check for OpenAI API key
if not os.environ.get("OPENAI_API_KEY"):
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize session state
if 'score_tracker' not in st.session_state:
    st.session_state.score_tracker = ScoreTracker()
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'attempt' not in st.session_state:
    st.session_state.attempt = 1
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'question_cache' not in st.session_state:
    st.session_state.question_cache = QuestionCache()

# Set page config
st.set_page_config(page_title="AI Math Quiz", page_icon="assets/math_icon.svg")

# Main title
st.title("AI-Powered Math Quiz")

# Topic selection
topics = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Algebra', 'Geometry', 'Greatest Common Factor', 'Least Common Multiple', 'Fractions', 'Decimals', 'Percentages', 'Exponents', 'Square Roots', 'Order of Operations']
selected_topic = st.selectbox("Select a math topic:", topics)

# Difficulty selection
difficulties = ['Easy', 'Medium', 'Hard']
selected_difficulty = st.selectbox("Select difficulty level:", difficulties)

# Start Quiz button
if st.button("Start Quiz"):
    st.session_state.quiz_mode = True
    st.session_state.questions_answered = 0
    st.session_state.quiz_score = 0
    st.session_state.attempt = 1
    st.session_state.current_question = generate_math_question(selected_topic, selected_difficulty.lower())
    st.rerun()

if st.session_state.quiz_mode:
    if st.session_state.questions_answered < 5:  # Limit to 5 questions
        st.write(f"Question {st.session_state.questions_answered + 1}: {st.session_state.current_question['question']}")
        user_answer = st.text_input("Your answer:", key=f"quiz_answer_{st.session_state.questions_answered}")

        if st.button("Submit Answer"):
            if validate_answer(st.session_state.current_question['question'], st.session_state.current_question['answer'], st.session_state.current_question['alternative_answers'], user_answer):
                st.success("Correct!")
                st.session_state.quiz_score += 1
                st.session_state.questions_answered += 1
                st.session_state.attempt = 1
                if st.session_state.questions_answered < 5:
                    st.session_state.current_question = generate_math_question(selected_topic, selected_difficulty.lower())
                st.rerun()
            else:
                if st.session_state.attempt == 1:
                    st.error("Incorrect. Try again!")
                    st.session_state.attempt = 2
                else:
                    st.error(f"Incorrect. The correct answer was {st.session_state.current_question['answer']}.")
                    st.session_state.questions_answered += 1
                    st.session_state.attempt = 1
                    if st.session_state.questions_answered < 5:
                        st.session_state.current_question = generate_math_question(selected_topic, selected_difficulty.lower())
                    st.rerun()

    if st.session_state.questions_answered >= 5:
        st.write(f"Quiz completed! Your final score: {st.session_state.quiz_score}/5")
        st.session_state.score_tracker.add_score(selected_topic, st.session_state.quiz_score)
        st.session_state.quiz_mode = False

    if st.button("End Quiz"):
        st.write(f"Quiz ended. Your final score: {st.session_state.quiz_score}/{st.session_state.questions_answered}")
        st.session_state.score_tracker.add_score(selected_topic, st.session_state.quiz_score)
        st.session_state.quiz_mode = False
        st.rerun()

# Display score
st.subheader("Your Score")
score_df = st.session_state.score_tracker.get_score_dataframe()
st.dataframe(score_df)

# Reset scores button
if st.button("Reset Scores"):
    st.session_state.score_tracker.reset_scores()
    st.success("Scores have been reset!")

# Instructions
st.sidebar.header("How to Play")
st.sidebar.write("""
1. Select a math topic from the dropdown menu.
2. Choose a difficulty level.
3. Click 'Start Quiz' to begin a 5-question quiz.
4. Type your answer in the text box.
5. Click 'Submit Answer' to check if you're correct.
6. If incorrect, you'll have one more attempt.
7. Your score will be updated automatically.
8. Use 'Reset Scores' to start over.
""")

# Background question generation
if not st.session_state.quiz_mode:
    for topic in topics:
        for difficulty in difficulties:
            if len(st.session_state.question_cache.cache.get((topic, difficulty.lower()), [])) < 20:
                question = generate_math_question(topic, difficulty.lower())
                st.session_state.question_cache.add_question(topic, difficulty.lower(), question)
