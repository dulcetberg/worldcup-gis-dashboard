import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import math

# 1. Page Setup & Configuration
st.set_page_config(layout="wide", page_title="2026 World Cup Analytics Hub")

# Main Title & Author Banner
st.title("⚽ 2026 FIFA World Cup: Logistics, Fatigue & Carbon GIS Simulator")
st.markdown("### Developed by: **Brian Bergstrom**")
st.markdown("📈 *Simulating jet lag, team recovery burdens, and aviation environmental footprints across North America.*")

# 2. Master Dataset: All 16 Official Venues with Coordinates
stadiums_data = {
    "New York New Jersey Stadium (MetLife)": [40.813, -74.074],
    "Dallas Stadium (AT&T)": [32.747, -97.093],
    "Atlanta Stadium (Mercedes-Benz)": [33.755, -84.401],
    "Los Angeles Stadium (SoFi)": [33.953, -118.339],
    "Miami Stadium (Hard Rock)": [25.958, -80.238],
    "San Francisco Bay Area Stadium (Levi's)": [37.403, -121.970],
    "Seattle Stadium (Lumen Field)": [47.595, -122.332],
    "Houston Stadium (NRG)": [29.684, -95.408],
    "Kansas City Stadium (Arrowhead)": [39.048, -94.483],
    "Boston Stadium (Gillette)": [42.090, -71.264],
    "Philadelphia Stadium (Lincoln Financial)": [39.900, -75.167],
    "Mexico City Stadium (Azteca)": [19.303, -99.151],
    "Monterrey Stadium (BBVA)": [25.669, -100.244],
    "Guadalajara Stadium (Akron)": [20.681, -103.462],
    "Vancouver Stadium (BC Place)": [49.276, -123.111],
    "Toronto Stadium (BMO Field)": [43.633, -79.418]
}

# 3. Tournament Schedule Database (Flight paths)
team_itineraries = {
    "United States": ["Los Angeles Stadium (SoFi)", "Seattle Stadium (Lumen Field)", "Los Angeles Stadium (SoFi)", "San Francisco Bay Area Stadium (Levi's)"],
    "Mexico": ["Mexico City Stadium (Azteca)", "Guadalajara Stadium (Akron)", "Mexico City Stadium (Azteca)", "Mexico City Stadium (Azteca)"],
    "Canada": ["Toronto Stadium (BMO Field)", "Vancouver Stadium (BC Place)", "Vancouver Stadium (BC Place)", "Los Angeles Stadium (SoFi)"],
    "England": ["New York New Jersey Stadium (MetLife)", "Boston Stadium (Gillette)", "Philadelphia Stadium (Lincoln Financial)", "Atlanta Stadium (Mercedes-Benz)"],
    "Argentina": ["Miami Stadium (Hard Rock)", "Dallas Stadium (AT&T)", "Houston Stadium (NRG)", "Miami Stadium (Hard Rock)"],
    "France": ["Kansas City Stadium (Arrowhead)", "Dallas Stadium (AT&T)", "New York New Jersey Stadium (MetLife)", "Atlanta Stadium (Mercedes-Benz)"],
    "Belgium": ["Seattle Stadium (Lumen Field)", "Vancouver Stadium (BC Place)", "Seattle Stadium (Lumen Field)", "Seattle Stadium (Lumen Field)"],
    "Norway": ["Toronto Stadium (BMO Field)", "Boston Stadium (Gillette)", "Toronto Stadium (BMO Field)", "Toronto Stadium (BMO Field)"]
}

# Dynamic fallback generation for all 48 teams
all_48_teams = [
    "Argentina", "Australia", "Austria", "Belgium", "Bosnia and Herzegovina", "Brazil", "Cabo Verde", "Canada", 
    "Colombia", "Congo DR", "Croatia", "Curaçao", "Czechia", "Côte d'Ivoire", "Ecuador", "Egypt", "England", 
    "France", "Germany", "Ghana", "Haiti", "IR Iran", "Iraq", "Japan", "Jordan", "Korea Republic", "Mexico", 
    "Morocco", "Netherlands", "New Zealand", "Norway", "Panama", "Paraguay", "Portugal", "Qatar", 
    "Saudi Arabia", "Scotland", "Senegal", "South Africa", "Spain", "Sweden", "Switzerland", "Tunisia", 
    "Türkiye", "United States", "Uruguay", "Uzbekistan"
]

for team in all_48_teams:
    if team not in team_itineraries:
        team_itineraries[team] = ["Miami Stadium (Hard Rock)", "Atlanta Stadium (Mercedes-Benz)", "New York New Jersey Stadium (MetLife)"]

# 4. GIS Engine: Geodetic Haversine Distance Formula
def haversine_km(coord1, coord2):
    R = 6371.0  # Earth's radius in kilometers
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 5. Scientific Metric Simulator Calculations
# Environmental Constants: Average commercial aviation CO2 emissions ~0.115 kg per passenger per km.
# A chartered squad + staff is roughly 60 people.
SQUAD_SIZE = 60
CO2_KG_PER_KM = 0.115

