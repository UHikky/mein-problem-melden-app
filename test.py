import streamlit as st
import pandas as pd
from datetime import datetime
import os

EXCEL_DATEI = "Lokale_ProblemMeldungen.xlsx"

# --- 🚨 GEHEIMER EXCEL-TUNNEL (OHNE JAVASCRIPT) 🚨 ---
# Wenn Excel die URL mit ?download=true aufruft, senden wir sofort reines CSV zurück
query_params = st.query_params
if query_params.get("download") == "true":
    if os.path.exists(EXCEL_DATEI):
        df = pd.read_excel(EXCEL_DATEI)
        # Verwandelt die Excel-Daten in ein CSV-Textformat für Excel
        st.text(df.to_csv(index=False, sep=";"))
    else:
        st.text("Zeitstempel;Sitzplatz;Problem\n;;")
    st.stop() # Stoppt die Webseite hier, damit kein HTML/JavaScript geladen wird!


# --- SEITEN-STYLING (iOS Minimal-Look für Smartphones) ---
st.set_page_config(page_title="Problem Melden", page_icon="🚨", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .app-title { color: #1E67C6; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 25px; }
    div[data-baseweb="textarea"] { border-radius: 15px !important; border: 1px solid #E0E0E0 !important; background-color: white !important; }
    div.stButton > button { background-color: #007AFF !important; color: white !important; border-radius: 10px !important; width: 100% !important; padding: 12px !important; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="app-title">Problem Melden</p>', unsafe_allow_html=True)

# --- SITZPLATZ-PRÜFUNG ---
qr_platz = query_params.get("platz", None)

if qr_platz is None:
    st.error("❌ Zugriff verweigert: Kein Sitzplatz erkannt.")
    st.stop()

st.info(f"📍 **Sitzplatz: {qr_platz}**")
st.write("") 

problem_text = st.text_area(label="Problembeschreibung", placeholder="Beschreibe dein Problem hier...", label_visibility="collapsed", height=200)

# --- ABSENDEN BUTTON ---
if st.button("Senden ✓"):
    if problem_text.strip() == "":
        st.warning("Bitte beschreibe zuerst das Problem.")
    else:
        zeitpunkt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        neue_daten = pd.DataFrame([{"Zeitstempel": zeitpunkt, "Sitzplatz": str(qr_platz), "Problem": str(problem_text)}])
        
        if os.path.exists(EXCEL_DATEI):
            alt_daten = pd.read_excel(EXCEL_DATEI)
            kombiniert = pd.concat([alt_daten, neue_daten], ignore_index=True)
            kombiniert.to_excel(EXCEL_DATEI, index=False)
        else:
            neue_daten.to_excel(EXCEL_DATEI, index=False)
            
        st.success(f"🎉 Vielen Dank! Das Problem für {qr_platz} wurde erfolgreich gespeichert.")
