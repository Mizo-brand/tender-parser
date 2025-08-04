from fastapi import FastAPI
from pydantic import BaseModel
import fitz  # PyMuPDF
import requests
from io import BytesIO

app = FastAPI()

class LotRequest(BaseModel):
    pdf_url: str

@app.post("/extract")
def extract_text_from_pdf(data: LotRequest):
    try:
        response = requests.get(data.pdf_url)
        pdf_data = BytesIO(response.content)
        doc = fitz.open(stream=pdf_data, filetype="pdf")

        all_text = []
        for page in doc:
            text = page.get_text()
            all_text.append(text.strip())

        full_text = "\n".join(all_text).strip()

        keywords = ["поставка", "объем", "характеристика", "количество", "единиц", "наименование"]
        important_lines = [
            line for line in full_text.splitlines()
            if any(k.lower() in line.lower() for k in keywords)
        ]

        result = "\n".join(important_lines[:30])
        return {"status": "ok", "text": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
