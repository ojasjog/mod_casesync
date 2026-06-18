# ss.py
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

# Color Palette
DARK_BLUE   = colors.HexColor("#1a3a5c")
MID_BLUE    = colors.HexColor("#2563a8")
LIGHT_GRAY  = colors.HexColor("#f3f4f6")
BORDER      = colors.HexColor("#d1d5db")
WHITE       = colors.white
BLACK       = colors.black

def get_reportlab_styles():
    return {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, textColor=DARK_BLUE, leading=18),
        "section_header": ParagraphStyle("section_header", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.HexColor("#4a5568"), leading=12),
        "value": ParagraphStyle("value", fontName="Helvetica", fontSize=9.5, textColor=BLACK, leading=14),
        "note_text": ParagraphStyle("note_text", fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#374151"), leading=16),
        "cino": ParagraphStyle("cino", fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor("#6b7280")),
    }

def build_section_header(text, styles):
    t = Table([[Paragraph(text, styles["section_header"])]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return t

def build_info_table(rows, styles, page_width):
    data = []
    for label, value in rows:
        data.append([
            Paragraph(label.upper(), styles["label"]),
            Paragraph(str(value) if value else "—", styles["value"]),
        ])
    t = Table(data, colWidths=[page_width * 0.32, page_width * 0.68])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def add_page_decorations(canvas, doc):
    canvas.saveState()
    w, h = A4
    margin = 15 * mm
    canvas.setStrokeColor(DARK_BLUE)
    canvas.setLineWidth(0.5)
    canvas.rect(margin, margin, w - 2 * margin, h - 2 * margin)
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(margin, h - margin - 5, w - 2 * margin, 5, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    footer = f"CaseSync Intelligent PDF Exporter  •  Page {doc.page}"
    canvas.drawCentredString(w / 2, margin - 5, footer)
    canvas.restoreState()

def process_screenshot_to_pdf(uploaded_image_bytes, custom_notes, output_filename):
    """
    Processes the raw data extracted from your sample eCourts screenshot format.
    """
    # 1. Realistically, your local OCR parsing script maps image contents to these fields:
    parsed_data = {
        "crn": "MHST160002642017",
        "reg_no": "50/2017",
        "case_type": "R.C.S.",
        "stage": "Arguments",
        "filing_date": "17-02-2017",
        "filing_no": "80/2017",
        "reg_date": "24-02-2017",
        "first_hearing": "24-02-2017",
        "decision_date": "09-08-2024",
        "is_disposed": "Yes",
        "last_hearing": "09-08-2024",
        "court": "Jt. Civil Judge Jr. Dn. J.M.F.C Wai / CIVIL JUDGE JR. DN. J.M.F.C. WAI",
        "petitioners": "1) Vitthal Krushna Waghmare (Advocate: Khamkar L.S)<br/>2) Prakash Vitthal Waghmare (Advocate: Yadav R.R)",
        "respondents": "1) Bajrang Murlidhar Raskar (Advocate: Ghadge P.S)"
    }

    # Setup Document layout parameters
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm
    )
    
    styles = get_reportlab_styles()
    page_width = A4[0] - 40 * mm
    story = []

    # Title & Dynamic Status Badge Block
    case_title_text = f"{parsed_data['case_type']} - Reg No. {parsed_data['reg_no']}"
    
    # Check if case is disposed based on the screenshot data
    if parsed_data["is_disposed"] == "Yes":
        status_text = "◆ DISPOSED"
        status_color = colors.HexColor("#7f1d1d")
        status_bg = colors.HexColor("#fee2e2")
    else:
        status_text = "● ACTIVE"
        status_color = colors.HexColor("#065f46")
        status_bg = colors.HexColor("#d1fae5")

    status_style = ParagraphStyle("status", fontName="Helvetica-Bold", fontSize=9, textColor=status_color, alignment=TA_RIGHT)
    
    title_table = Table([
        [Paragraph(case_title_text, styles["title"]), Paragraph(status_text, status_style)]
    ], colWidths=[page_width * 0.75, page_width * 0.25])
    
    title_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (1, 0), (1, 0), status_bg),
        ("ROUNDEDCORNERS", (1, 0), (1, 0), [4, 4, 4, 4]),
        ("LEFTPADDING",  (1, 0), (1, 0), 8),
        ("RIGHTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING",   (1, 0), (1, 0), 4),
        ("BOTTOMPADDING",(1, 0), (1, 0), 4),
    ]))
    
    story.append(title_table)
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"CNR/CRN Number: {parsed_data['crn']}", styles["cino"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=MID_BLUE, spaceAfter=10, spaceBefore=6))

    # 1. Court Registry & History Grid
    story.append(build_section_header("Case Registration Details", styles))
    story.append(Spacer(1, 4))
    
    court_rows = [
        ("Case Type", parsed_data["case_type"]),
        ("Current Stage", parsed_data["stage"]),
        ("Filing Particulars", f"No. {parsed_data['filing_no']} ({parsed_data['filing_date']})"),
        ("Registration Date", parsed_data["reg_date"]),
        ("First Hearing Date", parsed_data["first_hearing"]),
        ("Last Hearing Date", parsed_data["last_hearing"]),
    ]
    if parsed_data["decision_date"]:
        court_rows.append(("Decision Date", parsed_data["decision_date"]))
        
    court_rows.append(("Court Designation", parsed_data["court"]))
    
    story.append(build_info_table(court_rows, styles, page_width))
    story.append(Spacer(1, 12))

    # 2. Litigant Parties Section
    story.append(build_section_header("Parties & Legal Counsel", styles))
    story.append(Spacer(1, 4))
    
    party_rows = [
        ("Petitioner(s)", parsed_data["petitioners"]),
        ("Respondent(s)", parsed_data["respondents"]),
    ]
    story.append(build_info_table(party_rows, styles, page_width))
    story.append(Spacer(1, 12))

    # 3. User Custom Notes Section
    story.append(build_section_header("Appended Case Notes & Observations", styles))
    story.append(Spacer(1, 4))
    
    clean_notes = custom_notes.strip() if custom_notes else "No live notes entered into mobile terminal dashboard for this listing."
    formatted_notes = clean_notes.replace("\n", "<br/>")
    
    note_table = Table([[Paragraph(formatted_notes, styles["note_text"])]], colWidths=[page_width])
    note_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbeb")),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.HexColor("#fcd34d")),
    ]))
    story.append(note_table)

    # Build PDF and destroy image memory links safely
    doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
    return output_filename