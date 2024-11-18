import streamlit as st
import graphviz

# Function to parse syllable input
def parse_syllables(syllable_input):
    syllables = syllable_input.split(".")  # Split syllables by `.`
    parsed_syllables = []
    for syllable in syllables:
        if "/" in syllable:
            parts = syllable.split("/")
            if len(parts) == 3:  # Onset, Nucleus, Coda
                onset, nucleus, coda = parts[0], parts[1], parts[2]
            elif len(parts) == 2:  # Only Onset and Nucleus or Nucleus and Coda
                onset, nucleus, coda = parts[0], parts[1], ""
            else:  # Only Nucleus
                onset, nucleus, coda = "", parts[1], ""
        else:
            onset, nucleus, coda = "", "", ""
        parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda})
    return parsed_syllables

# Function to create a syllable tree with Onset, Rhyme, Nucleus, and Coda
def create_syllable_tree(syllable_data):
    graph = graphviz.Digraph(format="png")
    graph.node("Syllable", "Syllable", shape="ellipse")
    
    # Onset Node
    if syllable_data["Onset"]:
        graph.node("Onset", f"Onset: {syllable_data['Onset']}", shape="ellipse")
        graph.edge("Syllable", "Onset")
    
    # Rhyme Node
    if syllable_data["Nucleus"] or syllable_data["Coda"]:
        graph.node("Rhyme", "Rhyme", shape="ellipse")
        graph.edge("Syllable", "Rhyme")
        
        # Nucleus Node
        if syllable_data["Nucleus"]:
            graph.node("Nucleus", f"Nucleus: {syllable_data['Nucleus']}", shape="ellipse")
            graph.edge("Rhyme", "Nucleus")
        
        # Coda Node
        if syllable_data["Coda"]:
            graph.node("Coda", f"Coda: {syllable_data['Coda']}", shape="ellipse")
            graph.edge("Rhyme", "Coda")
    
    return graph

# Streamlit App
st.title("Syllable Structure Visualizer")

st.markdown("""
### Instructions:
1. Enter a syllabified word or phrase.
2. Use:
   - `.` for syllable boundaries.
   - `/` to mark **both sides** of the nucleus.
3. Example: `str/ɛ/.ŋ/θ/.en/`
""")

# Input box
syllable_input = st.text_input("Enter syllabified text:", placeholder="e.g., str/ɛ/.ŋ/θ/.en/")

# Generate button
if st.button("Generate Tree"):
    if syllable_input:
        syllables = parse_syllables(syllable_input)
        
        for i, syl in enumerate(syllables, start=1):
            if syl["Onset"] or syl["Nucleus"] or syl["Coda"]:  # Only show valid syllables
                st.markdown(f"### Syllable {i}")
                tree = create_syllable_tree(syl)
                st.graphviz_chart(tree)
    else:
        st.error("Please enter a valid syllabified input.")
