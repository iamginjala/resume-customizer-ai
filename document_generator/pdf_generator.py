import io
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate(resume: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer,pagesize=LETTER,
                            topMargin = 0.5*inch,bottomMargin = 0.5*inch,
                            leftMargin=0.75*inch, rightMargin=0.75*inch)
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle("name", fontSize=18, fontName="Helvetica-Bold", spaceAfter=4)
    title_style = ParagraphStyle("title", fontSize=11, fontName="Helvetica", spaceAfter=4)
    contact_style = ParagraphStyle("contact", fontSize=9, fontName="Helvetica", spaceAfter=12)

    story = []

    # --- Name + Contact ---
    story.append(Paragraph(resume.get("name", ""), name_style))
    story.append(Paragraph(resume.get("title", ""), title_style))

    contact_parts = [resume.get("email",""), resume.get("phone",""), resume.get("linkedin",""), resume.get("location","")]
    contact_line = " | ".join(p for p in contact_parts if p)
    story.append(Paragraph(contact_line, contact_style))

    story.append(Spacer(1, 8))
    
    # --- Summary ---

    section_heading_style = ParagraphStyle("section_heading", fontSize=11, fontName="Helvetica-Bold", spaceAfter=4, textColor=colors.black)
    body_style = ParagraphStyle("body", fontSize=9, fontName="Helvetica", spaceAfter=6, leading=14)
    story.append(Paragraph("SUMMARY",section_heading_style))
    story.append(Paragraph(resume.get("summary",""),body_style))
    story.append(Spacer(1,8))

    # --- Skills ---
    story.append(Paragraph("TECHNICAL SKILLS",section_heading_style))
    skills = resume.get("skills", {})
    for category, items in skills.items():
        category_label = category.replace("_", " ").title()
        skills_line = f"<b>{category_label}:</b> {', '.join(items)}"
        story.append(Paragraph(skills_line, body_style))

    story.append(Spacer(1, 8))

    # --- Experience ---
    experience = resume.get("experience", [])
    if experience:
        story.append(Paragraph("EXPERIENCE", section_heading_style))
        for job in experience:
            title = job.get("title", "")
            company = job.get("company", "")
            client_name = job.get("client", "")
            location = job.get("location", "")
            start = job.get("start_date", "")
            end = job.get("end_date", "")

            date_line = f"{start} - {end}" if start else ""
            company_line = f"{title} | {company}"
            if client_name:
                company_line += f" (Client: {client_name})"
            if location:
                company_line += f" | {location}"

            job_title_style = ParagraphStyle("job_title", fontSize=10, fontName="Helvetica-Bold", spaceAfter=2)
            job_meta_style = ParagraphStyle("job_meta", fontSize=9, fontName="Helvetica-Oblique", spaceAfter=4)
            bullet_style = ParagraphStyle("bullet", fontSize=9, fontName="Helvetica", spaceAfter=3, leading=13, leftIndent=12, firstLineIndent=-12)

            story.append(Paragraph(company_line, job_title_style))
            if date_line:
                story.append(Paragraph(date_line, job_meta_style))

            context = job.get("context", "")
            if context:
                story.append(Paragraph(context, body_style))

            for bullet in job.get("bullets", []):
                story.append(Paragraph(f"• {bullet}", bullet_style))

            story.append(Spacer(1, 8))

    # --- Education ---
    education = resume.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", section_heading_style))
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
            story.append(Paragraph(edu_line, ParagraphStyle("edu", fontSize=9, fontName="Helvetica-Bold", spaceAfter=2)))

            meta_parts = []
            if start or end:
                meta_parts.append(f"{start} - {end}".strip(" -"))
            if gpa:
                meta_parts.append(f"GPA: {gpa}")
            if meta_parts:
                story.append(Paragraph(" | ".join(meta_parts), body_style))

        story.append(Spacer(1, 8))

    # --- Certifications ---
    certifications = resume.get("certifications", [])
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", section_heading_style))
        for cert in certifications:
            name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            cert_line = name
            if issuer:
                cert_line += f" | {issuer}"
            if date:
                cert_line += f" | {date}"
            story.append(Paragraph(f"• {cert_line}", body_style))
        story.append(Spacer(1, 8))

    # --- Projects ---
    projects = resume.get("projects", [])
    if projects:
        story.append(Paragraph("PROJECTS", section_heading_style))
        for project in projects:
            name = project.get("name", "")
            description = project.get("description", "")
            tech = project.get("tech_stack", [])
            link = project.get("link", "")

            story.append(Paragraph(f"<b>{name}</b>", body_style))
            if description:
                story.append(Paragraph(description, body_style))
            if tech:
                story.append(Paragraph(f"Tech: {', '.join(tech)}", body_style))
            if link:
                story.append(Paragraph(f"Link: {link}", body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    return buffer.getvalue()