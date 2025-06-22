def suggest_jobs(skills):
    jobs = [
        {"title": "Python Developer", "skills": ["Python", "Flask", "SQL"]},
        {"title": "Data Analyst", "skills": ["Python", "Pandas", "Excel"]},
        {"title": "Web Developer", "skills": ["HTML", "CSS", "JavaScript"]}
    ]
    def score(job):
        return len(set(job['skills']).intersection(skills))
    return sorted(jobs, key=score, reverse=True)
