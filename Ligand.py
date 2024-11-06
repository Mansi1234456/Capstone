import streamlit as st
from Bio import PDB
import io
import plotly.graph_objects as go

st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)

def get_ligand_ids(pdb_content):
    pdb_content_string = io.StringIO(pdb_content.decode('utf-8'))
    parser = PDB.PDBParser()
    structure = parser.get_structure('protein', pdb_content_string)

    ligand_ids = set()
    for model in structure:
        for chain in model:
            for residue in chain:
                hetero_flag = residue.get_id()[0]
                if hetero_flag[0] != ' ':
                    ligand_ids.add(residue.id[1])
    return sorted(list(ligand_ids))

def visualize_binding_sites(pdb_content, ligand_id):
    pdb_content_string = io.StringIO(pdb_content.decode('utf-8'))
    parser = PDB.PDBParser()
    structure = parser.get_structure('protein', pdb_content_string)

    ligand_coordinates = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.id[1] == ligand_id:
                    for atom in residue:
                        ligand_coordinates.append(atom.get_coord())

    if not ligand_coordinates:
        st.error("Ligand ID not found in the protein structure.")
        return

    protein_coordinates = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    protein_coordinates.append(atom.get_coord())

    protein_x, protein_y, protein_z = zip(*protein_coordinates)
    ligand_x, ligand_y, ligand_z = zip(*ligand_coordinates)

    fig = go.Figure()

    # Add protein trace
    fig.add_trace(go.Scatter3d(
        x=protein_x, y=protein_y, z=protein_z,
        mode='markers', marker=dict(color='blue', size=3),
        name='Protein'
    ))

    # Add ligand trace
    fig.add_trace(go.Scatter3d(
        x=ligand_x, y=ligand_y, z=ligand_z,
        mode='markers', marker=dict(color='red', size=5),
        name='Ligand'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis',
        ),
        title='Protein-Ligand Binding Sites Visualization',
        margin=dict(l=0, r=0, t=40, b=0),
    )

    st.plotly_chart(fig)

def main():
    st.title("Protein-Ligand Binding Sites Visualization")

    pdb_file = st.file_uploader("Upload PDB file", type=["pdb"])

    if pdb_file is not None:
        st.write("Uploaded PDB file:", pdb_file.name)
        
        ligand_ids = get_ligand_ids(pdb_file.read())
        if ligand_ids:
            selected_ligand_id = st.selectbox("Select Ligand ID:", ligand_ids)

            if st.button("Visualize"):
                pdb_content = pdb_file.getvalue()
                visualize_binding_sites(pdb_content, selected_ligand_id)
        else:
            st.warning("No ligand IDs found in the PDB file.")

if __name__ == "__main__":
    main()