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

# Generate question button
if st.button("Generate Question"):
    question = generate_math_question(selected_topic, selected_difficulty.lower(), question_request)
    st.session_state.current_question = question
    st.write(f"Question ({selected_difficulty}): {question['question']}")

# Answer input
user_answer = st.text_input("Your answer:")

# Check answer button
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
4. Click 'Generate Question' to get a new question.
5. Type your answer in the text box.
6. Click 'Check Answer' to see if you're correct.
7. Your score will be updated automatically.
8. Use 'Reset Scores' to start over.
""")
