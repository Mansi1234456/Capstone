import streamlit as st
import requests
import plotly.express as px
import pandas as pd
st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)
# Title
st.title("Protein Feature Visualization with UniProt")

# Extended list of UniProt IDs and names
uniprot_samples = {
    "P69905": "Hemoglobin subunit alpha",
    "P68871": "Hemoglobin subunit beta",
    "P68133": "Alpha-synuclein",
    "P02649": "Apolipoprotein E",
    "P12345": "Protein X",
    "P67890": "Protein Y",
    "P54321": "Protein Z",
    "Q12345": "Protein A",
    "P12346": "Protein B",
    "P11111": "Myosin heavy chain",
    "P12347": "ATP synthase subunit",
    "Q9UBS5": "Collagen type II alpha 1 chain",
    "O14786": "Insulin receptor",
    "O00230": "Ribulose bisphosphate carboxylase",
    "P30740": "GAPDH",
    "Q9Y6A6": "Voltage-gated potassium channel",
    "Q9TYJ7": "Glutamate receptor",
    "P49760": "Serine/threonine-protein kinase",
    "P0A5Z5": "Pyruvate kinase",
    "P0A9W9": "E. coli ribosome protein",
    "P42137": "Alpha-1-antitrypsin",
    "Q9H714": "Serum amyloid A protein",
    "P04637": "CDK2 protein",
    "Q9NZK0": "P53 tumor suppressor protein",
    "Q9UJX4": "Ras-related protein",
    "O00427": "Tyrosine kinase",
    "P13056": "Calmodulin",
    "Q9GZZ3": "NADH dehydrogenase",
    "P30153": "Acetylcholinesterase",
    "P05155": "Cytochrome P450",
    "P00558": "Tumor necrosis factor receptor",
    "Q9CQ72": "Heat shock protein 90",
    "P02774": "Beta-globin",
    "P20702": "Bovine serum albumin",
    "P62937": "Interleukin-2 receptor",
    "P25963": "Erythropoietin receptor",
    "Q8NDQ2": "Eukaryotic translation initiation factor",
    "P60903": "Caspase-3",
    "Q9UN76": "Kinesin light chain",
    "Q9UHC6": "Protein kinase C",
    "P62158": "Actin, cytoplasmic",
    "Q99723": "Peptidylprolyl isomerase",
    "P08567": "Rhodopsin",
    "P49297": "Hemoglobin subunit delta",
    "Q9BXS1": "BCL-2 associated X protein",
    "Q9H9M5": "Transcription factor AP-2",
    "P51451": "Ubiquitin-conjugating enzyme",
    "P09160": "Pectinase",
    "Q6NY98": "Epithelial cadherin",
    "P04968": "Hsp70 protein",
    "P02157": "Bovine lactoferrin",
    "Q2M9R7": "Dystrophin",
    "O43389": "Rho GTPase",
    "Q14765": "Purinergic receptor",
    "Q9Y263": "Alkaline phosphatase",
    "Q9UV94": "Protein kinase AMP-activated",
    "P00533": "G-protein coupled receptor",
    "P12830": "Parathyroid hormone receptor",
    "O14540": "Thyroid-stimulating hormone receptor",
    "P01375": "Fibrinogen alpha chain",
    "Q9UBV4": "Neurotrophin receptor",
    "P63104": "Focal adhesion kinase",
    "O60736": "Retinol-binding protein",
    "Q01955": "Cadherin-like protein",
    "Q7L5Y2": "Integrin alpha 5",
    "P11532": "Actin-binding protein",
    "P02785": "Fas receptor",
    "Q99548": "P53-binding protein",
    "P03241": "Polymerase",
    "P08474": "Phospholipase",
    "P15531": "Toll-like receptor 4",
    "P01308": "Human serum albumin",
}

# Searchable dropdown for selecting a UniProt Accession ID
search_term = st.text_input("Search for a UniProt Accession ID or Name")
filtered_samples = {k: v for k, v in uniprot_samples.items() if search_term.lower() in k.lower() or search_term.lower() in v.lower()}

if not filtered_samples:
    st.warning("No results found. Try a different search term.")

accession_id = st.selectbox("Select a UniProt Accession ID", options=list(filtered_samples.keys()), format_func=lambda x: filtered_samples[x])

# Function to fetch protein data
def fetch_protein_data(accession_id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to create a DataFrame for visualization
def create_feature_df(protein_data):
    features = protein_data.get('features', [])
    data = []
    for feature in features:
        data.append({
            'feature': feature.get('type', 'N/A'),
            'start': feature.get('begin', 0),
            'end': feature.get('end', 0),
        })
    df = pd.DataFrame(data)
    return df

# Display protein data
protein_data = fetch_protein_data(accession_id)
if protein_data:
    st.write(f"**Protein Name:** {protein_data.get('protein', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'N/A')}")
    st.write(f"**Organism:** {protein_data.get('organism', {}).get('scientificName', 'N/A')}")
    st.write(f"**Sequence Length:** {protein_data.get('sequence', {}).get('length', 'N/A')}")
    st.write(f"**Function:** {protein_data.get('comments', [{}])[0].get('text', [{}])[0].get('value', 'N/A')}")

    # Create DataFrame for visualization
    feature_df = create_feature_df(protein_data)

    if not feature_df.empty:
        # Plotting with Plotly
        fig = px.bar(
            feature_df,
            x='start',
            y='feature',
            orientation='h',
            title="Protein Features",
            labels={'start': 'Start Position', 'end': 'End Position'}
        )
        st.plotly_chart(fig)

        # Embed UniProt feature viewer
        st.markdown(f"""
            <script src="https://cdn.jsdelivr.net/npm/protvista-uniprot@0.3.0/dist/protvista-uniprot.min.js"></script>
            <protvista-uniprot accession="{accession_id}"></protvista-uniprot>
            """, unsafe_allow_html=True)
    else:
        st.warning("No features found for visualization.")
else:
    st.warning("No data found for the given Uniprot Accession ID.")
