from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services import prepare_prompts, split_invoice, process_docvqa, process_cord
from app.utils import clean_generated_text, format_cord_output

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000", "http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_invoice")
async def process_invoice(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        header_image, table_image = split_invoice(contents)

        # Header - DocVQA
        prompts = prepare_prompts()
        header_results = process_docvqa(header_image, prompts)
        cleaned_header = {k: clean_generated_text(v) for k, v in header_results.items()}

        # Table - CORD
        cord_raw = process_cord(table_image)
        table_results = format_cord_output(cord_raw)

        return JSONResponse(content={
            "Invoice_header_fields": cleaned_header,
            "Invoice_table_items": table_results
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
