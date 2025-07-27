## Round 1B: Persona-Driven Document Intelligence

**Theme:** “Connect What Matters — For the User Who Matters”

---

### 📖 Overview

In **Round 1B** of the Adobe Hackathon, we build a **CPU-only**, **offline** service that:

1. **Ingests** a small collection of PDFs (3–10 per “collection”).
2. **Extracts** the top 5 most relevant sections across those PDFs for a given persona and task.
3. **Ranks** them by importance.
4. **Summarizes** each chosen section in concise, bullet-style form.
5. **Emits** a clean, structured JSON (`challenge1b_final_output.json`) per collection.

All processing must complete in under 60 seconds for 3–5 small documents and the model footprint must stay below 1 GB.

---

### 🔍 Challenge Brief

* **Input**

  * **Document Collection**: 3–10 related PDFs
  * **Persona**: A role with domain expertise
  * **Job-to-be-Done**: A concrete task the persona must accomplish

* **Output**
  A JSON with:

  1. **metadata**

     * `input_documents`: list of filenames
     * `persona`
     * `job_to_be_done`
     * `processing_timestamp`
  2. **extracted\_sections** (top 5)

     * `document`, `page_number`, `section_title`, `importance_rank`
  3. **subsection\_analysis**

     * For each extracted section: `document`, `page_number`, `refined_text`

---

### ⚙️ Project Structure

```
challenge_1b/
├── collection1/
│   ├── PDFs/
│   │   └── South of France – … .pdf
│   └── challenge1b_input.json
├── collection2/
│   ├── PDFs/
│   │   └── Learn Acrobat – … .pdf
│   └── challenge1b_input.json
├── collection3/
│   ├── PDFs/
│   │   └── Dinner Ideas – … .pdf
│   └── challenge1b_input.json
├── model #folder containing the model and its dependencies 
├── Challenge_1b_final_flan_t5_base.ipynb
├── Challenge_1b_final_flan_t5_base_clean.ipynb
├── Dockerfile
├── README.md
├── requirements.txt
├── download_flan_t5_base.py     # fetches Flan-T5 at build time
└── run_inference.py             # main inference script
```

---

### ⚙️ Prerequisites

* **Local**

  * Python 3.10+
  * pip
  * Docker (for container builds & offline runs)

* **No GPU required** – everything runs on CPU.

---

### 🛠️ Local Setup & Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/Leorasaharia/challenge_1b.git
   cd challenge_1b
   ```

2. **Install dependencies**

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. **(One-time) Download Flan-T5 model**

   ```bash
   python download_flan_t5_base.py
   ```

   > Populates `model/flan_t5_base/` with tokenizer & weights.

4. **Run the inference**

   ```bash
   python run_inference.py
   ```

   This will process **collection1**, **collection2**, and **collection3**, writing
   `challenge1b_final_output.json` in each folder.

---

### 🐳 Docker Build & Run

1. **Build the container**

   ```bash
   docker build -t doc-analyst:latest .
   ```
2. **Run offline**

   ```bash
   docker run --rm --network none doc-analyst:latest
   ```

   * Reads `collection*/challenge1b_input.json`
   * Writes each `collection*/challenge1b_final_output.json`

---

### 📦 Deliverables

* **approach\_explanation.md**
  300–500 words on methodology, design choices, and performance considerations.

* **Dockerfile** & **execution instructions** (this README).

* **Sample input/output** under each `collection*/`.

---

### 🎯 Sample Test Cases

1. **Academic Research**

   * 4 research papers on “Graph Neural Networks for Drug Discovery”
   * Persona: PhD Researcher, Computational Biology
   * Job: “Comprehensive literature review focusing on methodologies, datasets, performance benchmarks”

2. **Business Analysis**

   * 3 annual reports (2022–2024)
   * Persona: Investment Analyst
   * Job: “Analyze revenue trends, R\&D investments, market positioning”

3. **Educational Content**

   * 5 textbook chapters on Organic Chemistry
   * Persona: Undergraduate Student
   * Job: “Identify key concepts & mechanisms for reaction kinetics exam prep”

---

### 📝 Sample Output Snippet

```jsonc
{
  "metadata": {
    "input_documents": [
      "South of France - Cities.pdf",
      "... other guides ..."
    ],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-27T10:15:22.123456"
  },
  "extracted_sections": [
    {
      "document": "South of France - Cities.pdf",
      "section_title": "Comprehensive Guide to Major Cities…",
      "page_number": 1,
      "importance_rank": 1
    },
    /* top 5 entries */
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cities.pdf",
      "page_number": 1,
      "refined_text": "- Nice: Promenade des Anglais; - Antibes: Charming old town; …"
    },
    /* one bullet summary per extracted section */
  ]
}
```

---

### 🔑 Key Features

* **Persona-driven**: tailor extraction & summaries to the user’s role & task.
* **Section ranking**: pick and order the 5 most relevant segments.
* **Concise summaries**: bullet-style refined text.
* **CPU-only**: no GPU dependencies.
* **Offline**: fully self-contained Docker image.

---

**GitHub:** [https://github.com/Leorasaharia/challenge\_1b](https://github.com/Leorasaharia/challenge_1b)

---

© 2025 Leora Saharia. Swara Mandale. Adya Singh
