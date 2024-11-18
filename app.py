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
            
            # Initialize components
            onset, rhyme = "", ""
            nucleus, coda = "", ""

            if "//" in syllable:  # Syllabic consonant
                parts = syllable.split("//")
                onset = parts[0] if len(parts) > 1 else ""
                nucleus = coda = parts[-1]
            elif "/" in syllable:  # Regular syllable
                parts = syllable.split("/")
                onset = parts[0]
                if len(parts) == 2:
                    nucleus = parts[1]
                elif len(parts) == 3:
                    nucleus = parts[1]
                    coda = parts[2]
            else:
                onset = syllable  # If no nucleus or rhyme, everything is onset

            # Add nodes to the graph
            syllable_color = "orange" if is_stressed else "white"
            subgraph.node(f"syllable_{idx}", "Syllable", style="filled", fillcolor=syllable_color, shape="ellipse")
            
            if onset:
                subgraph.node(f"onset_{idx}", f"Onset: {onset}", shape="ellipse")
                subgraph.edge(f"syllable_{idx}", f"onset_{idx}", arrowhead="none")
            
            subgraph.node(f"rhyme_{idx}", "Rhyme", shape="ellipse")
            subgraph.edge(f"syllable_{idx}", f"rhyme_{idx}", arrowhead="none")

            if nucleus == coda and nucleus:  # Syllabic consonant
                subgraph.node(f"nucleus_coda_{idx}", f"Nucleus/Coda: {nucleus}", shape="ellipse")
                subgraph.edge(f"rhyme_{idx}", f"nucleus_coda_{idx}", arrowhead="none")
            else:
                if nucleus:
                    subgraph.node(f"nucleus_{idx}", f"Nucleus: {nucleus}", shape="ellipse")
                    subgraph.edge(f"rhyme_{idx}", f"nucleus_{idx}", arrowhead="none")
                if coda:
                    subgraph.node(f"coda_{idx}", f"Coda: {coda}", shape="ellipse")
                    subgraph.edge(f"rhyme_{idx}", f"coda_{idx}", arrowhead="none")

    return graph
