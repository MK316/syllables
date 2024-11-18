def create_syllable_tree(syllable_data, syllable_number):
    graph = graphviz.Digraph(format="png")
    syllable_color = "orange" if syllable_data.get("Stress") else "black"  # Highlight stressed syllables

    # Syllable node
    graph.node(f"Syllable{syllable_number}", "Syllable", shape="ellipse", style="filled", fillcolor=syllable_color)

    # Onset Node
    if syllable_data.get("Onset"):
        graph.node(f"Onset{syllable_number}", f"Onset: {syllable_data['Onset']}", shape="ellipse")
        graph.edge(f"Syllable{syllable_number}", f"Onset{syllable_number}", arrowhead="none")

    # Always add a Rhyme node
    graph.node(f"Rhyme{syllable_number}", "Rhyme", shape="ellipse")
    graph.edge(f"Syllable{syllable_number}", f"Rhyme{syllable_number}", arrowhead="none")

    if syllable_data.get("Syllabic"):  # Syllabic consonant
        # Single node for Nucleus and Coda (shared)
        graph.node(f"Nucleus_Coda{syllable_number}", f"Nucleus/Coda: {syllable_data['Nucleus_Coda']}", shape="ellipse")
        graph.edge(f"Rhyme{syllable_number}", f"Nucleus_Coda{syllable_number}", arrowhead="none")
    else:
        # Nucleus Node
        if syllable_data.get("Nucleus"):
            graph.node(f"Nucleus{syllable_number}", f"Nucleus: {syllable_data['Nucleus']}", shape="ellipse")
            graph.edge(f"Rhyme{syllable_number}", f"Nucleus{syllable_number}", arrowhead="none")

        # Coda Node
        if syllable_data.get("Coda"):
            graph.node(f"Coda{syllable_number}", f"Coda: {syllable_data['Coda']}", shape="ellipse")
            graph.edge(f"Rhyme{syllable_number}", f"Coda{syllable_number}", arrowhead="none")

    return graph
