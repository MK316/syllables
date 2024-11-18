import streamlit as st
import graphviz

# Function to parse syllable input
def parse_syllables(syllable_input):
    syllables = syllable_input.split(".")
    parsed_syllables = []
    for syllable in syllables:
        if "/" in syllable:
            onset, rest = syllable.split("/", 1)
            nucleus = rest[0]
            coda = rest[1:] if len(rest) > 1 else ""
        else:
            onset, nucleus, coda = "", "", ""
        parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda})
    return parsed_syllables

# Function to create a syllable tree
def create_syllable_tree(syllable_data):
    graph = graphviz.Digraph()
    graph.node("Syllable", "Syllable")
    
    if syllable_data["Onset"]:
        graph.node("Onset", f"Onset: {syllable_data['Onset']}")
        graph.edge("Syllable", "Onset")
    
    if syllable_data["Nucleus"]:
        graph.node("Nucleus", f"Nucleus: {syllable_data['Nucleus']}")
        graph.edge("Syllable", "Nucleus")
    
    if syllable_data["Coda"]:
        graph.node("Coda", f"Coda: {syllable_data['Coda']}")
        graph.edge("Syllable", "Coda")
    
    return graph

# Streamlit App
st.title("Syllable Structure Visualizer")

st.markdown("""
### Instructions:
1. Enter a syllabified word or phrase.
2. Use:
   - `.` for syllable boundaries.
   - `/` to mark the nucleus.
3. Example: `str/e.ng/th.en`
""")

# Input box
syllable_input = st.text_input("Enter syllabified text:", placeholder="e.g., str/e.ng/th.en")

# Generate button
if st.button("Generate Tree"):
    if syllable_input:
        syllables = parse_syllables(syllable_input)
        
        for i, syl in enumerate(syllables, start=1):
            st.markdown(f"### Syllable {i}")
            tree = create_syllable_tree(syl)
            st.graphviz_chart(tree, use_container_width=True)
    else:
        st.error("Please enter a valid syllabified input.")
