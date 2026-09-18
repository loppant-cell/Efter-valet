import streamlit as st
from google import genai

# Inställningar för sidan
st.set_page_config(page_title="Elevportal", layout="centered")

st.title("🎓 Elevportal – Svara & få direkt feedback")
st.write("Skriv ditt svar i rutan nedan. Ingen inloggning krävs och ingenting sparas.")

# ==========================================
# 1. HÄR SKRIVER DU DIN FRÅGA TILL ELEVEN
# ==========================================
st.subheader("Uppgift / Frågeställning:")
st.info("""
**Fråga:** [Förklara hur det går till att bilda regering i Sverige?]

*Instruktion:* [I din förklaring ska orden parlamentarism, talman och statsminister ingå.]
""")

# ==========================================
# 2. ELEVENS SVARSRUTA
# ==========================================
elev_svar = st.text_area("Ditt svar:", height=200, placeholder="Skriv ditt svar här...")

# ==========================================
# 3. NÄR ELEVEN KLICKAR PÅ KNAPPEN
# ==========================================
if st.button("Skicka för feedback", type="primary"):
    if not elev_svar.strip():
        st.warning("Vänligen skriv ett svar innan du skickar!")
    else:
        with st.spinner("Analyserar ditt svar och skapar återkoppling..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # ==========================================
                # 4. HÄR ANPASSAR DU FEEDBACK-INSTRUKTIONEN
                # ==========================================
                prompt = f"""
                Du är en uppmuntrande och pedagogisk lärare.
                Ge formativ feedback på följande elevsvar.

                UPPGIFT:
                [Förklara hur det går till att bilda regering i Sverige?]

                VAD ETT BRA SVAR BÖR INNEHÅLLA (BEDÖMNINGSKRITERIER):
                - [Kriterium 1, t.ex. Riksdagen väljer statsminister]
                - [Kriterium 2, t.ex. Talmannen undersöker vem som kan få tillräckligt stöd för att bilda regering]
                - [Kriterium 3, t.ex. Det finns flera sätt att bilda regering]

                ELEVENS SVAR:
                "{elev_svar}"

                HUR FEEDBACKEN SKA SKRIVAS:
                Ge feedbacken på svenska med följande struktur:
                1. 🌟 Vad du har gjort bra (Lyft fram specifika styrkor i svaret)
                2. 💡 Vad du kan utveckla eller lägga till (Konkret stöd för att förbättra svaret)
                3. ❓ Tänk vidare på (En utmanande följdfråga för att djupna kunskapen)

                Håll språket enkelt, konstruktivt och anpassat för elever.
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                st.success("Här är din återkoppling!")
                st.markdown(response.text)

            except Exception as e:
                st.error("Ett fel uppstod vid anslutning till AI-tjänsten. Kontrollera att din API-nyckel är inlagd i Streamlit Secrets.")
