from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect
from transformers import pipeline
import spacy

app = FastAPI()

@app.get("/")
def health():
    return {"status": "OK"}

# Load pipelines
summarizer = pipeline("summarization", model="t5-small")
translator = pipeline("translation", model="t5-small")
rephraser = pipeline("text2text-generation", model="t5-small")
nlp = spacy.load("en_core_web_sm")

class InputPayload(BaseModel):
    text: str
    tone: str = "Professional"
    target_lang: str = "en"

def extract_tags(text):
    doc = nlp(text)
    tags = {
        "Topics": list(set([ent.text for ent in doc.ents if ent.label_ in ["ORG", "EVENT", "WORK_OF_ART"]])),
        "People": list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])),
        "Places": list(set([ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]])),
        "Tech Terms": [token.text for token in doc if token.text.lower() in ["ai", "ml", "data", "python", "cloud"]],
        "Buzzwords": [word for word in text.split() if word.lower() in ["innovation", "scalable", "synergy", "disruptive"]]
    }
    return tags

@app.post("/process_text")
def process_text(payload: InputPayload):
    original_text = payload.text

    # 🔍 Detect Language
    detected_lang = detect(original_text)

    # 🌐 Translate to English if needed
    if detected_lang != "en":
        translated = translator(original_text)[0]['translation_text']
    else:
        translated = original_text

    # 📝 Summarize
    summary = summarizer(translated, max_length=60, min_length=20, do_sample=False)[0]['summary_text']

    # ✍️ Rephrase tone
    prompt = f"Rewrite this in a {payload.tone} tone: {summary}"
    rephrased = rephraser(prompt, max_length=60)[0]['generated_text']

    # 🏷️ Tags
    tags = extract_tags(translated)

    return {
        "original_language": detected_lang,
        "translated_input": translated,
        "summary": summary,
        "rephrased_summary": rephrased,
        "tags": tags
    }
