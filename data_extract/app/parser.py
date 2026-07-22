import re


def find(patterns, text):
    """
    Try multiple regex patterns until one matches.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

        if match:
            return match.group(1).strip()

    return ""


def parse_invoice(text):

    invoice = {}

    # -----------------------------
    # Invoice Number
    # -----------------------------
    invoice["invoice_number"] = find([
        r"Invoice\s*(?:No|Number)?[:#]?\s*([A-Za-z0-9\-\/]+)",
        r"Tax Invoice\s*No[:#]?\s*([A-Za-z0-9\-\/]+)",
        r"Invoice ID[:#]?\s*([A-Za-z0-9\-\/]+)",
        r"Inv(?:oice)?\s*#\s*([A-Za-z0-9\-\/]+)"
    ], text)

    # -----------------------------
    # Invoice Date
    # -----------------------------
    invoice["invoice_date"] = find([
        r"Invoice Date[: ]*([A-Za-z0-9,/\- ]+)",
        r"Date[: ]*([A-Za-z0-9,/\- ]+)",
        r"Bill Date[: ]*([A-Za-z0-9,/\- ]+)"
    ], text)

    # -----------------------------
    # GSTIN
    # -----------------------------
    invoice["gstin"] = find([
        r"GSTIN[: ]*([0-9A-Z]{15})",
        r"GST No[: ]*([0-9A-Z]{15})"
    ], text)

    # -----------------------------
    # PAN
    # -----------------------------
    invoice["pan"] = find([
        r"PAN[: ]*([A-Z]{5}[0-9]{4}[A-Z])",
        r"PAN No[: ]*([A-Z]{5}[0-9]{4}[A-Z])"
    ], text)

    # -----------------------------
    # Purchase Order
    # -----------------------------
    invoice["po_number"] = find([
        r"PO\s*Number[: ]*([A-Za-z0-9\-\/]+)",
        r"Purchase Order[: ]*([A-Za-z0-9\-\/]+)",
        r"PO[: ]*([A-Za-z0-9\-\/]+)"
    ], text)

    # -----------------------------
    # Vendor
    # -----------------------------
    invoice["vendor"] = find([
        r"From:\s*(.*?)\n",
        r"Supplier[: ]*(.*?)\n",
        r"Vendor[: ]*(.*?)\n",
        r"Sold By[: ]*(.*?)\n",
        r"Company[: ]*(.*?)\n"
    ], text)

    # -----------------------------
    # Sub Total
    # -----------------------------
    invoice["subtotal"] = find([
        r"Sub\s*Total[: ]*[$₹]?\s*([\d,]+\.\d+)",
        r"Subtotal[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    # -----------------------------
    # CGST
    # -----------------------------
    invoice["cgst"] = find([
        r"CGST[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    # -----------------------------
    # SGST
    # -----------------------------
    invoice["sgst"] = find([
        r"SGST[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    # -----------------------------
    # IGST
    # -----------------------------
    invoice["igst"] = find([
        r"IGST[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    # -----------------------------
    # Tax
    # -----------------------------
    invoice["tax"] = find([
        r"Tax[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    # -----------------------------
    # Total
    # -----------------------------
    invoice["total"] = find([
        r"Grand Total[: ]*[$₹]?\s*([\d,]+\.\d+)",
        r"Total Due[: ]*[$₹]?\s*([\d,]+\.\d+)",
        r"Amount Due[: ]*[$₹]?\s*([\d,]+\.\d+)",
        r"Total[: ]*[$₹]?\s*([\d,]+\.\d+)"
    ], text)

    return invoice
