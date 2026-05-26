#!/usr/bin/env python3
"""
Generate slides/HealthcareDemo-Overview.pdf — a four-page branded overview
of the demo for stakeholders and pre-reads.

Requirements (not part of backend runtime — install on demand):
    pip install reportlab

Run from the project root:
    source backend/.venv/bin/activate
    python scripts/generate_overview_pdf.py
"""

import os
import sys
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak,
)

# ─── MongoDB brand palette (mirrors frontend/src/index.css) ────────────
SLATE_BLUE   = HexColor("#001E2B")
SURFACE      = HexColor("#112A37")
SURFACE_SUNK = HexColor("#0A1F2A")
BORDER       = HexColor("#1F3947")
MIST         = HexColor("#E3FCF7")
SPRING_GREEN = HexColor("#00ED64")
FOREST_GREEN = HexColor("#00684A")
TEXT_MUTED   = HexColor("#A4B5BC")
TEXT_FAINT   = HexColor("#6F8189")


# ─── Output path ──────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.normpath(os.path.join(HERE, "..", "slides",
                                         "HealthcareDemo-Overview.pdf"))


def _draw_leaf(canvas, x, y, height=12.0):
    """Draw a simplified MongoDB leaf glyph in Spring Green at (x, y) with
    the given height. Uses a teardrop/leaf path that reads as the MongoDB
    leaf without needing the full SVG (which conflicts with platypus state)."""
    w = height * 0.45  # leaf aspect ratio
    canvas.saveState()
    canvas.setFillColor(SPRING_GREEN)
    canvas.setStrokeColor(SPRING_GREEN)
    p = canvas.beginPath()
    # Teardrop: pointed at top, rounded at bottom
    cx = x + w / 2
    p.moveTo(cx, y + height)                            # top tip
    p.curveTo(x + w, y + height * 0.85,
              x + w, y + height * 0.35,
              cx, y)                                     # right side down to base
    p.curveTo(x, y + height * 0.35,
              x, y + height * 0.85,
              cx, y + height)                            # left side back to tip
    p.close()
    canvas.drawPath(p, fill=1, stroke=0)
    # Subtle midline rib (slightly darker green)
    canvas.setStrokeColor(FOREST_GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(cx, y + 0.5, cx, y + height - 0.5)
    canvas.restoreState()


# ─── Typography ───────────────────────────────────────────────────────
def styles():
    eyebrow = ParagraphStyle(
        "eyebrow", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=SPRING_GREEN, spaceAfter=6,
    )
    h1 = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=26, leading=30,
        textColor=MIST, spaceAfter=14,
    )
    h2 = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=15, leading=19,
        textColor=SPRING_GREEN, spaceBefore=14, spaceAfter=8,
    )
    body = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=MIST, spaceAfter=8,
    )
    muted = ParagraphStyle(
        "muted", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=TEXT_MUTED, spaceAfter=6,
    )
    bullet = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=10, leading=14,
        textColor=MIST, leftIndent=14, bulletIndent=4, spaceAfter=4,
    )
    code = ParagraphStyle(
        "code", fontName="Courier-Bold", fontSize=10, leading=14,
        textColor=SPRING_GREEN,
    )
    scenario_h = ParagraphStyle(
        "scen_h", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=SPRING_GREEN, spaceAfter=4,
    )
    scenario_body = ParagraphStyle(
        "scen_b", fontName="Helvetica", fontSize=9, leading=12,
        textColor=MIST, spaceAfter=4,
    )
    scenario_label = ParagraphStyle(
        "scen_l", fontName="Helvetica-Bold", fontSize=8, leading=10,
        textColor=TEXT_FAINT, spaceAfter=1,
    )
    return {
        "eyebrow": eyebrow, "h1": h1, "h2": h2, "body": body, "muted": muted,
        "bullet": bullet, "code": code,
        "scen_h": scenario_h, "scen_b": scenario_body, "scen_l": scenario_label,
    }


