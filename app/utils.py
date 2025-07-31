import re

def clean_generated_text(text: str, processor=None) -> str:
    text = re.sub(r"<s_docvqa><s_question>.*?</s_question>", "", text)
    return text.replace("<s_answer>", "").replace("</s_answer>", "").replace("</s>", "").strip()

def format_cord_output(cord_output_raw):
    # If input is a list, take first element
    if isinstance(cord_output_raw, list):
        cord_output_raw = cord_output_raw[0] if cord_output_raw else {}

    menu = cord_output_raw.get("menu", [])
    items = []

    if isinstance(menu, list) and len(menu) > 1:
        header = menu[0]  # Get header row to infer column indices

        for row in menu[1:]:
            if isinstance(row, dict):
                # Expected format
                desc = row.get("nm", "").strip()
                qty = row.get("cnt", "").strip()
                price = row.get("price", "").strip()
                sub = row.get("sub", {}).get("nm", "").strip()
            elif isinstance(row, list):
                # Handle row as list using index
                try:
                    desc = str(row[1]).strip() if len(row) > 1 else ""
                    qty = str(row[2]).strip() if len(row) > 2 else ""
                    price = str(row[3]).strip() if len(row) > 3 else ""
                    sub = ""
                except Exception as e:
                    print("⚠️ Error parsing list row:", row, e)
                    continue
            else:
                continue

            items.append({
                "description": desc,
                "sub_headings": [sub] if sub else [],
                "quantity": qty,
                "price": price
            })
    elif isinstance(menu, dict):
        # Fallback: single row
        desc = menu.get("nm", "").strip()
        qty = menu.get("cnt", "").strip()
        price = menu.get("price", "").strip()
        sub = menu.get("sub", {}).get("nm", "").strip()

        items.append({
            "description": desc,
            "sub_headings": [sub] if sub else [],
            "quantity": qty,
            "price": price
        })
    else:
        print("CORD output is empty or malformed.")

    total_block = cord_output_raw.get("total", {})
    total_price = total_block.get("creditcardprice") or total_block.get("total_price")

    return {
        "items": items,
        "total": total_price
    }
