
import streamlit as st
import pandas as pd
import math

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================

st.set_page_config(
    page_title="Merton Model | Credit Risk",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STILE GRAFICO
# ============================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f5f6fa;
    }

    .main-title {
        background: linear-gradient(120deg, #74152f, #a52b49);
        padding: 25px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 22px;
    }

    .main-title h1 {
        color: white;
        font-size: 30px;
        margin-bottom: 5px;
    }

    .main-title p {
        color: #f5dfe5;
        margin-bottom: 0;
        font-size: 15px;
    }

    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #841b38;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        min-height: 125px;
    }

    .result-label {
        color: #686868;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .result-value {
        color: #74152f;
        font-size: 28px;
        font-weight: 700;
    }

    .section-title {
        color: #74152f;
        font-size: 21px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .formula-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e5d5da;
        margin-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #eadde1;
        padding: 15px;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    .footer {
        color: #777;
        text-align: center;
        font-size: 12px;
        margin-top: 35px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNZIONI DEL MODELLO DI MERTON
# ============================================================

def normal_cdf(x):
    """Funzione di ripartizione della normale standard."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


def calculate_merton(V0, D, mu, sigma, T):
    """
    Calcola:
    - logaritmo del rapporto attività/debito
    - crescita attesa corretta
    - Distance to Default
    - Probability of Default
    """

    sigma_squared = sigma ** 2

    log_ratio = math.log(V0 / D)

    adjusted_growth = mu - sigma_squared / 2

    numerator = log_ratio + adjusted_growth * T

    dd = numerator / (sigma * math.sqrt(T))

    pd = normal_cdf(-dd)

    return {
        "log_ratio": log_ratio,
        "adjusted_growth": adjusted_growth,
        "sigma_squared": sigma_squared,
        "dd": dd,
        "pd": pd
    }


# ============================================================
# INTESTAZIONE
# ============================================================

st.markdown("""
<div class="main-title">
    <h1>📊 MERTON MODEL</h1>
    <p>Credit Risk Analysis | Distance to Default & Probability of Default</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR - INPUT
# ============================================================

st.sidebar.markdown("## ⚙️ Parametri del modello")
st.sidebar.caption("Modifica i parametri per aggiornare i risultati.")

st.sidebar.markdown("---")

st.sidebar.markdown("### Valore delle attività e debito")

V0 = st.sidebar.number_input(
    "Valore delle attività (V₀)",
    min_value=0.01,
    value=100.0,
    step=5.0,
    format="%.2f"
)

D = st.sidebar.number_input(
    "Debito da rimborsare (D)",
    min_value=0.01,
    value=70.0,
    step=5.0,
    format="%.2f"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Rendimento e volatilità")

mu_percent = st.sidebar.number_input(
    "Rendimento atteso (μ) %",
    value=5.0,
    min_value=-99.0,
    max_value=200.0,
    step=0.5
)

sigma_percent = st.sidebar.number_input(
    "Volatilità delle attività (σV) %",
    value=25.0,
    min_value=0.1,
    max_value=300.0,
    step=0.5
)

# Conversione percentuale in forma decimale
mu = mu_percent / 100
sigma = sigma_percent / 100

# Varianza calcolata automaticamente
sigma_squared = sigma ** 2

st.sidebar.markdown("---")

st.sidebar.markdown("### Orizzonte temporale")

T = st.sidebar.number_input(
    "Orizzonte temporale (anni)",
    min_value=0.1,
    max_value=30.0,
    value=1.0,
    step=0.5
)

st.sidebar.markdown("---")

if st.sidebar.button("↺ Ripristina parametri iniziali", use_container_width=True):
    st.rerun()

st.sidebar.caption(
    "I valori iniziali riproducono l'esempio illustrato "
    "nelle slide del corso."
)


# ============================================================
# CONTROLLO PARAMETRI
# ============================================================

if V0 <= 0 or D <= 0 or sigma <= 0 or T <= 0:
    st.error("Inserire esclusivamente valori validi e positivi per V₀, D, σV e T.")
    st.stop()


# ============================================================
# CALCOLO MODELLO
# ============================================================

results = calculate_merton(V0, D, mu, sigma, T)

dd = results["dd"]
pd_value = results["pd"]

log_ratio = results["log_ratio"]
adjusted_growth = results["adjusted_growth"]


# ============================================================
# RISULTATI PRINCIPALI
# ============================================================

st.markdown('<div class="section-title">Risultati del modello</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Distance to Default (DD)</div>
        <div class="result-value">{dd:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Probability of Default (PD)</div>
        <div class="result-value">{pd_value * 100:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Orizzonte temporale</div>
        <div class="result-value">{T:g} anni</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("")


# ============================================================
# INTERPRETAZIONE
# ============================================================

st.markdown('<div class="section-title">Interpretazione dei risultati</div>',
            unsafe_allow_html=True)

if dd >= 4:
    st.success(
        "Distance to Default elevata: le attività si trovano "
        "a una distanza considerevole dalla soglia di default."
    )
elif dd >= 2:
    st.info(
        "Distance to Default positiva: le attività sono sopra "
        "la soglia di default, ma la distanza non è particolarmente elevata."
    )
elif dd >= 1:
    st.warning(
        "Distance to Default contenuta: l'impresa presenta "
        "una maggiore esposizione al rischio di default."
    )
else:
    st.error(
        "Distance to Default inferiore a 1: la distanza dalla "
        "soglia di default è ridotta o negativa."
    )

st.write(
    f"La Distance to Default è pari a **{dd:.4f}**. "
    f"Ciò significa che il valore delle attività si trova a "
    f"{dd:.4f} deviazioni standard dalla soglia di default "
    f"nel modello."
)


# ============================================================
# DETTAGLIO DEL CALCOLO
# ============================================================

st.markdown("---")

st.markdown('<div class="section-title">Calcolo passo per passo</div>',
            unsafe_allow_html=True)

with st.expander("Visualizza i passaggi matematici", expanded=True):

    st.markdown("**Passaggio 1 – Rapporto tra attività e debito**")

    st.latex(
        r"\ln\left(\frac{V_0}{D}\right)"
        r"=\ln\left(\frac{" + f"{V0:.4f}" +
        r"}{" + f"{D:.4f}" + r"}\right)"
        r"=" + f"{log_ratio:.6f}"
    )

    st.markdown("**Passaggio 2 – Varianza e crescita attesa corretta**")

    st.write(f"Volatilità: σV = {sigma:.6f}")

    st.write(
        f"Varianza: σV² = {sigma_squared:.6f} "
        f"({sigma_squared * 100:.4f}%)"
    )

    st.latex(
        r"\mu-\frac{\sigma_V^2}{2}"
        r"=" + f"{mu:.6f}" +
        r"-\frac{" + f"{sigma_squared:.6f}" +
        r"}{2}=" + f"{adjusted_growth:.6f}"
    )

    st.markdown("**Passaggio 3 – Distance to Default**")

    st.latex(
        r"DD=\frac{\ln(V_0/D)+"
        r"\left(\mu-\frac{\sigma_V^2}{2}\right)T}"
        r"{\sigma_V\sqrt{T}}"
    )

    st.latex(
        r"DD=\frac{" + f"{log_ratio:.6f}" +
        r"+(" + f"{adjusted_growth:.6f}" +
        r"\times " + f"{T:.4f}" +
        r")}{ " + f"{sigma:.6f}" +
        r"\sqrt{" + f"{T:.4f}" +
        r"}}=" + f"{dd:.6f}"
    )

    st.markdown("**Passaggio 4 – Probability of Default**")

    st.latex(
        r"PD=\Phi(-DD)=\Phi("
        + f"{-dd:.6f}" +
        r")"
    )

    st.latex(
        r"PD=" + f"{pd_value:.6f}" +
        r"=" + f"{pd_value * 100:.4f}" + r"\%"
    )


# ============================================================
# ANALISI MULTI-ORIZZONTE
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📈 Probability of Default su più orizzonti temporali</div>',
    unsafe_allow_html=True
)

st.write(
    "A parità di parametri di mercato, il modello calcola "
    "la Distance to Default e la PD per differenti scadenze."
)

horizons = [1, 2, 3, 5]

multi_results = []

for horizon in horizons:

    result = calculate_merton(
        V0,
        D,
        mu,
        sigma,
        horizon
    )

    multi_results.append({
        "Orizzonte (anni)": horizon,
        "Distance to Default": result["dd"],
        "Probability of Default (%)": result["pd"] * 100
    })

df = pd.DataFrame(multi_results)

# ============================================================
# TABELLA
# ============================================================

st.markdown("#### Tabella comparativa")

display_df = df.copy()

display_df["Distance to Default"] = (
    display_df["Distance to Default"].map(lambda x: f"{x:.4f}")
)

display_df["Probability of Default (%)"] = (
    display_df["Probability of Default (%)"].map(lambda x: f"{x:.2f}%")
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# GRAFICO PD
# ============================================================

st.markdown("#### Evoluzione della Probability of Default")

chart_df = df.set_index("Orizzonte (anni)")[
    ["Probability of Default (%)"]
]

st.line_chart(
    chart_df,
    use_container_width=True
)


# ============================================================
# CONFRONTO DD E PD
# ============================================================

st.markdown("#### Confronto tra Distance to Default e PD")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.caption("Distance to Default")
    st.bar_chart(
        df.set_index("Orizzonte (anni)")[
            ["Distance to Default"]
        ]
    )

with chart_col2:
    st.caption("Probability of Default (%)")
    st.bar_chart(
        df.set_index("Orizzonte (anni)")[
            ["Probability of Default (%)"]
        ]
    )


# ============================================================
# FORMULA GENERALE
# ============================================================

st.markdown("---")

st.markdown('<div class="section-title">Formula del modello di Merton</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="formula-box">
<p><b>Distance to Default</b></p>
</div>
""", unsafe_allow_html=True)

st.latex(
    r"DD=\frac{\ln(V_0/D)+"
    r"\left(\mu-\frac{\sigma_V^2}{2}\right)T}"
    r"{\sigma_V\sqrt{T}}"
)

st.markdown("""
<div class="formula-box">
<p><b>Probability of Default</b></p>
</div>
""", unsafe_allow_html=True)

st.latex(r"PD=\Phi(-DD)")

st.info(
    "Nota metodologica: σV² è calcolata automaticamente come "
    "quadrato della volatilità σV. Non è un parametro indipendente. "
    "La PD rappresenta la probabilità cumulata di default entro "
    "l'orizzonte T, secondo le ipotesi del modello."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    MERTON MODEL | CREDIT RISK ANALYSIS<br>
    Structural Credit Risk Model
</div>
""", unsafe_allow_html=True)
