import streamlit as st
import pandas as pd
import os
import time
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
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Set page config
st.set_page_config(page_title="AI Math Quiz", page_icon="assets/math_icon.svg")

# Difficulty selection
difficulties = ['Easy', 'Medium', 'Hard']

def quiz_setup():
    st.title("AI-Powered Addition Quiz")
    st.session_state.user_name = st.text_input("Enter your name:")
    st.session_state.selected_difficulty = st.selectbox("Select difficulty level:", difficulties)
    if st.button("Start Quiz") and st.session_state.user_name:
        st.session_state.quiz_mode = True
        st.session_state.questions_answered = 0
        st.session_state.quiz_score = 0
        st.session_state.attempt = 1
        st.session_state.start_time = time.time()
        st.session_state.current_question = generate_math_question('Addition', st.session_state.selected_difficulty.lower())
        st.rerun()

if not st.session_state.quiz_mode:
    quiz_setup()
else:
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
                    st.session_state.current_question = generate_math_question('Addition', st.session_state.selected_difficulty.lower())
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
                        st.session_state.current_question = generate_math_question('Addition', st.session_state.selected_difficulty.lower())
                    st.rerun()

    if st.session_state.questions_answered >= 5:
        end_time = time.time()
        quiz_time = end_time - st.session_state.start_time
        st.write(f"Quiz completed! Your final score: {st.session_state.quiz_score}/5")
        st.write(f"Time taken: {quiz_time:.2f} seconds")
        st.session_state.score_tracker.add_score('Addition', st.session_state.quiz_score, st.session_state.user_name, quiz_time)
        st.session_state.quiz_mode = False

    if st.button("End Quiz"):
        end_time = time.time()
        quiz_time = end_time - st.session_state.start_time
        st.write(f"Quiz ended. Your final score: {st.session_state.quiz_score}/{st.session_state.questions_answered}")
        st.write(f"Time taken: {quiz_time:.2f} seconds")
        st.session_state.score_tracker.add_score('Addition', st.session_state.quiz_score, st.session_state.user_name, quiz_time)
        st.session_state.quiz_mode = False
        st.rerun()

# Display score
st.subheader("Your Score")
score_df = st.session_state.score_tracker.get_score_dataframe()
st.dataframe(score_df)

# Display leaderboard
st.subheader("Leaderboard")
leaderboard_df = st.session_state.score_tracker.get_leaderboard_dataframe()
st.dataframe(leaderboard_df)

# Reset scores button
if st.button("Reset Scores"):
    st.session_state.score_tracker.reset_scores()
    st.success("Scores have been reset!")

# Instructions
st.sidebar.header("How to Play")
st.sidebar.write("""
1. Enter your name.
2. Choose a difficulty level.
3. Click 'Start Quiz' to begin a 5-question quiz.
4. Type your answer in the text box.
5. Click 'Submit Answer' to check if you're correct.
6. If incorrect, you'll have one more attempt.
7. Your score and time will be recorded.
8. Check the leaderboard to see how you rank!
9. Use 'Reset Scores' to start over.
""")

# Background question generation
if not st.session_state.quiz_mode:
    for difficulty in difficulties:
        if len(st.session_state.question_cache.cache.get(('Addition', difficulty.lower()), [])) < 20:
            question = generate_math_question('Addition', difficulty.lower())
            st.session_state.question_cache.add_question('Addition', difficulty.lower(), question)
