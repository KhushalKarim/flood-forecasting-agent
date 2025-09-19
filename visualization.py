import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

def show_table(df):
    def color_risk(val):
        if val == "High":
            color = "red"
        elif val == "Medium":
            color = "orange"
        else:
            color = "green"
        return f'background-color: {color}; color: white; font-weight:bold'

    st.subheader("🚨 Flood Risk Table")
    st.dataframe(df.style.applymap(color_risk, subset=["flood_risk"]))

def show_charts(df):
    st.subheader("🌡️ Temperature Forecast")
    fig1, ax1 = plt.subplots()
    ax1.plot(df.index, df["temp"], marker="o", color="skyblue")
    ax1.set_ylabel("°C")
    ax1.set_xlabel("Day")
    ax1.set_xticks(df.index)
    ax1.set_xticklabels([f"Day {i+1}" for i in df.index])
    st.pyplot(fig1)

    st.subheader("💧 Humidity Forecast")
    fig2, ax2 = plt.subplots()
    ax2.plot(df.index, df["humidity"], marker="o", color="green")
    ax2.set_ylabel("%")
    ax2.set_xlabel("Day")
    ax2.set_xticks(df.index)
    ax2.set_xticklabels([f"Day {i+1}" for i in df.index])
    st.pyplot(fig2)

def show_map(agent_data):
    """Show main place + nearby safe locations on map with hover names"""
    lat = agent_data["lat"]
    lon = agent_data["lon"]
    safe = agent_data.get("safe_nearby")

    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], tooltip=f"{agent_data['place_name']} (Your Place)", 
                  icon=folium.Icon(color="red")).add_to(m)

    for nb in agent_data["nearby_forecasts"]:
        color = "green" if nb["flood_risk"]=="Low" else "orange" if nb["flood_risk"]=="Medium" else "red"
        folium.CircleMarker(
            [nb["lat"], nb["lon"]],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.7,
            tooltip=f"{nb['name']} - Risk: {nb['flood_risk']}"
        ).add_to(m)

    if safe:
        folium.Marker([safe["lat"], safe["lon"]], 
                      tooltip=f"Safest Nearby: {safe['name']} - Risk: {safe['flood_risk']}",
                      icon=folium.Icon(color="blue")).add_to(m)

    folium_static(m)
