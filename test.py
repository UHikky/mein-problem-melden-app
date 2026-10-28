import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# --- SEITEN-STYLING (iOS Minimal-Look) ---
st.set_page_config(page_title="Problem Melden", page_icon="🚨", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .app-title { color: #1E67C6; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 25px; }
    div[data-baseweb="textarea"] {
        border-radius: 15px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.05) !important;
        background-color: white !important;
    }
    div.stButton > button {
        background-color: #007AFF !important; color: white !important;
        border-radius: 10px !important; border: none !important;
        width: 100% !important; padding: 12px !important;
        font-size: 18px !important; font-weight: 500 !important;
        box-shadow: 0px 4px 6px rgba(0, 122, 255, 0.2) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="app-title">Problem Melden</p>', unsafe_allow_html=True)

# --- SITZPLATZ-PRÜFUNG ---
query_params = st.query_params
qr_platz = query_params.get("platz", None)

if qr_platz is None:
    st.error("❌ Zugriff verweigert: Kein Sitzplatz erkannt.")
    st.warning("Bitte nutzen Sie die offizielle Desktop-Verknüpfung oder scannen Sie den QR-Code an Ihrem Platz.")
    st.stop()

st.info(f"📍 **Sitzplatz: {qr_platz}**")
st.write("")

problem_text = st.text_area(label="Problembeschreibung", placeholder="Beschreibe dein Problem hier...", label_visibility="collapsed", height=200)

# --- GOOGLE SHEETS VERBINDUNG ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Fehler bei der Initialisierung der Google-Verbindung.")
    st.info(f"Details: {e}")
    st.stop()

# --- ABSENDEN BUTTON ---
if st.button("Senden"):
    if problem_text.strip() == "":
        st.warning("Bitte beschreibe zuerst das Problem.")
    else:
        zeitpunkt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        neue_daten = pd.DataFrame([{"Zeitstempel": zeitpunkt, "Sitzplatz": str(qr_platz), "Problem": str(problem_text)}])
       
        try:
            # 1. Bestehende Daten aus Google Sheets laden
            try:
                # 'Sheet1' ist der Name des Tabellenblatts unten links in Google Sheets (ggf. in 'Tabellenblatt1' ändern)
                alt_daten = conn.read(spreadsheet="ProblemMeldungen_Online", worksheet="Sheet1", ttl=0)
                kombiniert = pd.concat([alt_daten, neue_daten], ignore_index=True)
            except Exception:
                # Falls die Tabelle noch komplett leer ist
                kombiniert = neue_daten
               
            # 2. Daten zurück in die Google Tabelle schreiben
            conn.update(spreadsheet="ProblemMeldungen_Online", worksheet="Sheet1", data=kombiniert)
                                
            st.success(f"🎉 Vielen Dank! Das Problem für {qr_platz} wurde erfolgreich übermittelt.")
            
        except Exception as e:
            st.error(f"Fehler beim Schreiben in Google Sheets: {e}")
            st.info("Bitte prüfe, ob du die Tabelle für die E-Mail-Adresse aus deinen Secrets freigegeben hast.")
