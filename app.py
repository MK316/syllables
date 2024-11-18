import streamlit as st
import graphviz

# Function to parse syllable input
def parse_syllables(syllable_input):
    syllables = syllable_input.split(".")  # Split syllables by `.`
    parsed_syllables = []
    for syllable in syllables:
        is_stressed = syllable.startswith("ˈ")  # Check for stress marker
        if is_stressed:
            syllable = syllable[1:]  # Remove stress marker for processing
        if "//" in syllable:  # Handle syllabic consonants
            parts = syllable.split("//")
            if len(parts) == 3:  # Onset, Syllabic Consonant (Nucleus + Coda)
                onset, nucleus_coda = parts[0], parts[1]
                parsed_syllables.append({"Onset": onset, "Nucleus_Coda": nucleus_coda, "Syllabic": True, "Stress": is_stressed})
            elif len(parts) == 2:  # No onset, only Syllabic Consonant
                nucleus_coda = parts[1]
                parsed_syllables.append({"Onset": "", "Nucleus_Coda": nucleus_coda, "Syllabic": True, "Stress": is_stressed})
        elif "/" in syllable:  # Handle regular vowels
            parts = syllable.split("/")
            if len(parts) == 3:  # Onset, Nucleus, Coda
                onset, nucleus, coda = parts[0], parts[1], parts[2]
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
            elif len(parts) == 2:  # Only Onset and Nucleus or Nucleus and Coda
                onset, nucleus, coda = parts[0], parts[1], ""
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
            else:  # Only Nucleus
                onset, nucleus, coda = "", parts[1], ""
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
        else:
            parsed_syllables.append({"Onset": "", "Nucleus": "", "Coda": "", "Syllabic": False, "Stress": is_stressed})
    return parsed_syllables

# Function to format text with double slashes
def format_with_slashes(text):
    if text.startswith("/") and text.endswith("/"):
        return text  # If already has slashes, return as is
    return f"/{text}/"  # Otherwise, add slashes

# Function to create a syllable tree with Onset, Rhyme, Nucleus, and Coda
def create_syllable_tree(syllable_data, syllable_number):
    graph = graphviz.Digraph(format="png")
    syllable_color = "orange" if syllable_data.get("Stress") else "white"  # Highlight stressed syllables

    # Create syllable node
    graph.node(
        f"Syllable{syllable_number}",
        "Syllable",
        shape="ellipse",
        style="filled",
        fillcolor=syllable_color,
        fontcolor="black",
        color="lightgray"
    )

    # Onset Node
    if syllable_data.get("Onset"):
        graph.node(
            f"Onset{syllable_number}",
            label=f"Onset\n{format_with_slashes(syllable_data['Onset'])}",
            shape="ellipse",
            style="filled",
            fillcolor="white",
            color="lightgray"
        )
        graph.edge(f"Syllable{syllable_number}", f"Onset{syllable_number}", arrowhead="none")

    # Rhyme Node
    if syllable_data.get("Syllabic"):  # Syllabic consonant
        graph.node(
            f"Rhyme{syllable_number}",
            "Rhyme",
            shape="ellipse",
            style="filled",
            fillcolor="white",
            color="lightgray"
        )
        graph.edge(f"Syllable{syllable_number}", f"Rhyme{syllable_number}", arrowhead="none")
        
        # Single node for Nucleus and Coda (shared)
        graph.node(
            f"Nucleus_Coda{syllable_number}",
            label=f"Nucleus/Coda\n{format_with_slashes(syllable_data['Nucleus_Coda'])}",
            shape="ellipse",
            style="filled",
            fillcolor="white",
            color="lightgray"
        )
        graph.edge(f"Rhyme{syllable_number}", f"Nucleus_Coda{syllable_number}", arrowhead="none")
    else:
        if syllable_data.get("Nucleus") or syllable_data.get("Coda"):
            graph.node(
                f"Rhyme{syllable_number}",
                "Rhyme",
                shape="ellipse",
                style="filled",
                fillcolor="white",
                color="lightgray"
            )
            graph.edge(f"Syllable{syllable_number}", f"Rhyme{syllable_number}", arrowhead="none")
            
            # Nucleus Node
            if syllable_data.get("Nucleus"):
                graph.node(
                    f"Nucleus{syllable_number}",
                    label=f"Nucleus\n{format_with_slashes(syllable_data['Nucleus'])}",
                    shape="ellipse",
                    style="filled",
                    fillcolor="white",
                    color="lightgray"
                )
                graph.edge(f"Rhyme{syllable_number}", f"Nucleus{syllable_number}", arrowhead="none")
            
            # Coda Node
            if syllable_data.get("Coda"):
                graph.node(
                    f"Coda{syllable_number}",
                    label=f"Coda\n{format_with_slashes(syllable_data['Coda'])}",
                    shape="ellipse",
                    style="filled",
                    fillcolor="white",
                    color="lightgray"
                )
                graph.edge(f"Rhyme{syllable_number}", f"Coda{syllable_number}", arrowhead="none")

    return graph

# Streamlit App
st.title("Syllable Structure Visualizer")

st.markdown("""
### Instructions:
1. Enter a syllabified word or phrase.
2. Use:
   - `.` for syllable boundaries.
   - `/` to mark **both sides** of the nucleus.
   - `//` to mark **syllabic consonants** (e.g., `//n//`).
   - `ˈ` before a syllable to mark **stress**.
3. Example: `ˈstr/ɛ/.ŋ/θ/.//n//`
""")

# Input box
syllable_input = st.text_input("Enter syllabified text:", placeholder="e.g., ˈstr/ɛ/.ŋ/θ/.//n//")

# Generate button
if st.button("Generate Tree"):
    if syllable_input:
        syllables = parse_syllables(syllable_input)
        
        for i, syl in enumerate(syllables, start=1):
            if syl.get("Onset") or syl.get("Nucleus") or syl.get("Coda") or syl.get("Nucleus_Coda"):
                st.markdown(f"### Syllable {i}")
                tree = create_syllable_tree(syl, i)
                st.graphviz_chart(tree)
    else:
        st.error("Please enter a valid syllabified input.")
