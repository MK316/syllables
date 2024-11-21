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
            elif len(parts == 2:  # No onset, only Syllabic Consonant
                nucleus_coda = parts[1]
                parsed_syllables.append({"Onset": "", "Nucleus_Coda": nucleus_coda, "Syllabic": True, "Stress": is_stressed})
        elif "/" in syllable:  # Handle regular vowels
            parts = syllable.split("/")
            if len(parts) == 3:  # Onset, Nucleus, Coda
                onset, nucleus, coda = parts[0], parts[1], parts[2]
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
            elif len(parts == 2:  # Only Onset and Nucleus or Nucleus and Coda
                onset, nucleus, coda = parts[0], parts[1], ""
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
            else:  # Only Nucleus
                onset, nucleus, coda = "", parts[1], ""
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
        else:
            parsed_syllables.append({"Onset": "", "Nucleus": "", "Coda": "", "Syllabic": False, "Stress": is_stressed})
    return parsed_syllables

# Create tabs
tab1, tab2 = st.tabs(["Syllable Tree Generator", "Image Viewer"])

with tab1:
    st.title("🌳 Syllable Structure Visualizer")
    st.markdown("""
    ### 🔳 Instructions:
    1. Enter a word using IPA symbols ([Visit IPA online website](https://ipa.typeit.org/))
    
    2. Use:
       - `.` for syllable boundaries.
       - `/` to mark **both sides** of the nucleus.
       - `//` to mark **syllabic consonants** (e.g., `//n//`).
       - `ˈ` before a syllable to mark **stress**.
    3. Example: `ˈstr/ɛ/ŋ.θ//n//` for [strɛŋθn̩]
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

with tab2:
    st.title("🖼️ Image Viewer")
    
    # URL list of images stored on GitHub
    # List of image URLs hosted on GitHub
    images = [
        "https://github.com/MK316/MK-316/blob/main/images/syllables.001.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.002.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.003.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.004.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.005.png?raw=true"
    ]

    
    # State to track current image index
    if 'current_image_index' not in st.session_state:
        st.session_state.current_image_index = 0

    # Display the current image
    st.image(images[st.session_state.current_image_index], width=300)

    # Next button to show the next image
    if st.button("Next Image"):
        if st.session_state.current_image_index < len(images) - 1:
            st.session_state.current_image_index += 1
        else:
            st.session_state.current_image_index = 0  # Loop back to the first image
