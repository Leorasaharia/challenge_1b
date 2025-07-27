#!/usr/bin/env python3
import glob, json, os
from datetime import datetime
from PyPDF2 import PdfReader
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

def load_model():
    # after Docker build, model lives under /app/model/flan_t5_base
    tok = AutoTokenizer.from_pretrained("model/flan_t5_base")
    base = AutoModelForSeq2SeqLM.from_pretrained("model/flan_t5_base")
    # no LoRA here unless you copy in your adapters the same way
    return tok, base

def extract_sections(tok, mdl, pages, persona, job):
    prompt = (
        f"Persona: {persona}\nJob: {job}\n\n"
        + "\n\n".join(pages)
        + "\n\nExtract top 5 and RETURN *ONLY* JSON array of objects with keys "
          "document, section_title, page_number, importance_rank."
    )
    inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=1024)
    with torch.no_grad():
        out = mdl.generate(**inputs, max_length=512, num_beams=4)
    txt = tok.decode(out[0], skip_special_tokens=True)
    try:
        return json.loads(txt)
    except:
        return []

def refine(tok, mdl, persona, job, sec, text):
    prompt = (
        f"Persona: {persona}\nJob: {job}\n"
        f"Section: {sec['section_title']} (Page {sec['page_number']})\n\n"
        f"{text}\n\n"
        "Produce ONLY a bullet-style summary."
    )
    inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=1024)
    with torch.no_grad():
        out = mdl.generate(**inputs, max_length=256, num_beams=4)
    return tok.decode(out[0], skip_special_tokens=True)

def main():
    tok, mdl = load_model()
    for inp in sorted(glob.glob("collection*/*_input.json")):
        data = json.load(open(inp))
        persona = data["persona"]["role"]
        job     = data["job_to_be_done"]["task"]

        # read pages
        pages, meta = [], []
        col = os.path.dirname(inp)
        for doc in data["documents"]:
            path = os.path.join(col,"PDFs",doc["filename"])
            reader = PdfReader(path)
            for i,p in enumerate(reader.pages,1):
                txt = p.extract_text() or ""
                pages.append(f"[{doc['filename']} – PAGE {i}]\n{txt}")
                meta.append((doc["filename"],i))

        arr = extract_sections(tok,mdl,pages,persona,job)
        final = {
            "metadata": {
                "input_documents":[d["filename"] for d in data["documents"]],
                "persona":persona,
                "job_to_be_done":job,
                "processing_timestamp":datetime.utcnow().isoformat()
            },
            "extracted_sections":[],
            "subsection_analysis":[]
        }

        for idx,s in enumerate(arr,1):
            final["extracted_sections"].append({
                "document":s.get("document",""),
                "section_title":s.get("section_title",""),
                "page_number":s.get("page_number",None),
                "importance_rank":s.get("importance_rank",idx)
            })

        for sec in final["extracted_sections"]:
            path = os.path.join(col,"PDFs",sec["document"])
            reader = PdfReader(path)
            txt=reader.pages[sec["page_number"]-1].extract_text() or ""
            summary = refine(tok,mdl,persona,job,sec,txt)
            final["subsection_analysis"].append({
                "document":sec["document"],
                "page_number":sec["page_number"],
                "refined_text":summary
            })

        out = inp.replace("_input.json","_final_output.json")
        with open(out,"w",encoding="utf-8") as f:
            json.dump(final,f,ensure_ascii=False,indent=2)
        print("Wrote", out)

if __name__=="__main__":
    main()
