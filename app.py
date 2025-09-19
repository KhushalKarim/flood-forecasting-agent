# app.py
import streamlit as st
import pandas as pd
from agents import FloodRiskAgent, SafetyAgent
from visualization import show_table, show_charts, show_map

st.title("🌦️ FloodAgent - Nearby Safe Areas")

# Step 0: User input
place_input = st.text_input("Enter a place name:")

if place_input:
    # Initialize agents
    flood_agent = FloodRiskAgent()
    safety_agent = SafetyAgent()

    # Step 1: Get main forecast from Flood Risk Agent
    flood_data = flood_agent.run(place_input)

    if "error" in flood_data:
        st.error(flood_data["error"])
    else:
        # Step 2: Get nearby safe places from Safety Agent
        safety_data = safety_agent.run(flood_data["lat"], flood_data["lon"])

        # Step 3: Merge both results
        combined_data = {**flood_data, **safety_data}

        # Step 4: Display results
        df = pd.DataFrame(combined_data["main_forecast"])
        show_table(df)
        show_charts(df)
        show_map(combined_data)
