# pdf_generator.py
import io
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate(resume: dict) -> bytes:
    buffer = io.BytesIO()
    
    # 0.5 inch margins all around to comfortably fit the extensive content on 2 pages
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    story = []
    
    # --- Custom Typography Styles ---
    name_style = ParagraphStyle(
        "DocName", 
        fontSize=18, 
        fontName="Helvetica-Bold", 
        leading=22, 
        spaceAfter=2, 
        alignment=0
    )
    title_style = ParagraphStyle(
        "DocTitle", 
        fontSize=11, 
        fontName="Helvetica-Bold", 
        leading=14, 
        spaceAfter=2, 
        textColor=colors.HexColor("#333333")
    )
    contact_style = ParagraphStyle(
        "DocContact", 
        fontSize=9, 
        fontName="Helvetica", 
        leading=12, 
        spaceAfter=8
    )
    
    section_heading_style = ParagraphStyle(
        "DocSectionHeading", 
        fontSize=11, 
        fontName="Helvetica-Bold", 
        leading=14, 
        spaceBefore=12, 
        spaceAfter=2, 
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        "DocBody", 
        fontSize=9.5, 
        fontName="Helvetica", 
        leading=13.5, 
        spaceAfter=4
    )
    meta_left_style = ParagraphStyle(
        "MetaLeft", 
        fontSize=10, 
        fontName="Helvetica-Bold", 
        leading=13
    )
    meta_right_style = ParagraphStyle(
        "MetaRight", 
        fontSize=10, 
        fontName="Helvetica-Bold", 
        leading=13, 
        alignment=2
    ) 
    bullet_style = ParagraphStyle(
        "DocBullet", 
        fontSize=9.5, 
        fontName="Helvetica", 
        leading=13.5, 
        leftIndent=14,      # Locks all text (lines 1, 2, etc.) perfectly to this margin
        bulletIndent=4,     # Positions the bullet character explicitly to the left of the text
        spaceAfter=3
    )

    # Helper function to inject section headers with clean full-width underlines
    def add_section_header(title):
        story.append(Paragraph(title, section_heading_style))
        story.append(HRFlowable(
            width="100%", 
            thickness=0.75, 
            color=colors.HexColor("#333333"), 
            spaceBefore=2, 
            spaceAfter=6
        ))

    # --- Header Section ---
    story.append(Paragraph(resume.get("name", ""), name_style))
    story.append(Paragraph(resume.get("title", ""), title_style))
    
    # Safely building the contact line string
    contact_parts = [resume.get("phone", ""), resume.get("email", ""), resume.get("linkedin", ""), resume.get("location", "")]
    contact_line = " | ".join(p for p in contact_parts if p)
    if contact_line:
        story.append(Paragraph(contact_line, contact_style))
    
    # --- Professional Summary ---
    if resume.get("summary"):
        summary_title = "PROFESSIONAL SUMMARY"
        add_section_header(summary_title)
        story.append(Paragraph(resume.get("summary", ""), body_style))
    
    # --- Technical Skills ---
    skills = resume.get("skills", {})
    if skills:
        add_section_header("TECHNICAL SKILLS")
        for category, items in skills.items():
            category_label = category.replace("_", " ").title()
            
            # Normalizing common labels to match expected resume layout
            if "Platform" in category_label: category_label = "Power Platform"
            elif "Alm" in category_label: category_label = "Environment & ALM Administration"
            elif "Api" in category_label: category_label = "API & Data Integration"
            
            # Handle both string values and array lists gracefully
            skills_text = ", ".join(items) if isinstance(items, list) else str(items)
            skills_line = f"<b>{category_label}:</b> {skills_text}"
            story.append(Paragraph(skills_line, body_style))

    # --- Professional Experience ---
    experience = resume.get("experience", [])
    if experience:
        add_section_header("PROFESSIONAL EXPERIENCE")
        
        for job in experience:
            title = job.get("title", "")
            company = job.get("company", "")
            client_name = job.get("client", "")
            project = job.get("project", "")
            start = job.get("start_date", "")
            end = job.get("end_date", "")
            
            # Build Metadata Title (Left Side)
            left_text = f"{company} | {title}" if company and title else (company or title)
            if client_name or project:
                extra_meta = []
                if client_name: extra_meta.append(f"Client: {client_name}")
                if project: extra_meta.append(f"Project: {project}")
                left_text += f"<br/><font fontName='Helvetica' size='9' color='#444444'>{' | '.join(extra_meta)}</font>"
            
            # Build Date Layout (Right Side)
            date_line = f"{start} - {end}" if (start and end) else f"{start}{end}"

            # Two-column layout grid to handle split strings side-by-side cleanly
            meta_table_data = [
                [Paragraph(left_text, meta_left_style), Paragraph(date_line, meta_right_style)]
            ]
            meta_table = Table(meta_table_data, colWidths=[5.5*inch, 2.0*inch])
            meta_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 2),
            ]))
            story.append(meta_table)

            # Bullet points processing
            # Bullet points processing
            for bullet in job.get("bullets", []):
                story.append(Paragraph(f"<bullet>&bull;</bullet>{bullet}", bullet_style))

    # --- Education Section ---
    education = resume.get("education", [])
    if education:
        add_section_header("EDUCATION")
        for edu in education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            start = edu.get("start_date", "")
            end = edu.get("end_date", "")
            
            edu_left = f"{degree}, {institution}" if degree and institution else (degree or institution)
            edu_right = f"{start} - {end}" if (start and end) else f"{start}{end}"
            
            edu_table_data = [
                [Paragraph(edu_left, meta_left_style), Paragraph(edu_right, meta_right_style)]
            ]
            edu_table = Table(edu_table_data, colWidths=[5.5*inch, 2.0*inch])
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('TOPPADDING', (0,0), (-1,-1), 2),
            ]))
            story.append(edu_table)

    # --- Certifications Section ---
    # --- Certifications Section ---
    certifications = resume.get("certifications", [])
    if certifications:
        add_section_header("CERTIFICATIONS")
        for cert in certifications:
            if isinstance(cert, dict):
                name = cert.get("name", "")
                issuer = cert.get("issuer", "")
                date = cert.get("date", "")
                cert_line = f"{name}" + (f" | {issuer}" if issuer else "") + (f" | {date}" if date else "")
            else:
                cert_line = str(cert)
            # Use the bullet tag here too
            story.append(Paragraph(f"<bullet>&bull;</bullet>{cert_line}", bullet_style))

    # --- Projects Section ---
    projects = resume.get("projects", [])
    if projects:
        add_section_header("PROJECTS")
        for project in projects:
            name = project.get("name", "")
            description = project.get("description", "")
            tech = project.get("tech_stack", [])
            link = project.get("link", "")

            story.append(Paragraph(f"<b>{name}</b>", body_style))
            if description:
                story.append(Paragraph(description, body_style))
            if tech:
                tech_text = ", ".join(tech) if isinstance(tech, list) else str(tech)
                story.append(Paragraph(f"Tech: {tech_text}", body_style))
            if link:
                story.append(Paragraph(f"Link: {link}", body_style))

    doc.build(story)
    return buffer.getvalue()