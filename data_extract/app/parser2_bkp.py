import re


def find(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        return match.group(1).strip()

    return ""


def parse_invoice(text):

    invoice = {}

    # Invoice Number
    invoice["invoice_number"] = find(
        r"Invoice\s*(?:No|Number)?[:#]?\s*([A-Za-z0-9\-\/]+)",
        text
    )

    # Invoice Date
    invoice["invoice_date"] = find(
        r"Invoice\s*Date\s*([A-Za-z]+\s+\d{1,2},\s+\d{4}|[0-9/\-.]+)",
        text
    )

    # GSTIN
    invoice["gstin"] = find(
        r"GSTIN[: ]*([A-Z0-9]+)",
        text
    )

    # PAN
    invoice["pan"] = find(
        r"PAN[: ]*([A-Z0-9]+)",
        text
    )

    # Purchase Order
    invoice["po_number"] = find(
        r"(?:PO|Order)\s*(?:No|Number)?[: ]*([A-Za-z0-9\-\/]+)",
        text
    )

    # Vendor (supports From: or Supplier:)
    invoice["vendor"] = find(
        r"(?:From|Supplier)[: ]*\n?(.+)",
        text
    )

    # Sub Total (supports "Sub Total" and "Subtotal")
    invoice["subtotal"] = find(
        r"Sub\s*Total[: ]*\$?₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    # CGST
    invoice["cgst"] = find(
        r"CGST[: ]*\$?₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    # SGST
    invoice["sgst"] = find(
        r"SGST[: ]*\$?₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    # IGST
    invoice["igst"] = find(
        r"IGST[: ]*\$?₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    # Total (supports Total Due / Total Amount / Total)
    invoice["total"] = find(
        r"Total(?:\s*Due|\s*Amount)?[: ]*\$?₹?\s*([\d,]+\.\d+|[\d,]+)",
        text
    )

    return invoice
