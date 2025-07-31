from transformers import DonutProcessor, VisionEncoderDecoderModel
from app.config import DOCVQA_MODEL, CORD_MODEL, DEVICE

def load_docvqa_model():
    processor = DonutProcessor.from_pretrained(DOCVQA_MODEL)
    model = VisionEncoderDecoderModel.from_pretrained(DOCVQA_MODEL).to(DEVICE)
    return processor, model

def load_cord_model():
    processor = DonutProcessor.from_pretrained(CORD_MODEL)
    model = VisionEncoderDecoderModel.from_pretrained(CORD_MODEL).to(DEVICE)
    return processor, model
