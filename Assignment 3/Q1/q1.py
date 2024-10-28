import re
import requests

# Download and load the lexicon file from the URL
url = "https://openslr.elda.org/resources/11/librispeech-lexicon.txt"
response = requests.get(url)
lexicon = response.text.splitlines()

# Define pronunciation rules as functions
def apply_rule_fish(phonemes):
    # Rule 1: Any - /f/ - Any : Substituted with /ph/
    return ["/ph/" if p == "/f/" else p for p in phonemes]

def apply_rule_film(phonemes):
    # Rule 2: None - consonant - consonant : Insert a vowel between consonants
    result = []
    for i, p in enumerate(phonemes):
        result.append(p)
        if i < len(phonemes) - 1:
            # Check for consonant - consonant pairs
            if re.match(r'[b-df-hj-np-tv-z]', p) and re.match(r'[b-df-hj-np-tv-z]', phonemes[i+1]):
                result.append("/ə/")  # Insert schwa
    return result

def apply_rule_vowel(phonemes):
    # Rule 3: Any - /v,w/ - Any : Substitute with /bh/
    return ["/bh/" if p in ["/v/", "/w/"] else p for p in phonemes]

def apply_rule_measure(phonemes):
    # Rule 4: Any - /tʃ, dʒ, s, z, ʃ, ʒ / - Any : Substitute with /Es/ or /Ez/ or /ǝz/
    return ["/Ez/" if p in ["/tʃ/", "/dʒ/", "/s/", "/z/", "/ʃ/", "/ʒ/"] else p for p in phonemes]

def apply_rule_lamp(phonemes):
    # Rule 5: Nasal - Plosive - Any : Plosive is voiced
    plosives = {'/p/': '/b/', '/t/': '/d/', '/k/': '/g/'}
    result = []
    for i, p in enumerate(phonemes):
        if i > 0 and re.match(r'[m,n,ŋ]', phonemes[i-1]) and p in plosives:
            result.append(plosives[p])  # Voiced plosive
        else:
            result.append(p)
    return result

# Function to apply all rules to a phoneme list
def apply_rules(phonemes):
    phonemes = apply_rule_fish(phonemes)
    phonemes = apply_rule_film(phonemes)
    phonemes = apply_rule_vowel(phonemes)
    phonemes = apply_rule_measure(phonemes)
    phonemes = apply_rule_lamp(phonemes)
    return phonemes

# Process each word in the lexicon
modified_lexicon = []
for line in lexicon:
    # Each line has the format: WORD PHONEMES
    word, *phonemes = line.split()
    # Apply rules
    modified_phonemes = apply_rules(phonemes)
    # Store the modified transcription
    modified_lexicon.append(f"{word} {' '.join(modified_phonemes)}")

# Display or save results
for entry in modified_lexicon[:10]:  # Display first 10 results for preview
    print(entry)

# Optional: Save to file
with open("modified_librispeech_lexicon.txt", "w") as f:
    for entry in modified_lexicon:
        f.write(f"{entry}\n")
