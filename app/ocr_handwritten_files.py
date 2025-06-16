from pdf2image import convert_from_path
import easyocr
import os
from clean_ocr_text import clean_text  # <-- Import cleaner

# === CONFIGURATION ===
PDF_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\docs\SQL Handwritten Notes .pdf"
OUTPUT_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\output\sql_notes_easyocr.txt"
OUTPUT_CLEAN_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\output\sql_notes_cleaned.txt"

POPLER_BIN = r"C:\poppler-24.08.0\Library\bin"

reader = easyocr.Reader(['en'])  # English language model

# Make sure output folder exists
os.makedirs(os.path.dirname(OUTPUT_CLEAN_PATH), exist_ok=True)

# === OCR PROCESSING ===
with open(OUTPUT_CLEAN_PATH, "w", encoding="utf-8") as f:
    for page_num in range(1, 4):  # Try 3 pages first to test
        print(f"[🔁] Page {page_num} -> Image")

        # Convert single page to image
        images = convert_from_path(PDF_PATH, poppler_path=POPLER_BIN,
                                   first_page=page_num, last_page=page_num)

        # OCR using EasyOCR
        result = reader.readtext(images[0], detail=0)
        page_text = ' '.join(result)

        # Clean the extracted text
        cleaned = clean_text(page_text)

        # Save to file
        f.write(f"\n\n--- Page {page_num} ---\n{cleaned}")
        print(f"[✅] Page {page_num} done.")

print(f"[🚀] OCR + Cleaning done! Cleaned text saved at: {OUTPUT_CLEAN_PATH}")

import os
import numpy as np
from pdf2image import convert_from_path
import cv2
import easyocr
from app.clean_ocr_text import clean_text  # Make sure this exists and is working

# === Configuration ===
PDF_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\docs\SQL Handwritten Notes .pdf"
OUTPUT_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\output\sql_notes_easyocr.txt"
OUTPUT_CLEAN_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\output\sql_notes_cleaned.txt"

POPLER_BIN = r"C:\poppler-24.08.0\Library\bin"

# === Setup ===
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you later install CUDA

os.makedirs(os.path.dirname(OUTPUT_CLEAN_PATH), exist_ok=True)

print("[🚀] Starting enhanced OCR on first page...")

# Convert only the first page to image
images = convert_from_path(PDF_PATH, poppler_path=POPLER_BIN, first_page=1, last_page=1)
image = images[0]

# Preprocess image for better OCR
def preprocess_image(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

processed_image = preprocess_image(image)

# OCR using EasyOCR
print("[🔁] Reading text using EasyOCR...")
result = reader.readtext(processed_image, detail=0)

# Join result and clean it
raw_text = "\n".join(result)
cleaned_text = clean_text(raw_text)

# Save output
with open(OUTPUT_CLEAN_PATH, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print(f"[✅] Done. Cleaned OCR output saved to:\n{OUTPUT_CLEAN_PATH}")
