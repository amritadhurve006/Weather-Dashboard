from datetime import date, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from weather_utils import get_live_weather, search_city, weather_condition

# Page Configuration
st.set_page_config(
    page_title="Weather Trend Dashboard", page_icon="🌤️", layout="wide"
)

# Custom CSS for Ultra-Modern Glassmorphism & Glow Effects
st.markdown(
    """
    <style>
    /* Force Streamlit Sidebar Background to Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1e2f 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Completely hide Streamlit text input label wrapper */
    [data-testid="stSidebar"] div.stTextInput > label,
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Clean Search Input Styling */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border: 2px solid #38bdf8 !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
    }
    
    [data-testid="stSidebar"] input {
        color: #0f172a !important;
        font-weight: 700 !important;
        background-color: transparent !important;
    }
    
    /* Quick Status Title */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #38bdf8 !important;
        margin-bottom: 12px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Small Info Cards with Glow on Hover */
    .info-card {
        background: rgba(14, 165, 233, 0.12);
        border-radius: 14px;
        padding: 12px;
        text-align: left;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .info-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
    }
    .card-label {
        font-size: 0.8rem;
        color: #7dd3fc !important;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff !important;
    }

    /* Featured Cards */
    .featured-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.35) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 16px;
        padding: 15px;
        border: 2px solid #38bdf8;
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.4);
        margin-top: 15px;
    }
    .featured-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #7dd3fc !important;
        margin-bottom: 6px;
    }
    .featured-temp {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 6px;
    }
    .featured-details {
        font-size: 0.8rem;
        color: #e2e8f0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding-top: 6px;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Metric Cards Styling */
    .stMetric {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #7dd3fc;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        box-shadow: 0 6px 15px rgba(2, 132, 199, 0.2);
        transform: translateY(-2px);
    }
    .stMetric label {
        color: #0369a1 !important;
        font-weight: 600;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Main Title Header with Updated Icon (🌤️)
st.markdown(
    "<h1 style='color: #0284c7; display: flex; align-items: center; gap:"
    " 10px;'><span>🌤️</span> Weather Trend Dashboard</h1>",
    unsafe_allow_html=True,
)
st.divider()

# Sidebar Implementation
with st.sidebar:
  city = st.text_input(
      "Search City",
      value="Gwalior",
      label_visibility="collapsed",
      placeholder="Search City...",
  ).strip()

  if not city:
    st.warning("Please enter a city name.")
    st.stop()

  try:
    with st.spinner("Fetching data..."):
      location = search_city(city)

      if not location:
        st.error("City not found.")
        st.stop()

      weather = get_live_weather(
          location["latitude"],
          location["longitude"],
          location.get("timezone", "auto"),
      )

  except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

  current = weather["current"]
  hourly = weather["hourly"]
  daily = weather["daily"]

  # Quick Status Section
  st.markdown(
      '<div class="section-title">🧭 Quick Status</div>', unsafe_allow_html=True
  )

  wind_val = current.get("wind_speed_10m", 5.8)

  col_s1, col_s2 = st.columns(2)
  with col_s1:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">📍 Location</div>
            <div class="card-value">{location['name']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">💧 Humidity</div>
            <div class="card-value">{current['relative_humidity_2m']}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_s2:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">🌡️ Temp</div>
            <div class="card-value">{current['temperature_2m']} °C</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">💨 Wind Speed</div>
            <div class="card-value">{wind_val} km/h</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  # Upcoming Hour Temperature Card (Updated Name)
  next_temp = (
      hourly["temperature_2m"][1]
      if len(hourly["temperature_2m"]) > 1
      else current["temperature_2m"]
  )
  next_rain = (
      hourly["precipitation_probability"][1]
      if len(hourly["precipitation_probability"]) > 1
      else 0
  )
  next_wind = (
      hourly["wind_speed_10m"][1]
      if len(hourly["wind_speed_10m"]) > 1
      else current["wind_speed_10m"]
  )

  st.markdown(
      f"""
    <div class="featured-card">
        <div class="featured-title">⏱️ Upcoming Hour</div>
        <div class="featured-temp">{next_temp} °C <span style="font-size: 0.85rem; font-weight: normal; color: #fde047;">({weather_condition(hourly['weather_code'][1]) if 'weather_code' in hourly else 'Sunny'})</span></div>
        <div class="featured-details">
            💧 Rain chance: {next_rain}%<br>
            💨 Wind: {next_wind} km/h N
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# Main Dashboard Title
st.subheader(
    f"📍 Climate Analysis for: {location['name']}, "
    f"{location.get('country', '')}"
)

# Current weather metric cards (5 Columns including UV Index)
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("🌡️ Temperature", f"{current['temperature_2m']} °C", delta="Live")
c2.metric("🤗 Feels Like", f"{current['apparent_temperature']} °C")
c3.metric("💧 Humidity", f"{current['relative_humidity_2m']}%")
c4.metric("💨 Wind Speed", f"{current['wind_speed_10m']} km/h")

uv_val = (
    hourly["uv_index"][0]
    if "uv_index" in hourly and len(hourly["uv_index"]) > 0
    else 4.2
)
c5.metric("☀️ UV Index", f"{uv_val}", delta="Moderate")

st.info(
    f"🌟 **Current Weather Condition:**"
    f" {weather_condition(current['weather_code'])}"
    f" &nbsp;|&nbsp; 🌧️ **Precipitation:** {current['precipitation']} mm"
)

# Smart Weather Advice Box
temp_now = current["temperature_2m"]
advice_text = "The weather is pleasant, perfect for an outdoor walk! 🌳"
if temp_now > 35:
  advice_text = (
      "⚠️ High temperature alert! Stay hydrated and protect yourself from"
      " direct sunlight."
  )
elif temp_now < 15:
  advice_text = (
      "❄️ It's quite cold outside! Make sure to wear warm clothes before"
      " heading out."
  )

st.success(f"💡 **Smart Weather Advisor:** {advice_text}")

# Prepare DataFrames
hourly_df = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"]),
    "Temperature": hourly["temperature_2m"],
    "Humidity": hourly["relative_humidity_2m"],
    "Rain Probability": hourly["precipitation_probability"],
    "Rainfall (mm)": hourly["precipitation"],
    "Wind Speed": hourly["wind_speed_10m"],
})

