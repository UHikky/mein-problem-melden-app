import streamlit as st
import requests

# --- SEITEN-STYLING (iOS Minimal-Look) ---
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
query_params = st.query_params
qr_platz = query_params.get("platz", None)

if qr_platz is None:
    st.error("❌ Zugriff verweigert: Kein Sitzplatz erkannt.")
    st.stop()

st.info(f"📍 **Sitzplatz: {qr_platz}**")
problem_text = st.text_area(label="Problembeschreibung", placeholder="Beschreibe dein Problem hier...", label_visibility="collapsed", height=200)

# 🚨 HIER NUTZEN WIR EINEN KOSTENLOSEN WEB-DIENST, DER REINE TEXT-EMAILS VERSCHICKT 🚨
# Ersetzen Sie 'IHRE_FIRMEN_EMAIL' durch Ihre echte geschäftliche E-Mail-Adresse!
FIRMEN_EMAIL = "alba.h.ortega@gmail.com" 

# --- ABSENDEN BUTTON ---
if st.button("Senden ✓"):
    if problem_text.strip() == "":
        st.warning("Bitte beschreibe zuerst das Problem.")
    else:
        with st.spinner("Wird übermittelt..."):
            # Formsubmit ist ein kostenloser Dienst, der das Formular sicher als E-Mail an Sie weiterleitet
            form_url = f"https://formsubmit.co{FIRMEN_EMAIL}"
            payload = {
                "Sitzplatz": str(qr_platz),
                "Problembeschreibung": str(problem_text),
                "_subject": f"🚨 Problem-Meldung: Standort {qr_platz}"
            }
            try:
                antwort = requests.post(form_url, data=payload)
                if antwort.status_code == 200:
                    st.success(f"🎉 Vielen Dank! Das Problem für {qr_platz} wurde erfolgreich übermittelt.")
                else:
                    st.error("Übermittlungsfehler. Bitte versuchen Sie es später noch einmal.")
            except Exception as e:
                st.error(f"Sende-Fehler: {e}")
