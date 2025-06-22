def generate_cover_letter(summary):
    if not summary:
        return "Unable to generate cover letter — summary missing."

    # Simple mock cover letter using the parsed summary
    return f"""
Dear Hiring Manager,

I am excited to apply for a position that aligns with my background. Based on the summary below, I am confident in my ability to contribute effectively to your organization:

{summary}

I would welcome the opportunity to bring my skills and enthusiasm to your team. Thank you for considering my application.

Sincerely,  
Your Name
"""
