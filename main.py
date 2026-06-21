from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile, os
from extractor import extract_pdf
from ai_parser import parse_with_ai
from jats_builder import build_jats

app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"])
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detail": traceback.format_exc()},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.get("/")
def root():
    return {"status": "PDF to JATS backend is running"}

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        extracted = extract_pdf(tmp_path)
        structured = parse_with_ai(extracted["full_text"])
        return JSONResponse({"status": "ok", "data": structured})
    finally:
        os.unlink(tmp_path)

@app.post("/generate")
async def generate_xml(payload: dict):
    xml_str = build_jats(payload)
    return JSONResponse({"xml": xml_str})