hourly_df["Hour_Label"] = [
    f"{i} hour" if i > 0 else "0 hour" for i in range(len(hourly_df))
]

daily_df = pd.DataFrame({
    "Date": pd.to_datetime(daily["time"]),
    "Maximum Temperature": daily["temperature_2m_max"],
    "Minimum Temperature": daily["temperature_2m_min"],
    "Rainfall (mm)": daily["precipitation_sum"],
    "Weather Code": daily["weather_code"],
})

# Tabs for Structured Data
tabs = st.tabs([
    "📊 Overview",
    "📈 Trend Analysis",
    "☀️ 7-Day Forecast",
    "🌍 City Comparison",
    "💾 Download Data",
])

# TAB 1: OVERVIEW (Next 24 Hours Temperature Trend)
with tabs[0]:
  st.markdown("### ⚡ Next 24 Hours Temperature Progression Graph")

  df_24h = hourly_df.head(25).copy()

  fig = px.line(
      df_24h,
      x="Hour_Label",
      y="Temperature",
      markers=True,
      title="Hourly Temperature Trend",
      color_discrete_sequence=["#0284c7"],
  )
  fig.update_xaxes(
      categoryorder="array", categoryarray=df_24h["Hour_Label"].tolist()
  )
  st.plotly_chart(fig, use_container_width=True)

  st.markdown("### 📅 Daily Weather Summary")
  daily_view = daily_df.copy()
  daily_view["Condition"] = daily_view["Weather Code"].apply(weather_condition)

  st.dataframe(
      daily_view.drop(columns=["Weather Code"]),
      use_container_width=True,
      hide_index=True,
  )

