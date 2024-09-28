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
if 'question_cache' not in st.session_state:
    st.session_state.question_cache = QuestionCache()
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []

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
    
    # Generate 5 unique questions
    unique_questions = set()
    while len(unique_questions) < 5:
        question = generate_math_question(selected_topic, selected_difficulty.lower())
        question_key = (question['question'], question['answer'])
        if question_key not in unique_questions:
            unique_questions.add(question_key)
    
    st.session_state.quiz_questions = list(unique_questions)
    st.rerun()

if st.session_state.quiz_mode:
    if st.session_state.questions_answered < 5:
        current_question = st.session_state.quiz_questions[st.session_state.questions_answered]
        st.write(f"Question {st.session_state.questions_answered + 1}: {current_question[0]}")
        user_answer = st.text_input("Your answer:", key=f"quiz_answer_{st.session_state.questions_answered}")

        if st.button("Submit Answer"):
            if validate_answer(current_question[0], current_question[1], [], user_answer):
                st.success("Correct!")
                st.session_state.quiz_score += 1
                st.session_state.questions_answered += 1
                st.session_state.attempt = 1
                st.rerun()
            else:
                if st.session_state.attempt == 1:
                    st.error("Incorrect. Try again!")
                    st.session_state.attempt = 2
                else:
                    st.error(f"Incorrect. The correct answer was {current_question[1]}.")
                    st.session_state.questions_answered += 1
                    st.session_state.attempt = 1
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

# Display leaderboard
st.subheader("Leaderboard")
leaderboard_df = st.session_state.score_tracker.get_leaderboard()
if not leaderboard_df.empty:
    st.dataframe(leaderboard_df)
else:
    st.write("No scores available yet. Complete a quiz to see the leaderboard!")

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
