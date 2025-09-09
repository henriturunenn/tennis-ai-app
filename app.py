import streamlit as st
import requests
from openai import OpenAI

# ---- API KEYS ----
RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]
OPENAI_KEY = st.secrets["openai"]["key"]

client = OpenAI(api_key=OPENAI_KEY)

st.title("🎾 AI Tennis Companion")

# Fetch live tennis matches
url = "https://tennisapi1.p.rapidapi.com/api/tennis/live"
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "tennisapi1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    st.error("Could not fetch match data. Check API key or quota.")
else:
    matches = response.json().get("matches", [])

    if not matches:
        st.write("⚠️ No live matches right now.")
    else:
        options = [f"{m['home']} vs {m['away']}" for m in matches]
        choice = st.selectbox("Select a match:", options)
        match = matches[options.index(choice)]

        st.subheader("📊 Match Stats")
        st.json(match)

        if st.button("📝 Generate AI Summary"):
            stats_text = str(match)
            prompt = f"Write a short, engaging tennis match summary for fans using these stats: {stats_text}"
            
            result = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader("AI Match Summary")
            st.write(result.choices[0].message.content)