# TAB 2: TREND ANALYSIS
with tabs[1]:
  st.markdown("### 📈 Deep Parameter Analysis")

  parameter = st.selectbox(
      "Select Weather Parameter to Visualize",
      [
          "Temperature",
          "Humidity",
          "Rain Probability",
          "Rainfall (mm)",
          "Wind Speed",
      ],
  )

  fig = px.line(
      hourly_df.head(168),
      x="Time",
      y=parameter,
      markers=True,
      title=f"1-Week Hourly Trend: {parameter}",
      color_discrete_sequence=["#e11d48"],
  )
  st.plotly_chart(fig, use_container_width=True)

  st.markdown("### 🌡️ Maximum vs Minimum Temperature Comparison")
  fig2 = px.line(
      daily_df,
      x="Date",
      y=["Maximum Temperature", "Minimum Temperature"],
      markers=True,
      title="Daily Temp Spread",
      color_discrete_sequence=["#f59e0b", "#3b82f6"],
  )
  st.plotly_chart(fig2, use_container_width=True)

# TAB 3: FORECAST
with tabs[2]:
  st.markdown("### 🌤️ Comprehensive 7-Day Forecast")

  forecast_df = daily_df.copy()
  forecast_df["Condition"] = forecast_df["Weather Code"].apply(weather_condition)

  st.dataframe(
      forecast_df.drop(columns=["Weather Code"]),
      use_container_width=True,
      hide_index=True,
  )

  fig = px.bar(
      forecast_df,
      x="Date",
      y="Rainfall (mm)",
      title="Expected Daily Rainfall Volume",
      color="Rainfall (mm)",
      color_continuous_scale="Blues",
  )
  st.plotly_chart(fig, use_container_width=True)

# TAB 4: CITY COMPARISON
with tabs[3]:
  st.markdown("### 🌍 Multi-City Meteorological Comparison")
  city_input_comp = st.text_input(
      "Enter cities separated by commas",
      value="Delhi, Mumbai, Bhopal, Bengaluru, Gwalior",
      key="comp_cities",
  )

  if st.button("⚖️ Compare Cities Now", type="primary"):
    names = [x.strip() for x in city_input_comp.split(",") if x.strip()]
    rows = []
    errors = []

    for name in dict.fromkeys(names):
      try:
        loc = search_city(name)
        if not loc:
          errors.append(f"{name}: not found")
          continue
        res = get_live_weather(
            loc["latitude"], loc["longitude"], loc.get("timezone", "auto")
        )
        cur = res["current"]
        rows.append({
            "City": loc["name"],
            "Country": loc.get("country", ""),
            "Temperature": cur["temperature_2m"],
            "Humidity": cur["relative_humidity_2m"],
            "Wind Speed": cur["wind_speed_10m"],
        })
      except Exception:
        errors.append(f"{name}: error fetching data")

    if rows:
      comp_df = pd.DataFrame(rows)
      fig = px.bar(
          comp_df,
          x="City",
          y="Temperature",
          color="Temperature",
          hover_data=["Country", "Humidity", "Wind Speed"],
          title="Current Temperature Comparison",
          color_continuous_scale="Blues",
      )
      st.plotly_chart(fig, use_container_width=True)
      st.dataframe(comp_df, use_container_width=True, hide_index=True)

    for err in errors:
      st.warning(err)

# TAB 5: DOWNLOAD
with tabs[4]:
  st.markdown("### 💾 Export Weather Data")

  col_d1, col_d2 = st.columns(2)
  with col_d1:
    st.download_button(
        "📥 Download Hourly Forecast (CSV)",
        data=hourly_df.to_csv(index=False).encode("utf-8"),
        file_name="hourly_weather.csv",
        mime="text/csv",
    )
  with col_d2:
    st.download_button(
        "📥 Download 7-Day Forecast (CSV)",
        data=daily_df.to_csv(index=False).encode("utf-8"),
        file_name="weather_forecast.csv",
        mime="text/csv",
    )

st.divider()
st.markdown(
    "<p style='text-align: center; color: #64748b;'>✨ Powered by Open-Meteo"
    " API | Designed for Enhanced Climate Clarity ✨</p>",
    unsafe_allow_html=True,
)