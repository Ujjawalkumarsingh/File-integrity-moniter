
import os
import json
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def save_reports(data):
    os.makedirs("reports", exist_ok=True)

    # JSON report
    with open(
        "reports/report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(data, file, indent=4)

    # PDF report
    document = SimpleDocTemplate(
        "reports/report.pdf",
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(
        "FILE INTEGRITY MONITORING REPORT",
        styles["Title"]
    ))

    content.append(Spacer(1, 15))

    content.append(Paragraph(
        "Directory: " + escape(str(data["directory"])),
        styles["Normal"]
    ))

    content.append(Paragraph(
        "Scan time: " + escape(str(data["timestamp"])),
        styles["Normal"]
    ))

    content.append(Spacer(1, 20))

    summary = [
        ["Event", "Count"],
        ["Created", len(data["created"])],
        ["Modified", len(data["modified"])],
        ["Deleted", len(data["deleted"])]
    ]

    table = Table(summary, colWidths=[200, 100])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    for category in ("created", "modified", "deleted"):
        content.append(Paragraph(
            category.title() + " Files",
            styles["Heading2"]
        ))

        files = data[category]

        if not files:
            content.append(Paragraph(
                "No files detected.",
                styles["Normal"]
            ))

        for filename in files:
            content.append(Paragraph(
                escape(str(filename)),
                styles["Normal"]
            ))

        content.append(Spacer(1, 12))

    document.build(content)

    print("[+] JSON report generated")
    print("[+] PDF report generated")