# Physiological Constants: Fatigue builds linearly based on distance + cross-stadium switches.
BASE_FATIGUE_FACTOR = 0.05

distance_ledger = []
for team, path in team_itineraries.items():
    total_dist = 0
    for i in range(len(path) - 1):
        total_dist += haversine_km(stadiums_data[path[i]], stadiums_data[path[i+1]])
    
    # Calculate carbon footprint and biological physical toll
    squad_co2_tons = (total_dist * CO2_KG_PER_KM * SQUAD_SIZE) / 1000
    fatigue_index = (total_dist * BASE_FATIGUE_FACTOR) + (len(path) * 8) # Extra penalty for packing/unpacking
    
    distance_ledger.append({
        "Country": team, 
        "Stops Visited": len(path), 
        "Total Distance (KM)": int(total_dist),
        "Carbon Footprint (Metric Tons CO2)": round(squad_co2_tons, 1),
        "Fatigue Index Rating": round(fatigue_index, 1)
    })

df_distances = pd.DataFrame(distance_ledger).sort_values(by="Fatigue Index Rating", ascending=False)

# --- SIDEBAR AUTHOR & CONTROLS ---
st.sidebar.markdown("### 🧑‍💻 Dashboard Author")
st.sidebar.info("**Brian Bergstrom**  \n*GIS Data Analytics Specialist*")
st.sidebar.write("---")

st.sidebar.subheader("⚙️ Simulation Settings")
active_team = st.sidebar.selectbox("Select Active Team Route Map", sorted(all_48_teams))

# Get specific stats for targeted active team
team_row = df_distances[df_distances["Country"] == active_team].iloc[0]

# --- UI MAIN LAYOUT: SPLIT PANEL ---
col_map, col_stats = st.columns([5, 4])

with col_stats:
    st.subheader(f"📊 Live Analytics: Team {active_team}")
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Distance Flown", value=f"{team_row['Total Distance (KM)']} km")
    m2.metric(label="Squad Carbon Burden", value=f"{team_row['Carbon Footprint (Metric Tons CO2)']} t", delta="Aviation Impact", delta_color="inverse")
    m3.metric(label="Team Fatigue Index", value=f"{team_row['Fatigue Index Rating']} pts", delta="Physiological Strain", delta_color="inverse")
    
    # Add status warn cards based on fatigue index
    if team_row['Fatigue Index Rating'] > 120:
        st.error("⚠️ **High Performance Threat:** Extreme continental transit detected. Squad recovery metrics severely compromised.")
    elif team_row['Fatigue Index Rating'] > 60:
        st.warning("⚡ **Moderate Fatigue Risk:** Mid-tier recovery routines required between match vectors.")
    else:
        st.success("🟢 **Optimal Squad Fitness:** Minimal travel requirements. Team has maximum recovery advantages.")
        
    st.write("---")
    st.subheader("🏆 Global Tournament Fatigue Leaderboard")
    
    st.dataframe(
        df_distances,
        column_config={
            "Fatigue Index Rating": st.column_config.ProgressColumn(
                "Fatigue Index Rating",
                help="Higher values = greater physical fatigue and jetlag performance drops",
                format="%.1f pts",
                min_value=0,
                max_value=max(df_distances["Fatigue Index Rating"])
            )
        },
        use_container_width=True,
        hide_index=True
    )

with col_map:
    st.subheader(f"🗺️ GIS Vector Route Layer: Team {active_team}")
    
    # Initialize Map Object over North America
    m = folium.Map(location=[38.0, -97.0], zoom_start=4, tiles="CartoDB positron")
    
    # Draw all 16 stadium background markers
    for name, coords in stadiums_data.items():
        folium.CircleMarker(
            location=coords,
            radius=6,
            color="#2c3e50",
            fill=True,
            fill_color="#34495e",
            fill_opacity=0.8,
            tooltip=name
        ).add_to(m)
        
    # Extract route lines
    selected_path = team_itineraries[active_team]
    
    if len(selected_path) > 1:
        route_coords = [stadiums_data[stadium] for stadium in selected_path]
        
        # Draw connecting line vector path
        folium.PolyLine(
            locations=route_coords,
            color="#e74c3c",
            weight=5,
            opacity=0.85,
            tooltip=f"{active_team} Vector Vector Flight Path"
        ).add_to(m)
        
        # Add sequential waypoint drop-pins
        for step, stadium_name in enumerate(selected_path):
            folium.Marker(
                location=stadiums_data[stadium_name],
                popup=f"<b>Stop {step+1}:</b> {stadium_name}",
                icon=folium.Icon(color="red", icon="plane" if step > 0 else "star", prefix="fa")
            ).add_to(m)
            
    # Render Map view into Streamlit layout
    st_folium(m, width=720, height=620, key="world_cup_gis_map")
