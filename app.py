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

# Style CSS personnalisé pour le design industriel
st.markdown("""
    <style>
    .main-title {
        font-size:32px !important;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        font-size:22px !important;
        font-weight: bold;
        color: #1E3A8A;
        border-left: 5px solid #3B82F6;
        padding-left: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    .highlight-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- TITRE PRINCIPAL ---
st.markdown('<div class="main-title">Analyse Fonctionnelle & Process d\'Extrusion d\'Aluminium</div>', unsafe_allow_html=True)
st.write("**Application interactive de cartographie industrielle, d'analyse fonctionnelle et de maintenance.**")

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
st.sidebar.subheader("🏢 Contexte Industriel")
st.sidebar.info("**Modèle d'application :** Ligne d'extrusion intégrée (Type TPR / Profilés Aluminium de haute précision).")

# ==========================================
# PAGE 1 : CHAÎNE DE PROCESSUS
# ==========================================
if page == "1. Chaîne de Processus (Synoptique)":
    st.markdown('<div class="section-header">1. Synoptique de la Chaîne de Production</div>', unsafe_allow_html=True)
    st.write("Le cycle de l'extrusion de l'aluminium est un procédé thermo-mécanique semi-continu structuré comme suit :")
    
    # Représentation visuelle des étapes
    etapes = [
        "📦 Stock Billettes", "🔥 Préchauffage Billettes", "✂️ Cisaille à Chaud", 
        "🏗️ Presse (Extrusion)", "❄️ Trempe (Quench)", "🚜 Puller / Traction", 
        "📏 Banc d'Étirage", "🪚 Scie de Finition", "🧪 Four de Maturation"
    ]
    
    # Affichage en colonnes
    cols = st.columns(len(etapes))
    for i, etape in enumerate(etapes):
        with cols[i]:
            st.info(etape)
            if i < len(etapes) - 1:
                st.markdown("<div style='text-align:center; font-size:20px;'>➡️</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Description détaillée des flux de production</div>', unsafe_allow_html=True)
    
    with st.expander("📍 Étape 1 à 3 : Préparation de la Matière (Amont)", expanded=True):
        st.write("""
        * **Stock & Préchauffage :** Les billettes d'aluminium (souvent alliage 6060/6063) sont chauffées dans un four à gaz ou à induction entre **450°C et 480°C** pour rendre le métal malléable.
        * **Cisaille à chaud :** La billette longue est sectionnée à la longueur exacte requise pour une pressée, sans perte de matière.
        """)
        
    with st.expander("📍 Étape 4 à 6 : Extrusion & Conduite (Cœur du Procédé)", expanded=True):
        st.write("""
        * **La Presse Hydraulique :** Un piston pousse l'aluminium chaud à travers une matrice préchauffée à **450°C** pour lui donner sa forme géométrique.
        * **La Trempe (Quench) :** Refroidissement brutal en sortie de filière (par air pulsé ou sprays d'eau) pour fixer les propriétés mécaniques.
        * **Le Puller :** Un extracteur mécanique maintient une tension constante pour guider le profilé droit le long de la table.
        """)

    with st.expander("📍 Étape 7 à 9 : Finition & Traitement Thermique (Aval)", expanded=True):
        st.write("""
        * **Le Stretcher (Banc de traction) :** Étirement mécanique (1% à 3%) pour éliminer les tensions internes et garantir une rectitude parfaite.
        * **Scie de finition :** Découpe des nappes de profilés aux longueurs commerciales standard (ex: 6 mètres).
        * **Four de Maturation :** Traitement thermique final à **185°C pendant 5 à 8 heures** pour atteindre le durcissement structural maximal (États métallurgiques T5 ou T6).
        """)

# ==========================================
# PAGE 2 : ANALYSE FONCTIONNELLE GLOBALE
# ==========================================
elif page == "2. Analyse Fonctionnelle (SADT A-0)":
    st.markdown('<div class="section-header">2. Analyse Fonctionnelle Globale (Actigramme SADT A-0)</div>', unsafe_allow_html=True)
    st.write("L'actigramme A-0 permet de définir la valeur ajoutée globale du système et ses contraintes de pilotage.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="highlight-box">➔ <b>Fonction Globale (A-0) :</b><br>Transformer par déformation plastique à chaud des billettes brutes d\'aluminium en profilés géométriques précis selon les tolérances requises.</div>', unsafe_allow_html=True)
        st.markdown('🗳️ **Matière d\'Œuvre Entrante (MOE) :**')
        st.write("- Billettes d'aluminium brutes\n- Matrices / Filières de rechange")
        st.markdown('📦 **Matière d\'Œuvre Sortante (MOS) :**')
        st.write("- Profilés d'aluminium extrudés et stabilisés\n- Chutes d'aluminium (destinées à la fonderie / recyclage)")

    with col2:
        st.markdown('⚙️ **Données de Contrôle & Contraintes de Pilotage :**')
        st.success("**Configuration (W) :** Géométrie et forme de la matrice installée.")
        st.success("**Énergie (E) :** Électricité (Automates/Moteurs), Gaz (Fours), Hydraulique (Presse).")
        st.success("**Réglages (R) :** Températures (Billettes/Conteneur), Vitesse de poussée, Force de traction.")
        st.success("**Exploitation (C) :** Programme de supervision (Recettes de production SCADA).")

# ==========================================
# PAGE 3 : DÉCOMPOSITION & TABLEAU FAST
# ==========================================
elif page == "3. Décomposition & FAST par Équipement":
    st.markdown('<div class="section-header">3. Analyse Descendante & Diagramme FAST</div>', unsafe_allow_html=True)
    st.write("Sélectionnez une zone de l'usine pour inspecter l'analyse fonctionnelle des équipements et sous-équipements :")

    zone = st.selectbox(
        "Sélectionner la zone industrielle :",
        [
            "Zone 1 : Chauffage & Cisaille",
            "Zone 2 : Presse d'Extrusion (Cœur)",
            "Zone 3 : Sortie, Trempe & Puller",
            "Zone 4 : Banc d'étirage & Coupe",
            "Zone 5 : Four de Vieillissement"
        ]
    )

    # Base de données pour le tableau FAST
    data_fast = {
        "Zone 1 : Chauffage & Cisaille": [
            {"FT": "Chauffer la matière à ~470°C", "Action": "Élever la température de la billette", "Composant": "Brûleurs à gaz / Bobines d'induction"},
            {"FT": "Contrôler la température", "Action": "Mesurer sans contact le flux thermique", "Composant": "Pyromètre optique infrarouge"},
            {"FT": "Sectionner la billette", "Action": "Couper à chaud sans perte de matière", "Composant": "Cisaille hydraulique (Lame + Vérin)"}
        ],
        "Zone 2 : Presse d'Extrusion (Cœur)": [
            {"FT": "Générer la force de poussée", "Action": "Développer jusqu'à 3500T de pression", "Composant": "Pompes hydrauliques à pistons + Cylindre principal"},
            {"FT": "Contenir la billette", "Action": "Maintenir la pression latérale et la chaleur", "Composant": "Le Conteneur + Résistances électriques de chemise"},
            {"FT": "Pousser le métal", "Action": "Transmettre la force sans retour de matière", "Composant": "Tige de poussée (Ram) + Grain expansible (Dummy Block)"},
            {"FT": "Verrouiller l'outillage", "Action": "Maintenir la matrice face au conteneur", "Composant": "Porte-matrice + Verrou hydraulique"},
            {"FT": "Éliminer le résidu", "Action": "Trancher le culot de billette en fin de cycle", "Composant": "Cisaille de culot arrière"}
        ],
        "Zone 3 : Sortie, Trempe & Puller": [
            {"FT": "Refroidir brutalement", "Action": "Figer la structure moléculaire (Trempe)", "Composant": "Caisson de trempe (Ventilateurs + Sprays eau)"},
            {"FT": "Guider et tracter", "Action": "Maintenir une tension axiale constante", "Composant": "Le Puller (Chariot motorisé à pinces pneumatiques)"},
            {"FT": "Supporter la dépose", "Action": "Éviter les rayures sur l'alu chaud", "Composant": "Table de transfert en feutre Kevlar / Graphite"}
        ],
        "Zone 4 : Banc d'étirage & Coupe": [
            {"FT": "Supprimer les torsions", "Action": "Étirer mécaniquement les barres (1 à 3%)", "Composant": "Banc d'étirage (Mors fixe + Vérin de traction)"},
            {"FT": "Dimensionner", "Action": "Couper en longueurs marchandes (ex: 6m)", "Composant": "Scie circulaire de finition + Micro-lubrification"}
        ],
        "Zone 5 : Four de Vieillissement": [
            {"FT": "Diffuser la chaleur", "Action": "Maintenir à ~185°C pendant 6h", "Composant": "Four à convection (Brûleurs + Ventilateurs de brassage)"}
        ]
    }

    df = pd.DataFrame(data_fast[zone])
    st.table(df)

# ==========================================
# PAGE 4 : MAINTENANCE & AUTOMATISATION
# ==========================================
elif page == "4. Maintenance & Automatisation 4.0":
    st.markdown('<div class="section-header">4. Stratégie de Maintenance & Automatisation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Automatisation par API")
        st.write("""
        * **Architecture Matérielle :** Pilotage centralisé via un automate maître (**ex: Siemens S7-1500**) interconnecté en **Profinet** haute vitesse avec des modules d'E/S déportés pour les périphériques.
        * **Régulations critiques :** * *Régulation isotherme :* Asservissement en temps réel de la vitesse du poinçon par rapport à la température de la filière.
            * *Synchronisation du Puller :* Contrôle vectoriel de couple pour éviter l'élongation non désirée des profilés.
        """)
        st.image("https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=400&q=80", caption="Automates de contrôle industriels", use_container_width=True)

    with col2:
        st.subheader("🛠️ Plan de Maintenance Préventive")
        st.write("**Fréquences clés des interventions mécaniques et hydrauliques :**")
        
        maint_data = {
            "Périodicité": ["Quotidien", "Hebdomadaire", "Mensuel", "Annuel (Grand arrêt)"],
            "Organe Ciblé": ["Groupe Hydraulique", "Table / Puller", "Système de Filtration", "Structure / Tirants de la presse"],
            "Type d'intervention": ["Contrôle des fuites, niveau d'huile, T° < 50°C", "Vérification des feutres Kevlar, tension des chaînes", "Analyse particulaire de l'huile, étalonnage pyromètres", "Contrôle par ultrasons des fissures de fatigue, révision pompes"]
        }
        st.dataframe(pd.DataFrame(maint_data), hide_index=True)
        
        st.markdown("""
        ⚠️ **Gestion du Curatif (Pannes fréquentes) :**
        1. **70% des arrêts fortuits** proviennent du circuit hydraulique (électrovanne bloquée, usure des pompes à pistons axiaux).
        2. **Pannes thermiques :** Rupture des thermocouples du conteneur dus aux vibrations et cycles thermiques intenses.
        """)

# --- PIED DE PAGE ---
st.markdown("---")
st.caption("Développé pour la visualisation des architectures de systèmes industriels - Procédé Extrusion Aluminium 2026.")
