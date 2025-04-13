from flask import Flask, request, jsonify
from langdetect import detect
from transformers import pipeline
import spacy

app = Flask(__name__)

# ✅ Health Check Route
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

# 🧠 Load NLP models once
summarizer = pipeline("summarization", model="t5-small")
translator = pipeline("translation", model="t5-small")
rephraser = pipeline("text2text-generation", model="t5-small")
nlp = spacy.load("en_core_web_sm")

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

@app.route("/process_text", methods=["POST"])
def process_text():
    data = request.get_json()
    text = data.get("text")
    tone = data.get("tone", "Professional")
    target_lang = data.get("target_lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # 🔍 Language detection
    detected_lang = detect(text)

    # 🌐 Translation
    translated = text
    if detected_lang != "en":
        translated = translator(text)[0]["translation_text"]

    # ✂️ Summarize
    summary = summarizer(translated, max_length=60, min_length=20, do_sample=False)[0]['summary_text']

    # 📝 Tone Rephrasing
    prompt = f"Rewrite this in a {tone} tone: {summary}"
    rephrased = rephraser(prompt, max_length=60)[0]["generated_text"]

    # 🏷️ Tags
    tags = extract_tags(translated)

    return jsonify({
        "original_language": detected_lang,
        "translated_input": translated,
        "summary": summary,
        "rephrased_summary": rephrased,
        "tags": tags
    })

