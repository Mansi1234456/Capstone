import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Bio.PDB import PDBParser
import os
st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)
# Title
st.title("Enhanced 3D Genome View from PDB File")

# Upload PDB file
uploaded_file = st.file_uploader("Upload a PDB file", type=["pdb"])

def extract_genomic_data(file_path):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("X", file_path)
    
    # Example genomic data extraction (replace with real logic)
    data = {
        'Chromosome': ['1', '1', '1', '2', '2', '2', '3', '3', '3'],
        'Start': [100, 150, 300, 100, 200, 400, 100, 150, 300],
        'End': [200, 250, 400, 200, 300, 500, 200, 250, 400],
        'Gene': ['GeneA', 'GeneB', 'GeneC', 'GeneD', 'GeneE', 'GeneF', 'GeneG', 'GeneH', 'GeneI'],
        'Type': ['Exon', 'Intron', 'Promoter', 'Exon', 'Intron', 'Promoter', 'Exon', 'Intron', 'Promoter'],
        'Domain': ['Domain1', 'Domain2', 'Domain3', 'Domain4', 'Domain5', 'Domain6', 'Domain7', 'Domain8', 'Domain9']
    }
    df = pd.DataFrame(data)
    return df

if uploaded_file:
    st.write("Processing PDB file...")

    # Save the uploaded file temporarily
    with open("temp.pdb", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract genomic data (using mock data for now)
    pdb_data = extract_genomic_data("temp.pdb")

    st.write("Extracted Data:")
    st.write(pdb_data)

    # Dropdown for selecting a chromosome
    chromosome = st.selectbox("Select a Chromosome", options=pdb_data['Chromosome'].unique())

    # Filter data based on selected chromosome
    filtered_df = pdb_data[pdb_data['Chromosome'] == chromosome]

    st.write("Filtered Data:")
    st.write(filtered_df)

    # Plotting with Plotly 3D
    if not filtered_df.empty:
        fig = go.Figure()

        colors = {
            'Exon': 'blue',
            'Intron': 'green',
            'Promoter': 'red'
        }

        for index, row in filtered_df.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[row['Start'], row['End']],
                y=[index, index],
                z=[0, 0],
                mode='lines+markers+text',
                text=[row['Gene'], row['Gene']],
                marker=dict(size=5, color=row['Start']),
                line=dict(color=colors.get(row['Type'], 'black'), width=2)
            ))

            # Adding domain as another layer
            fig.add_trace(go.Scatter3d(
                x=[row['Start'], row['End']],
                y=[index, index],
                z=[1, 1],  # Elevate domain layer
                mode='lines+markers+text',
                text=[row['Domain'], row['Domain']],
                marker=dict(size=3, color=row['End']),
                line=dict(color='purple', width=1, dash='dash')
            ))

        fig.update_layout(
            title=f"3D Genome View for Chromosome {chromosome} with Domains",
            scene=dict(
                xaxis_title='Position',
                yaxis_title='Gene Index',
                zaxis_title='',
                yaxis=dict(showticklabels=False)  # Hide y-axis labels
            )
        )

        st.plotly_chart(fig)
    else:
        st.warning("No data to display for the selected chromosome.")

    # Clean up the temporary file
    os.remove("temp.pdb")
else:
    st.info("Please upload a PDB file to generate the 3D genome view.")
