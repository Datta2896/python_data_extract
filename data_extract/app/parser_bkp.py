import re


def find(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


def parse_invoice(text):

    invoice = {}

    invoice["invoice_number"] = find(
        r"Invoice\s*(?:No|Number)?[:#]?\s*([A-Za-z0-9\-\/]+)",
        text
    )

    invoice["invoice_date"] = find(
        r"Date[: ]*([0-9/\-.]+)",
        text
    )

    invoice["gstin"] = find(
        r"GSTIN[: ]*([A-Z0-9]+)",
        text
    )

    invoice["pan"] = find(
        r"PAN[: ]*([A-Z0-9]+)",
        text
    )

    invoice["po_number"] = find(
        r"PO\s*Number[: ]*([A-Za-z0-9\-\/]+)",
        text
    )

    invoice["vendor"] = find(
        r"Supplier[: ]*(.+)",
        text
    )

    invoice["subtotal"] = find(
        r"Subtotal[: ]*₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    invoice["cgst"] = find(
        r"CGST[: ]*₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    invoice["sgst"] = find(
        r"SGST[: ]*₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    invoice["igst"] = find(
        r"IGST[: ]*₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    invoice["total"] = find(
        r"Total(?: Amount)?[: ]*₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    return invoice
