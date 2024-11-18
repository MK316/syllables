import streamlit as st
from graphviz import Digraph
import random

# Function to draw the syllable structure as a tree
def draw_syllable_tree(syllables):
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")  # Arrange syllables in a row

    for idx, syllable in enumerate(syllables, start=1):
        # Create a subgraph for each syllable
        with graph.subgraph(name=f"cluster_{idx}") as subgraph:
            subgraph.attr(label=f"Syllable {idx}")
            is_stressed = syllable.startswith("ˈ")
            if is_stressed:
                syllable = syllable[1:]  # Remove the stress marker
            
            # Parse the syllable structure
            onset, rhyme = "", ""
            nucleus, coda = "", ""
            
            if "/" in syllable:
                onset, rhyme = syllable.split("/")
                if rhyme.endswith("/"):
                    nucleus = rhyme[:-1]  # Remove the trailing '/'
                else:
                    nucleus, coda = rhyme.split("/")
            
            elif "//" in syllable:  # Syllabic consonant
                onset, rhyme = syllable.split("//")
                nucleus = coda = rhyme
            
            # Add nodes to the graph
            syllable_color = "orange" if is_stressed else "white"
            subgraph.node(f"syllable_{idx}", "Syllable", style="filled", fillcolor=syllable_color)
            
            subgraph.node(f"onset_{idx}", f"Onset: {onset}")
            subgraph.edge(f"syllable_{idx}", f"onset_{idx}")
            
            subgraph.node(f"rhyme_{idx}", "Rhyme")
            subgraph.edge(f"syllable_{idx}", f"rhyme_{idx}")
            
            if nucleus == coda:  # Syllabic consonant
                subgraph.node(f"nucleus_coda_{idx}", f"Nucleus/Coda: {nucleus}")
                subgraph.edge(f"rhyme_{idx}", f"nucleus_coda_{idx}")
            else:
                subgraph.node(f"nucleus_{idx}", f"Nucleus: {nucleus}")
                subgraph.node(f"coda_{idx}", f"Coda: {coda}")
                subgraph.edge(f"rhyme_{idx}", f"nucleus_{idx}")
                if coda:
                    subgraph.edge(f"rhyme_{idx}", f"coda_{idx}")

    return graph

# Streamlit app
st.title("Syllable Structure Visualizer")

st.markdown("""
### Instructions:
1. Enter a syllabified word or phrase.
2. Use:
   - `.` for syllable boundaries.
   - `/` to mark the nucleus.
   - `//` for syllabic consonants.
   - `ˈ` for stress before a syllable.
3. Example: `ˈstr/e.ng/th.en`.
""")

user_input = st.text_input("Enter syllabified text:", "ˈstr/e.ng/th.en")

if st.button("Generate Tree"):
    syllables = user_input.split(".")
    tree = draw_syllable_tree(syllables)
    st.graphviz_chart(tree)
