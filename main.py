import streamlit as st
import pandas as pd
import os
from openai_integration import generate_math_question
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

# New text input for specific question request
question_request = st.text_input("Specify the type of question you want (optional):")

# Generate question button
if st.button("Generate Question"):
    question = generate_math_question(selected_topic, question_request)
    st.session_state.current_question = question
    st.write(f"Question: {question['question']}")

# Answer input
user_answer = st.text_input("Your answer:")

# Check answer button
if st.button("Check Answer"):
    if 'current_question' in st.session_state:
        correct_answer = st.session_state.current_question['answer']
        if user_answer.strip().lower() == str(correct_answer).lower():
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
2. (Optional) Specify the type of question you want.
3. Click 'Generate Question' to get a new question.
4. Type your answer in the text box.
5. Click 'Check Answer' to see if you're correct.
6. Your score will be updated automatically.
7. Use 'Reset Scores' to start over.
""")
