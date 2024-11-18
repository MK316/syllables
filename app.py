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
                onset, nucleus, coda = "", parts[0], ""
                parsed_syllables.append({"Onset": onset, "Nucleus": nucleus, "Coda": coda, "Syllabic": False, "Stress": is_stressed})
        else:  # Edge case: Syllable without proper nucleus (invalid but included for robustness)
            parsed_syllables.append({"Onset": "", "Nucleus": "", "Coda": "", "Syllabic": False, "Stress": is_stressed})
    return parsed_syllables
