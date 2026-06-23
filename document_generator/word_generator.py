import io
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate(resume: dict) -> bytes:
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    def add_heading(text, size=11, bold=True):
        p = doc.add_paragraph()
        run = p.add_run(text.upper())
        run.bold = bold
        run.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_body(text, size=9, bold=False, italic=False):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(3)
        return p

    # --- Name + Contact ---
    name_p = doc.add_paragraph()
    name_run = name_p.add_run(resume.get("name", ""))
    name_run.bold = True
    name_run.font.size = Pt(18)
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    title_p = doc.add_paragraph()
    title_run = title_p.add_run(resume.get("title", ""))
    title_run.font.size = Pt(11)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    contact_parts = [resume.get("email",""), resume.get("phone",""), resume.get("linkedin",""), resume.get("location","")]
    contact_line = " | ".join(p for p in contact_parts if p)
    contact_p = doc.add_paragraph()
    contact_run = contact_p.add_run(contact_line)
    contact_run.font.size = Pt(9)
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # --- Summary ---
    add_heading("Summary")
    add_body(resume.get("summary", ""))
    doc.add_paragraph()

    # --- Skills ---
    skills = resume.get("skills", {})
    if skills:
        add_heading("Technical Skills")
        for category, items in skills.items():
            p = doc.add_paragraph()
            label = p.add_run(category.replace("_", " ").title() + ": ")
            label.bold = True
            label.font.size = Pt(9)
            content = p.add_run(", ".join(items))
            content.font.size = Pt(9)
            p.paragraph_format.space_after = Pt(3)
        doc.add_paragraph()

    # --- Experience ---
    experience = resume.get("experience", [])
    if experience:
        add_heading("Experience")
        for job in experience:
            title = job.get("title", "")
            company = job.get("company", "")
            client_name = job.get("client", "")
            location = job.get("location", "")
            start = job.get("start_date", "")
            end = job.get("end_date", "")

            company_line = f"{title} | {company}"
            if client_name:
                company_line += f" (Client: {client_name})"
            if location:
                company_line += f" | {location}"

            add_body(company_line, size=10, bold=True)

            if start or end:
                add_body(f"{start} - {end}", size=9, italic=True)

            context = job.get("context", "")
            if context:
                add_body(context)

            for bullet in job.get("bullets", []):
                p = doc.add_paragraph(style="List Bullet")
                run = p.add_run(bullet)
                run.font.size = Pt(9)
                p.paragraph_format.space_after = Pt(2)

            doc.add_paragraph()

    # --- Education ---
    education = resume.get("education", [])
    if education:
        add_heading("Education")
        for edu in education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            location = edu.get("location", "")
            start = edu.get("start_date", "")
            end = edu.get("end_date", "")
            gpa = edu.get("gpa", "")

            edu_line = f"{degree} | {institution}"
            if location:
                edu_line += f" | {location}"
            add_body(edu_line, bold=True)

            meta_parts = []
            if start or end:
                meta_parts.append(f"{start} - {end}".strip(" -"))
            if gpa:
                meta_parts.append(f"GPA: {gpa}")
            if meta_parts:
                add_body(" | ".join(meta_parts))
        doc.add_paragraph()

    # --- Certifications ---
    certifications = resume.get("certifications", [])
    if certifications:
        add_heading("Certifications")
        for cert in certifications:
            name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            cert_line = name
            if issuer:
                cert_line += f" | {issuer}"
            if date:
                cert_line += f" | {date}"
            add_body(f"• {cert_line}")
        doc.add_paragraph()

    # --- Projects ---
    projects = resume.get("projects", [])
    if projects:
        add_heading("Projects")
        for project in projects:
            name = project.get("name", "")
            description = project.get("description", "")
            tech = project.get("tech_stack", [])
            link = project.get("link", "")

            add_body(name, bold=True)
            if description:
                add_body(description)
            if tech:
                add_body(f"Tech: {', '.join(tech)}")
            if link:
                add_body(f"Link: {link}")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
