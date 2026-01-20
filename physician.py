import spacy
from keybert import KeyBERT

# Load models
nlp = spacy.load("en_ner_bc5cdr_md")   # Medical NER
kw_model = KeyBERT("distilbert-base-nli-mean-tokens")

def medical_nlp_summarizer(transcript: str):
    doc = nlp(transcript)

    summary = {
        "Symptoms": set(),
        "Diagnosis": set(),
        "Treatment": set(),
        "Keywords": []
    }

    # --- NER Extraction ---
    for ent in doc.ents:
        if ent.label_ == "DISEASE":
            summary["Diagnosis"].add(ent.text)
        elif ent.label_ == "CHEMICAL":
            summary["Treatment"].add(ent.text)

    # --- Simple symptom heuristic ---
    symptom_keywords = ["pain", "ache", "stiffness", "discomfort"]
    for token in doc:
        if token.lemma_.lower() in symptom_keywords:
            summary["Symptoms"].add(token.text)

    # --- Keyword Extraction ---
    keywords = kw_model.extract_keywords(
        transcript,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=8
    )
    summary["Keywords"] = [k[0] for k in keywords]

    # Convert sets to lists
    for key in ["Symptoms", "Diagnosis", "Treatment"]:
        summary[key] = list(summary[key])

    return summary


# ------------------ Example Usage ------------------
text = """
Patient had a car accident and experienced neck and back pain.
Diagnosed with whiplash injury and treated with painkillers and
ten physiotherapy sessions. Currently has occasional back pain.
"""

output = medical_nlp_summarizer(text)
print(output)