# ─── Page chrome (background + brand bar + footer) ────────────────────
def draw_background(canvas, doc):
    canvas.saveState()
    # Full-page slate
    canvas.setFillColor(SLATE_BLUE)
    canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
    # Spring-green top bar
    canvas.setFillColor(SPRING_GREEN)
    canvas.rect(0, letter[1] - 0.18 * inch, letter[0], 0.06 * inch,
                stroke=0, fill=1)
    # Brand: small leaf glyph + "MongoDB" wordmark in Spring Green,
    # with the doc-section breadcrumb to its right in muted text.
    header_baseline_y = letter[1] - 0.45 * inch
    _draw_leaf(canvas, 0.6 * inch, header_baseline_y - 1, height=11.0)
    canvas.setFillColor(SPRING_GREEN)
    canvas.setFont("Helvetica-Bold", 10)
    wordmark_x = 0.6 * inch + 11.0 * 0.45 + 5
    canvas.drawString(wordmark_x, header_baseline_y, "MongoDB")
    wordmark_width = canvas.stringWidth("MongoDB", "Helvetica-Bold", 10)
    canvas.setFillColor(TEXT_FAINT)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(wordmark_x + wordmark_width + 8, header_baseline_y,
                      "·  Healthcare AI Demo  ·  Overview")
    # Footer
    canvas.setFillColor(TEXT_FAINT)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.6 * inch, 0.5 * inch,
                      "Atlas  ·  Voyage AI  ·  Vector Search  ·  $rankFusion")
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.5 * inch,
                           f"Page {doc.page} of 4")
    canvas.restoreState()


# ─── Helpers for laying out tables ────────────────────────────────────
def step_flow_table(s):
    head_row = [
        Paragraph("<b>Step</b>", s["scen_l"]),
        Paragraph("<b>What happens</b>", s["scen_l"]),
        Paragraph("<b>MongoDB role</b>", s["scen_l"]),
    ]
    rows = [
        ("1", "Operational claim record loads — structured fields plus "
              "unstructured clinical notes.",
              "Operational database — the source of record."),
        ("2", "Voyage AI embeds the clinical notes into a 1024-dim vector "
              "(voyage-3) and writes it into the same document.",
              "Vector lives next to the data it describes — no separate store."),
        ("3", "Atlas Vector Search retrieves semantically relevant policies "
              "and prior cases, with operational filters enforced.",
              "$vectorSearch aggregation stage with hard filter clauses."),
        ("4", "Hybrid retrieval (optional): same query through $vectorSearch "
              "and $search, fused by $rankFusion.",
              "Single platform handles both retrieval styles natively."),
        ("5", "Reviewer-voice rationale generated from retrieved context "
              "and written back into the claim record.",
              "AI output stored in the same document as the operational data."),
    ]
    data = [head_row]
    for n, what, role in rows:
        data.append([
            Paragraph(n, s["scen_h"]),
            Paragraph(what, s["scen_b"]),
            Paragraph(role, s["scen_b"]),
        ])
    t = Table(data, colWidths=[0.6 * inch, 3.4 * inch, 2.8 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), SURFACE),
        ("BACKGROUND", (0, 1), (-1, -1), SURFACE_SUNK),
        ("LINEBELOW", (0, 0), (-1, 0), 1, SPRING_GREEN),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SURFACE_SUNK, SURFACE]),
    ]))
    return t


def scenario_column(s, letter_, title, member, pend, focus, outcome):
    return [
        Paragraph(f"Scenario {letter_}", s["eyebrow"]),
        Paragraph(title, s["scen_h"]),
        Spacer(1, 4),
        Paragraph("Member", s["scen_l"]),
        Paragraph(member, s["scen_b"]),
        Paragraph("Pend reason", s["scen_l"]),
        Paragraph(pend, s["scen_b"]),
        Paragraph("Clinical focus", s["scen_l"]),
        Paragraph(focus, s["scen_b"]),
        Paragraph("Expected outcome", s["scen_l"]),
        Paragraph(outcome, s["scen_b"]),
    ]


