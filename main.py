import streamlit as st
import pandas as pd
import os
from openai_integration import generate_math_question, validate_answer
from score_tracker import ScoreTracker

# Check for OpenAI API key
if not os.environ.get("OPENAI_API_KEY"):
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize session state
if 'score_tracker' not in st.session_state:
    st.session_state.score_tracker = ScoreTracker()
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False

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

# New text input for specific question request
question_request = st.text_input("Specify the type of question you want (optional):")

# Quiz mode
if not st.session_state.quiz_mode:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Question"):
            question = generate_math_question(selected_topic, selected_difficulty.lower(), question_request)
            st.session_state.current_question = question
            st.write(f"Question ({selected_difficulty}): {question['question']}")
    with col2:
        if st.button("Start Quiz"):
            st.session_state.quiz_questions = [generate_math_question(selected_topic, selected_difficulty.lower()) for _ in range(5)]
            st.session_state.current_question_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_mode = True
            st.experimental_rerun()

    # Answer input for single question mode
    user_answer = st.text_input("Your answer:")

    # Check answer button for single question mode
    if st.button("Check Answer"):
        if 'current_question' in st.session_state:
            correct_answer = st.session_state.current_question['answer']
            alternative_answers = st.session_state.current_question['alternative_answers']
            question = st.session_state.current_question['question']
            if validate_answer(question, correct_answer, alternative_answers, user_answer):
                st.success("Correct! Well done!")
                st.session_state.score_tracker.add_score(selected_topic, True)
            else:
                st.error(f"Sorry, that's incorrect. The correct answer is {correct_answer}.")
                st.session_state.score_tracker.add_score(selected_topic, False)
        else:
            st.warning("Please generate a question first.")
else:
    # Quiz mode
    if st.session_state.current_question_index < len(st.session_state.quiz_questions):
        current_question = st.session_state.quiz_questions[st.session_state.current_question_index]
        st.write(f"Question {st.session_state.current_question_index + 1}: {current_question['question']}")
        user_answer = st.text_input("Your answer:", key=f"quiz_answer_{st.session_state.current_question_index}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Question"):
                if validate_answer(current_question['question'], current_question['answer'], current_question['alternative_answers'], user_answer):
                    st.success("Correct!")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"Incorrect. The correct answer was {current_question['answer']}.")

                st.session_state.current_question_index += 1
                if st.session_state.current_question_index >= len(st.session_state.quiz_questions):
                    st.write(f"Quiz completed! Your score: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")
                    st.session_state.score_tracker.add_score(selected_topic, st.session_state.quiz_score == len(st.session_state.quiz_questions))
                    st.session_state.quiz_mode = False
                st.experimental_rerun()
        with col2:
            if st.button("End Quiz"):
                st.write(f"Quiz ended. Your score: {st.session_state.quiz_score}/{st.session_state.current_question_index}")
                st.session_state.score_tracker.add_score(selected_topic, st.session_state.quiz_score == st.session_state.current_question_index)
                st.session_state.quiz_mode = False
                st.experimental_rerun()

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
3. (Optional) Specify the type of question you want.
4. Click 'Generate Question' for a single question or 'Start Quiz' for a 5-question quiz.
5. Type your answer in the text box.
6. Click 'Check Answer' or 'Next Question' to see if you're correct.
7. Your score will be updated automatically.
8. Use 'Reset Scores' to start over.
""")
