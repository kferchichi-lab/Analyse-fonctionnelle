import streamlit as st
import pandas as pd
from weasyprint import HTML
import tempfile

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Analyse Fonctionnelle - Extrusion Aluminium",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour l'application Streamlit
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .section-header { font-size:22px !important; font-weight: bold; color: #1E3A8A; border-left: 5px solid #3B82F6; padding-left: 10px; margin-top: 25px; margin-bottom: 15px; }
    .highlight-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Base de données pour le tableau FAST (utilisée pour l'affichage et le PDF)
data_fast = {
    "Zone 1 : Chauffage & Cisaille": [
        {"FT": "Chauffer la matière à ~470°C", "Action": "Élever la température de la billette", "Composant": "Brûleurs à gaz / Bobines d'induction"},
        {"FT": "Contrôler la température", "Action": "Mesurer sans contact le flux thermique", "Composant": "Pyromètre optique infrarouge"},
        {"FT": "Sectionner la billette", "Action": "Couper à chaud sans perte de matière", "Composant": "Cisaille hydraulique (Lame + Vérin)"}
    ],
    "Zone 2 : Presse d'Extrusion (Cœur)": [
        {"FT": "Générer la force de poussée", "Action": "Développer jusqu'à 3500T de pression", "Composant": "Pompes hydrauliques + Cylindre principal"},
        {"FT": "Contenir la billette", "Action": "Maintenir la pression latérale et la chaleur", "Composant": "Le Conteneur + Résistances électriques"},
        {"FT": "Pousser le métal", "Action": "Transmettre la force sans retour de matière", "Composant": "Tige de poussée + Grain expansible"},
        {"FT": "Verrouiller l'outillage", "Action": "Maintenir la matrice face au conteneur", "Composant": "Porte-matrice + Verrou hydraulique"},
        {"FT": "Éliminer le résidu", "Action": "Trancher le culot de billette en fin de cycle", "Composant": "Cisaille de culot arrière"}
    ],
    "Zone 3 : Sortie, Trempe & Puller": [
        {"FT": "Refroidir brutalement", "Action": "Figer la structure moléculaire (Trempe)", "Composant": "Caisson de trempe (Ventilateurs + Sprays)"},
        {"FT": "Guider et tracter", "Action": "Maintenir une tension axiale constante", "Composant": "Le Puller (Chariot motorisé à pinces)"},
        {"FT": "Supporter la dépose", "Action": "Éviter les rayures sur l'alu chaud", "Composant": "Table de transfert en feutre Kevlar"}
    ],
    "Zone 4 : Banc d'étirage & Coupe": [
        {"FT": "Supprimer les torsions", "Action": "Étirer mécaniquement les barres (1 à 3%)", "Composant": "Banc d'étirage (Mors fixe + Vérin)"},
        {"FT": "Dimensionner", "Action": "Couper en longueurs marchandes (ex: 6m)", "Composant": "Scie de finition + Micro-lubrification"}
    ],
    "Zone 5 : Four de Vieillissement": [
        {"FT": "Diffuser la chaleur", "Action": "Maintenir à ~185°C pendant 6h", "Composant": "Four à convection + Ventilateurs"}
    ]
}

# --- FONCTION DE GÉNÉRATION DU PDF RAPPORT (HTML TO PDF VIA WEASYPRINT) ---
def generer_rapport_pdf():
    html_content = """
    <html>
    <head>
        <style>
            @page { size: A4; margin: 20mm; @bottom-right { content: "Page " counter(page); font-size: 9pt; } }
            body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; line-height: 1.5; font-size: 10pt; }
            h1 { text-align: center; color: #1E3A8A; font-size: 20pt; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }
            h2 { color: #1E3A8A; font-size: 14pt; border-left: 4px solid #3B82F6; padding-left: 8px; margin-top: 20px; page-break-after: avoid; }
            .box { background-color: #F3F4F6; padding: 12px; border: 1px solid #E5E7EB; border-radius: 6px; margin-bottom: 15px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; page-break-inside: avoid; }
            th, td { border: 1px solid #D1D5DB; padding: 8px; text-align: left; }
            th { background-color: #1E3A8A; color: white; font-weight: bold; }
            tr:nth-child(even) { background-color: #F9FAFB; }
            ul { padding-left: 20px; }
        </style>
    </head>
    <body>
        <h1>Rapport Technique : Analyse Fonctionnelle d'une Ligne d'Extrusion</h1>
        <p style="text-align:center; font-style: italic; color:#666;">Document officiel d'ingénierie et de maintenance</p>
        
        <h2>1. Analyse Fonctionnelle Globale (SADT A-0)</h2>
        <div class="box">
            <strong>Fonction Globale :</strong> Transformer par déformation plastique à chaud des billettes brutes d'aluminium en profilés géométriques précis selon les tolérances requises.
        </div>
        <p><strong>Matière d'Œuvre Entrante :</strong> Billettes d'aluminium brutes, Matrices / Filières.</p>
        <p><strong>Matière d'Œuvre Sortante :</strong> Profilés d'aluminium extrudés et stabilisés, Chutes d'aluminium recyclables.</p>
        <p><strong>Contraintes de pilotage :</strong> Énergie (Gaz, Électricité, Hydraulique), Configuration (Géométrie de la matrice), Réglages process (Températures, vitesses).</p>
        
        <h2>2. Analyse Fonctionnelle Détaillée (Diagramme FAST)</h2>
    """
    
    # Ajouter dynamiquement les tableaux de toutes les zones dans le PDF
    for zone_name, items in data_fast.items():
        html_content += f"<h3>{zone_name}</h3>"
        html_content += "<table><thead><tr><th>Fonction Technique</th><th>Action attendue</th><th>Composant Responsable</th></tr></thead><tbody>"
        for item in items:
            html_content += f"<tr><td>{item['FT']}</td><td>{item['Action']}</td><td>{item['Composant']}</td></tr>"
        html_content += "</tbody></table>"
        
    html_content += """
        <h2>3. Stratégie de Maintenance & Préventif</h2>
        <table>
            <thead>
                <tr><th>Périodicité</th><th>Organe Ciblé</th><th>Type d'intervention</th></tr>
            </thead>
            <tbody>
                <tr><td>Quotidien</td><td>Groupe Hydraulique</td><td>Contrôle des fuites, niveau d'huile, T° &lt; 50°C</td></tr>
                <tr><td>Hebdomadaire</td><td>Table / Puller</td><td>Vérification des feutres Kevlar, tension des chaînes</td></tr>
                <tr><td>Mensuel</td><td>Système de Filtration</td><td>Analyse particulaire de l'huile, étalonnage pyromètres</td></tr>
                <tr><td>Annuel</td><td>Structure / Tirants</td><td>Contrôle par ultrasons (fissures), révision pompes</td></tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Compilation du HTML vers le PDF dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=html_content).write_pdf(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()
    return pdf_bytes

# --- TITRE PRINCIPAL APP ---
st.markdown('<div class="main-title">Analyse Fonctionnelle & Process d\'Extrusion d\'Aluminium</div>', unsafe_allow_html=True)

# --- BARRE LATÉRALE (SIDEBAR) ---
st.sidebar.header("🧭 Navigation")
page = st.sidebar.radio(
    "Aller vers :",
    [
        "1. Chaîne de Processus (Synoptique)",
        "2. Analyse Fonctionnelle (SADT A-0)",
        "3. Décomposition & FAST par Équipement",
        "4. Maintenance & Automatisation 4.0"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🖨️ Action Édition")

# Génération du fichier PDF et création du bouton de téléchargement
with st.sidebar:
    try:
        pdf_data = generer_rapport_pdf()
        st.download_button(
            label="📥 Télécharger le Rapport PDF",
            data=pdf_data,
            file_name="rapport_analyse_fonctionnelle_extrusion.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.success("PDF prêt pour le tirage !")
    except Exception as e:
        st.error("Erreur lors de la préparation du PDF.")

st.sidebar.markdown("---")
st.sidebar.info("**Modèle d'application :** Ligne d'extrusion intégrée (Type TPR).")

# ==========================================
# AFFICHAGE DES PAGES SUR LE SITE
# ==========================================
if page == "1. Chaîne de Processus (Synoptique)":
    st.markdown('<div class="section-header">1. Synoptique de la Chaîne de Production</div>', unsafe_allow_html=True)
    etapes = ["📦 Stock Billettes", "🔥 Préchauffage Billettes", "✂️ Cisaille à Chaud", "🏗️ Presse (Extrusion)", "❄️ Trempe (Quench)", "🚜 Puller / Traction", "📏 Banc d'Étirage", "🪚 Scie de Finition", "🧪 Four de Maturation"]
    cols = st.columns(len(etapes))
    for i, etape in enumerate(etapes):
        with cols[i]:
            st.info(etape)
            if i < len(etapes) - 1: st.markdown("<div style='text-align:center;'>➡️</div>", unsafe_allow_html=True)

elif page == "2. Analyse Fonctionnelle (SADT A-0)":
    st.markdown('<div class="section-header">2. Analyse Fonctionnelle Globale (Actigramme SADT A-0)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="highlight-box">➔ <b>Fonction Globale (A-0) :</b><br>Transformer par déformation plastique à chaud des billettes brutes d\'aluminium en profilés géométriques précis.</div>', unsafe_allow_html=True)
        st.markdown('🗳️ **Matière d\'Œuvre Entrante :**\n- Billettes brutes\n- Matrices')
        st.markdown('📦 **Matière d\'Œuvre Sortante :**\n- Profilés finis\n- Chutes d\'alu')
    with col2:
        st.markdown('⚙️ **Données de Contrôle :**')
        st.success("**Configuration (W) :** Forme de la matrice.")
        st.success("**Énergie (E) :** Électricité, Gaz, Hydraulique.")
        st.success("**Réglages (R) :** Températures et vitesse de poussée.")

elif page == "3. Décomposition & FAST par Équipement":
    st.markdown('<div class="section-header">3. Analyse Descendante & Diagramme FAST</div>', unsafe_allow_html=True)
    zone = st.selectbox("Sélectionner la zone industrielle :", list(data_fast.keys()))
    df = pd.DataFrame(data_fast[zone])
    st.table(df)

elif page == "4. Maintenance & Automatisation 4.0":
    st.markdown('<div class="section-header">4. Stratégie de Maintenance & Automatisation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🤖 Automatisation")
        st.write("Pilotage centralisé via automate maître interconnecté en Profinet avec régulation isotherme temps réel.")
    with col2:
        st.subheader("🛠️ Maintenance Préventive")
        maint_data = {
            "Périodicité": ["Quotidien", "Hebdomadaire", "Mensuel", "Annuel"],
            "Organe Ciblé": ["Groupe Hydraulique", "Table / Puller", "Filtration", "Structure / Tirants"],
            "Intervention": ["Vérification fuites, T°", "Vérification feutres Kevlar", "Analyse d'huile", "Contrôle fissures ultrasons"]
        }
        st.dataframe(pd.DataFrame(maint_data), hide_index=True)
