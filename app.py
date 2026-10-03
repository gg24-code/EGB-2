import streamlit as st
import pandas as pd
import numpy_financial as npf
import io

st.set_page_config(page_title="Calcolatore Costo Ammortizzato", layout="wide")

st.title("📊 Calcolatore Credito al Costo Ammortizzato")
st.markdown("Calcola il **Tasso di Interesse Effettivo (TIE)** e genera il **Piano di Ammortamento** conforme ai principi contabili (IFRS 9 / OIC 15).")

# Sidebar Parametri
st.sidebar.header("⚙️ Parametri Finanziari")

capitale = st.sidebar.number_input("Capitale Erogato (€)", min_value=1000.0, value=10000.0, step=1000.0)
durata = st.sidebar.number_input("Durata (Anni)", min_value=1, value=10, step=1)
tasso_nominale_pct = st.sidebar.number_input("Tasso Nominale Annuale (%)", min_value=0.0, value=10.0, step=0.5) / 100
commissioni = st.sidebar.number_input("Commissioni / Costi di Transazione (€)", min_value=0.0, value=300.0, step=50.0)
tipo_rimborso = st.sidebar.selectbox("Tipologia di Rimborso Capitale", ["A scadenza (Bullet)", "Rate Costanti (Francese)"])

# Calcoli base
erogazione_netta = capitale - commissioni
cedola = capitale * tasso_nominale_pct

# Generazione flussi di cassa per TIE
flussi_tie = [erogazione_netta]

if tipo_rimborso == "A scadenza (Bullet)":
    for t in range(1, durata):
        flussi_tie.append(-cedola)
    flussi_tie.append(-(cedola + capitale))
else:
    # Ammortamento Francese (rata costante)
    rata_cap_int = npf.pmt(tasso_nominale_pct, durata, -capitale)
    for t in range(1, durata + 1):
        flussi_tie.append(-rata_cap_int)

tie = npf.irr(flussi_tie)

# Tabella Piano di Ammortamento
piano = []
valore_inizio = erogazione_netta

for t in range(1, durata + 1):
    interessi_effettivi = valore_inizio * tie
    if tipo_rimborso == "A scadenza (Bullet)":
        flusso_cassa = -cedola if t < durata else -(cedola + capitale)
    else:
        flusso_cassa = -rata_cap_int
    
    costo_ammortizzato = valore_inizio + interessi_effettivi + flusso_cassa
    
    piano.append({
        "Anno": t,
        "Valore Iniziale (€)": valore_inizio,
        "Interessi Effettivi (€)": interessi_effettivi,
        "Flusso di Cassa (€)": flusso_cassa,
        "Costo Ammortizzato Finale (€)": max(0.0, costo_ammortizzato) # Evita errori di arrotondamento infinitesimi
    })
    valore_inizio = costo_ammortizzato

df_piano = pd.DataFrame(piano)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Erogazione Netta Iniziale", f"€ {erogazione_netta:,.2f}")
col2.metric("TIE (Tasso Effettivo)", f"{tie:.4%}")
col3.metric("Totale Interessi Effettivi", f"€ {df_piano['Interessi Effettivi (€)'].sum():,.2f}")
col4.metric("Totale Flussi in Uscita", f"€ {abs(df_piano['Flusso di Cassa (€)'].sum()):,.2f}")

st.subheader("📋 Piano di Ammortamento")

# Formattazione per la visualizzazione a schermo
df_display = df_piano.copy()
for col in ["Valore Iniziale (€)", "Interessi Effettivi (€)", "Flusso di Cassa (€)", "Costo Ammortizzato Finale (€)"]:
    df_display[col] = df_display[col].apply(lambda x: f"€ {x:,.2f}")

st.dataframe(df_display, use_container_width=True)

# Export in Excel
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df_piano.to_excel(writer, index=False, sheet_name="Costo Ammortizzato")

st.download_button(
    label="📥 Scarica Piano di Ammortamento in Excel (.xlsx)",
    data=buffer.getvalue(),
    file_name="piano_costo_ammortizzato.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Grafico
st.subheader("📈 Evoluzione del Costo Ammortizzato nel Tempo")
st.line_chart(df_piano.set_index("Anno")[["Valore Iniziale (€)", "Costo Ammortizzato Finale (€)"]])