def scenarios_table(s):
    a = scenario_column(
        s, "A", "MRI Prior Authorization · CPT 72148",
        "James Thornton · 58 M · PPO · OH",
        "PA-MN-001 — medical-necessity review",
        "Lumbar radiculopathy with conservative treatment history; imaging request.",
        "<b>APPROVE</b> — conservative therapy documented, criteria met.",
    )
    b = scenario_column(
        s, "B", "Specialty Drug Infusion · HCPCS J1745 (Remicade)",
        "Eleanor K. Vasquez · 44 F · PPO · TX",
        "MN-DRUG-HCB-002 — high-cost biologic",
        "Seropositive RA on infliximab; step-therapy review for $18,420 claim.",
        "<b>APPROVE</b> — step therapy thoroughly documented.",
    )
    c = scenario_column(
        s, "C", "GLP-1 Prior Authorization · HCPCS S0148 (Wegovy)",
        "Patricia A. Reeves · 52 F · PPO · FL",
        "PA-OBE-GLP1-001 — lifestyle program docs",
        "Morbid obesity (BMI 38.2) with T2DM, HTN, OSA; lifestyle documentation gap.",
        "<b>ADDITIONAL INFORMATION REQUIRED</b> — qualifies but documentation incomplete.",
    )
    data = [[a, b, c]]
    t = Table(data, colWidths=[2.27 * inch] * 3, spaceBefore=0)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("BACKGROUND", (0, 0), (-1, -1), SURFACE_SUNK),
        ("LINEBEFORE", (1, 0), (-1, -1), 0.5, BORDER),
        ("LINEABOVE", (0, 0), (-1, 0), 1, SPRING_GREEN),
    ]))
    return t


# ─── Page builders ────────────────────────────────────────────────────
def page_title(s):
    return [
        Spacer(1, 0.4 * inch),
        Paragraph("MONGODB ATLAS  ·  HEALTHCARE AI DEMO", s["eyebrow"]),
        Paragraph("Operational data and AI retrieval, one platform.", s["h1"]),
        Spacer(1, 0.1 * inch),
        Paragraph(
            "This demo walks a single synthetic pended healthcare claim through a "
            "five-step AI-enrichment loop entirely inside MongoDB Atlas — clinical "
            "embeddings, Atlas Vector Search retrieval, hybrid search via "
            "<font name='Courier-Bold' color='#00ED64'>$rankFusion</font>, and an "
            "AI-generated reviewer rationale — all anchored in the same documents "
            "that hold the operational claim data.",
            s["body"],
        ),
        Paragraph(
            "The architectural thesis is simple: MongoDB Atlas serves as both the "
            "operational system of record and the retrieval foundation for AI "
            "workloads. Embeddings live alongside the data they describe; vector "
            "and lexical retrieval run as aggregation stages on the same "
            "collection; AI output is written back into the original record. No "
            "separate vector store, no sync layer, no glue code keeping two "
            "systems consistent.",
            s["body"],
        ),
        Spacer(1, 0.15 * inch),
        Paragraph("At a glance", s["h2"]),
        Paragraph(
            "•  Three engineered scenarios: MRI prior auth, biologic infusion, "
            "GLP-1 weight management.", s["bullet"]),
        Paragraph(
            "•  30 coverage policies and 71 prior adjudicated claims, all "
            "embedded with Voyage AI <font name='Courier-Bold' color='#00ED64'>voyage-3</font> "
            "(1024 dimensions).", s["bullet"]),
        Paragraph(
            "•  <font name='Courier-Bold' color='#00ED64'>$vectorSearch</font> and "
            "<font name='Courier-Bold' color='#00ED64'>$search</font> indexes "
            "live on the same collections; <font name='Courier-Bold' color='#00ED64'>$rankFusion</font> "
            "fuses them in one aggregation stage.", s["bullet"]),
        Paragraph(
            "•  Template-driven rationale — no external LLM API call required.",
            s["bullet"]),
        Paragraph(
            "•  Hard operational filters (plan type, state, outcome) are enforced "
            "as constraints, not hints, in both vector and lexical pipelines.",
            s["bullet"]),
    ]


