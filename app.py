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
        else:
            parsed_syllables.append({"Onset": "", "Nucleus_Coda": "", "Coda": "", "Syllabic": False, "Stress": is_stressed})
    return parsed_syllables

# Create tabs
tab1, tab2 = st.tabs(["Syllable Tree Generator", "Image Viewer"])

with tab1:
    st.header("🌳 Syllable Structure Visualizer")
    syllable_input = st.text_input("Enter syllabified text using IPA symbols:", placeholder="e.g., ˈstr/ɛ/.ŋ/θ/.//n//")
    if st.button("Generate Tree", key="generate"):
        syllables = parse_syllables(syllable_input)
        for i, syl in enumerate(syllables, start=1):
            st.subheader(f"Syllable {i}")
            tree = create_syllable_tree(syl, i)
            st.graphviz_chart(tree)

with tab2:
    st.header("🖼️ Image Viewer")
    # List of image URLs
    images = [
        "https://github.com/MK316/MK-316/blob/main/images/syllables.001.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.002.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.003.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.004.png?raw=true",
        "https://github.com/MK316/MK-316/blob/main/images/syllables.005.png?raw=true"
    ]

    # State management for image index
    if 'current_image_index' not in st.session_state:
        st.session_state.current_image_index = 0  # Initialize state if not present

    st.image(images[st.session_state.current_image_index], width=500)  # Display the current image

    if st.button("Next Image"):
        # Increment or loop the image index
        st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(images)
