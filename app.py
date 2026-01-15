import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# -------------------------
# Sentiment function
# -------------------------
def get_sentiment(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# -------------------------
# App Title
# -------------------------
st.title("💬 Real-Time Sentiment Analysis Dashboard")

st.write("Analyze single text OR upload a CSV file for bulk sentiment analysis.")

# -------------------------
# Single Text Section
# -------------------------
st.header("📝 Single Text Analysis")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("Enter your text here:")

if st.button("Analyze Text"):
    if user_input.strip() == "":
        st.warning("Please enter some text!")
    else:
        sentiment = get_sentiment(user_input)

        st.session_state.history.append({
            "Text": user_input,
            "Sentiment": sentiment
        })

        st.subheader("Result:")
        if sentiment == "Positive":
            st.success("😊 Positive")
        elif sentiment == "Negative":
            st.error("😡 Negative")
        else:
            st.info("😐 Neutral")

# Show history
if len(st.session_state.history) > 0:
    st.subheader("📜 Text Analysis History")
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist)

# -------------------------
# File Upload Section
# -------------------------
st.header("📂 Bulk Sentiment Analysis (CSV File)")

uploaded_file = st.file_uploader("Upload a CSV file (must have a 'text' column)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "text" not in df.columns:
        st.error("CSV must contain a column named 'text'")
    else:
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        # Apply sentiment
        df["Sentiment"] = df["text"].apply(get_sentiment)

        st.subheader("✅ Analyzed Data")
        st.dataframe(df)

        # Chart
        st.subheader("📊 Sentiment Distribution")

        counts = df["Sentiment"].value_counts()

        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        ax.set_title("Sentiment Count")
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")

        st.pyplot(fig)
