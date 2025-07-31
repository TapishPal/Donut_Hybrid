import re

def clean_generated_text(text: str, processor=None) -> str:
    text = re.sub(r"<s_docvqa><s_question>.*?</s_question>", "", text)
    return text.replace("<s_answer>", "").replace("</s_answer>", "").strip()

def format_cord_output(raw):
    menu = raw.get("menu", [])
    items = []
    for item in menu[1:]:  # skip header
        desc = item.get("nm", "").strip()
        qty = item.get("cnt", "").strip()
        price = item.get("price", "").strip()
        sub = item.get("sub", {}).get("nm", "").strip()

        items.append({
            "description": desc,
            "sub_headings": [sub] if sub else [],
            "quantity": qty,
            "price": price
        })

    total_block = raw.get("total", {})
    total_price = total_block.get("creditcardprice") or total_block.get("total_price")

    return {
        "items": items,
        "total": total_price
    }
