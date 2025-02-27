import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import datetime

# Get API key from environment variables (recommended)
GOOGLE_API_KEY = "YOUR_API_KEY"

if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Initialize Gemini model with API key
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error initializing Gemini: {e}")
    st.stop()

def get_travel_recommendations(source, destination, travel_date, preferences, travelers, class_preference):
    """Generates travel recommendations using Gemini."""

    system_message = SystemMessage(
        content="You are a helpful travel planner. Provide a structured response with travel options (cab, train, bus, flight) and estimated costs. If you cannot find a price, write 'Price not available'."
    )
    human_message = HumanMessage(
        content=f"Find travel options from {source} to {destination} with estimated costs on {travel_date} for {travelers}. Preferences: {preferences}. Class: {class_preference}. Include prices and travel durations."
    )

    try:
        response = llm.invoke([system_message, human_message])
        return response.content
    except Exception as e:
        return f"Error generating travel recommendations: {e}"

# Streamlit UI
st.title("Powered Travel Planner")

source = st.text_input("Enter Source Place:")
destination = st.text_input("Enter Destination Place:")
travel_date = st.date_input("Select Travel Date:",min_value=datetime.date.today())
preferences = st.selectbox("Travel Preferences",options=["Budget friendly","Fastest","Most Comfortable"])
travelers = st.number_input("Number of Travelers",min_value=1, max_value=10, value=1)
class_preference = st.selectbox("Class Preference",options=["Economy","Business","First Class","Sleeper Class"])

if st.button("Travel Recommendations"):
    if source and destination:
        st.spinner("Generating travel options...")
        with st.spinner():
            recommendations = get_travel_recommendations(source, destination, travel_date, preferences, travelers, class_preference)
        st.write(recommendations)
    else:
        st.warning("Please enter both source and destination.")