def page_flow(s):
    return [
        Paragraph("THE FIVE-STEP FLOW", s["eyebrow"]),
        Paragraph("From pended claim to written-back rationale.", s["h1"]),
        Paragraph(
            "Every step happens inside MongoDB Atlas. The clinical notes are "
            "embedded once and stored in the same document. Both retrieval stages "
            "are MongoDB aggregation operators. The AI rationale is written back "
            "into the original claim record, preserving a clean audit trail.",
            s["body"],
        ),
        Spacer(1, 0.15 * inch),
        step_flow_table(s),
    ]


def page_scenarios(s):
    return [
        Paragraph("THREE ENGINEERED SCENARIOS", s["eyebrow"]),
        Paragraph("Same architecture, three clinical situations.", s["h1"]),
        Paragraph(
            "Each scenario exercises the same five-step flow against different "
            "clinical content, plan type, and pend reason. Scenario B is the "
            "intended showcase for hybrid retrieval — the Crohn's contrast case "
            "<font name='Courier-Bold' color='#00ED64'>PCL-2024-BIO-3580</font> "
            "is engineered to surface in hybrid mode but not in pure "
            "<font name='Courier-Bold' color='#00ED64'>$vectorSearch</font>.",
            s["body"],
        ),
        Spacer(1, 0.15 * inch),
        scenarios_table(s),
    ]


def page_distinctive(s):
    return [
        Paragraph("WHY THIS ARCHITECTURE", s["eyebrow"]),
        Paragraph("What is distinctive about MongoDB Atlas here.", s["h1"]),

        Paragraph("One platform for operational and AI workloads", s["h2"]),
        Paragraph(
            "Operational claim data, Voyage AI embeddings, retrieval indexes, "
            "and AI output all live in the same Atlas cluster — anchored to the "
            "same documents. No separate vector database to keep in sync, no "
            "data movement to support retrieval.",
            s["body"],
        ),

        Paragraph("Hybrid retrieval, natively", s["h2"]),
        Paragraph(
            "<font name='Courier-Bold' color='#00ED64'>$rankFusion</font> "
            "(MongoDB 8.1+) combines a "
            "<font name='Courier-Bold' color='#00ED64'>$vectorSearch</font> "
            "pipeline and a "
            "<font name='Courier-Bold' color='#00ED64'>$search</font> (lexical) "
            "pipeline in a single aggregation stage with reciprocal rank fusion. "
            "The same hard filters apply to both pipelines, so the comparison "
            "stays operationally honest.",
            s["body"],
        ),

        Paragraph("Hard filters on semantic retrieval", s["h2"]),
        Paragraph(
            "Plan type, member state, and adjudication outcome are enforced as "
            "filters inside the search stage — they are constraints on the "
            "results, not hints to a model. This is the difference between "
            "useful semantic search and unguarded semantic search in a regulated "
            "healthcare context.",
            s["body"],
        ),

        Paragraph("AI output written back to the record", s["h2"]),
        Paragraph(
            "Step 5 stores the generated rationale, supporting policy IDs, "
            "comparable case IDs, and a status-history entry on the original "
            "claim document. Auditability is built in — no separate output "
            "store, no ID reconciliation between systems.",
            s["body"],
        ),
    ]


def build():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    doc = BaseDocTemplate(
        OUT_PATH, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.85 * inch, bottomMargin=0.75 * inch,
        title="Healthcare AI Demo — Overview",
        author="MongoDB",
        subject="MongoDB Atlas Healthcare AI Demo — Overview",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="content", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="dark", frames=[frame], onPage=draw_background),
    ])

    s = styles()
    story = []
    story.extend(page_title(s))
    story.append(PageBreak())
    story.extend(page_flow(s))
    story.append(PageBreak())
    story.extend(page_scenarios(s))
    story.append(PageBreak())
    story.extend(page_distinctive(s))

    doc.build(story)
    return OUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
    sys.exit(0)
