import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file_path):
    img = cv2.imread(file_path)

    if img is None:
        raise ValueError(f"Image not found or cannot be read: {file_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)
    return text