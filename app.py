# app.py
import os
from dotenv import load_dotenv
import google.generativeai as genai  # ✅ make sure this line is here and above the configure() line

load_dotenv()          # loads .env values into environment variables
GENAI_KEY = os.getenv("GENAI_API_KEY")

# configure Gemini API key
genai.configure(api_key=GENAI_KEY)

import streamlit as st
from database import create_database, insert_query, get_all_queries
import datetime

# Make sure the database and table exist before anything else
create_database()

st.set_page_config(page_title="DB Demo - Career Counselor", layout="centered")
st.title("Database Demo — Save and View Queries")

# Simple user input UI
username = st.text_input("Username", value="guest")
mode = st.selectbox("Input type", ["text", "image", "voice"])
question = st.text_area("Type your question here")

if st.button("Save to database"):
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        # Simulated AI response (replace with your real response variable)
        simulated_response = "This is a simulated AI response for testing."
        # Save the conversation to DB
        insert_query(username, question, simulated_response, mode)
        st.success("Saved to database ✅")

# Button to fetch and show history for current user
if st.button("Show my history"):
    rows = get_all_queries(username=username)
    if not rows:
        st.info("No saved entries for this user yet.")
    else:
        st.subheader("Your past queries")
        for row in rows:
            # row layout: (id, username, input_text, response_text, input_type, timestamp)
            st.markdown(f"**Q:** {row[2]}")
            st.markdown(f"**A:** {row[3]}")
            st.caption(f"Type: {row[4]}  •  Time: {row[5]}")
            st.markdown("---")

# Optional: show all rows (for admin/testing)
if st.checkbox("Show all saved rows (admin)"):
    all_rows = get_all_queries()
    st.write(all_rows)
