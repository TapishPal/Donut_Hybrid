from app.model import load_docvqa_model, load_cord_model
from app.config import FIELDS, DEVICE
import cv2
import torch
from PIL import Image
import numpy as np

docvqa_processor, docvqa_model = load_docvqa_model()
cord_processor, cord_model = load_cord_model()

def prepare_prompts():
    return {
        field: f"<s_docvqa><s_question>{q}</s_question><s_answer>"
        for field, q in FIELDS.items()
    }

def process_docvqa(image, prompts):
    pixel_values = docvqa_processor(image, return_tensors="pt").pixel_values.to(DEVICE)
    results = {}
    for field, prompt in prompts.items():
        decoder_input = docvqa_processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids.to(DEVICE)
        with torch.no_grad():
            outputs = docvqa_model.generate(
                pixel_values,
                decoder_input_ids=decoder_input,
                max_length=512,
                pad_token_id=docvqa_processor.tokenizer.pad_token_id,
                eos_token_id=docvqa_processor.tokenizer.eos_token_id,
                return_dict_in_generate=True
            )
        sequence = docvqa_processor.batch_decode(outputs.sequences)[0]
        results[field] = sequence
    return results

def process_cord(image):
    pixel_values = cord_processor(image, return_tensors="pt").pixel_values.to(DEVICE)
    decoder_input = cord_processor.tokenizer("<s_cord-v2>", add_special_tokens=False, return_tensors="pt").input_ids.to(DEVICE)

    with torch.no_grad():
        outputs = cord_model.generate(
            pixel_values,
            decoder_input_ids=decoder_input,
            max_length=1024,
            pad_token_id=cord_processor.tokenizer.pad_token_id,
            eos_token_id=cord_processor.tokenizer.eos_token_id,
            return_dict_in_generate=True
        )
    sequence = cord_processor.batch_decode(outputs.sequences)[0]
    return cord_processor.token2json(sequence)

def split_invoice(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]

    header_candidates = []
    table_candidates = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h < 10 or w < 50:
            continue
        if y < height * 0.5:
            header_candidates.append((x, y, w, h))
        else:
            table_candidates.append((x, y, w, h))

    # Header
    x_min = min([x for x, y, w, h in header_candidates])
    y_min = min([y for x, y, w, h in header_candidates])
    x_max = width
    y_max = max([y + h for x, y, w, h in header_candidates])
    header_img = img[y_min:y_max, x_min:x_max]
    header_pil = Image.fromarray(cv2.cvtColor(header_img, cv2.COLOR_BGR2RGB))

    # Table
    x_min = min([x for x, y, w, h in table_candidates])
    y_min = min([y for x, y, w, h in table_candidates])
    x_max = max([x + w for x, y, w, h in table_candidates])
    y_max = max([y + h for x, y, w, h in table_candidates])
    table_img = img[y_min:y_max, x_min:x_max]
    table_pil = Image.fromarray(cv2.cvtColor(table_img, cv2.COLOR_BGR2RGB))

    return header_pil, table_pil
