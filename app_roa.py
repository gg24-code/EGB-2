import streamlit as st
import pandas as pd
import altair as alt
import io

# Configurazione della pagina
st.set_page_config(page_title="Calcolatore ROA Stabilizzante", layout="wide")

st.title("📊 Calcolatore ROA Stabilizzante")
st.markdown("Questa Web App calcola il livello del **ROA necessario a stabilizzare il Tier 1 ratio**.")

# Barra laterale per i parametri di input
st.sidebar.header("⚙️ Parametri Fissi (Input)")

quota_profitti = st.sidebar.number_input("Quota profitti distribuiti [%]", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100
coeff_rischio = st.sidebar.number_input("Coefficiente di rischio attività [%]", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100

st.sidebar.markdown("---")
st.sidebar.header("📐 Impostazioni Matrice")
st.sidebar.markdown("Personalizza i range della tabella:")

t1_min = st.sidebar.number_input("Livello Tier 1 Minimo [%] (Es. 8%)", min_value=1.0, max_value=20.0, value=8.0, step=1.0) / 100
t1_max = st.sidebar.number_input("Livello Tier 1 Massimo [%]", min_value=2.0, max_value=30.0, value=14.0, step=1.0) / 100

g_min = st.sidebar.number_input("Crescita Attivo Minima [%]", min_value=1.0, max_value=20.0, value=4.0, step=1.0) / 100
g_max = st.sidebar.number_input("Crescita Attivo Massima [%]", min_value=2.0, max_value=30.0, value=10.0, step=1.0) / 100

# Generazione dinamica dei range (con step di 1%)
t1_range = [t1_min + (i * 0.01) for i in range(int(round((t1_max - t1_min) * 100)) + 1)]
g_range = [g_min + (i * 0.01) for i in range(int(round((g_max - g_min) * 100)) + 1)]

# Calcolo della matrice
matrice = []
for t1 in t1_range:
    riga = []
    for g in g_range:
        roa_stab = (t1 * (g / (1 + g)) * coeff_rischio) / (1 - quota_profitti)
        riga.append(roa_stab)
    matrice.append(riga)

# Creazione del DataFrame Pandas (Tabella)
col_names = [f"{g*100:.0f}%" for g in g_range]
row_names = [f"{t1*100:.0f}%" for t1 in t1_range]

df = pd.DataFrame(matrice, index=row_names, columns=col_names)

# Visualizzazione della matrice formattata
st.subheader("📌 Matrice del ROA Stabilizzante")
st.markdown("L'incrocio tra le righe (Livello Tier 1) e le colonne (Crescita Attivo) mostra la **% di ROA** necessaria.")

# Formattazione per mostrare le percentuali a video
df_styled = df.copy()
for col in df_styled.columns:
    df_styled[col] = df_styled[col].apply(lambda x: f"{x*100:.2f} %")
    
st.dataframe(df_styled, use_container_width=True)

# Esportazione in Excel
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="ROA Stabilizzante")

st.download_button(
    label="📥 Scarica Tabella in Excel (.xlsx)",
    data=buffer.getvalue(),
    file_name="matrice_roa_stabilizzante.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Grafico Visivo
st.divider()
st.subheader("📈 Sensibilità del ROA alla Crescita dell'Attivo")
st.markdown("Il grafico illustra la relazione diretta tra la **crescita dell'attivo bancario** e la **redditività dell'attivo (ROA) minima richiesta** per non intaccare la patrimonializzazione.")

# Preparazione dati per Altair
plot_data = []
for t1 in t1_range:
    for g in g_range:
        roa_stab = (t1 * (g / (1 + g)) * coeff_rischio) / (1 - quota_profitti)
        plot_data.append({
            "Crescita Attivo": f"{g*100:.0f}%",
            "Livello Tier 1": f"{t1*100:.0f}%",
            "ROA Stabilizzante (%)": roa_stab * 100
        })

df_plot = pd.DataFrame(plot_data)

# Grafico Altair
chart = alt.Chart(df_plot).mark_line(point=True).encode(
    x=alt.X('Crescita Attivo:N', sort=col_names, title="Tasso di Crescita dell'Attivo (%)"),
    y=alt.Y('ROA Stabilizzante (%):Q', title='ROA Stabilizzante (%)', axis=alt.Axis(format='.2f')),
    color=alt.Color('Livello Tier 1:N', sort=row_names, legend=alt.Legend(title="Livello di Tier 1")),
    tooltip=[
        alt.Tooltip('Livello Tier 1:N', title='Tier 1'),
        alt.Tooltip('Crescita Attivo:N', title='Crescita Attivo'),
        alt.Tooltip('ROA Stabilizzante (%):Q', format='.2f', title='ROA Richiesto (%)')
    ]
).properties(
    height=450
).interactive()

st.altair_chart(chart, use_container_width=True)
