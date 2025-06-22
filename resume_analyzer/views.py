'''from django.shortcuts import render
from .forms import ResumeForm
from .resume_parser import parse_resume  #  Not used now: Only for real resume file parsing
from job_matcher.matcher import suggest_jobs
from ai_generator.cover_letter import generate_cover_letter

def upload_resume(request):
    if request.method == 'POST':
        # 🔒 Not used now: Real form upload handling
         form = ResumeForm(request.POST, request.FILES)
         if form.is_valid():
           resume = form.save()
           parsed = parse_resume(resume.file.path)

        # ✅ Using MOCK data for testing without uploading resume
        #parsed = {
         #   'skills': ['Python', 'Django', 'Git', 'SQL'],
          #  'summary': 'Experienced backend developer...'
       # }

         summary = parsed.get('summary', '')
         if not summary:
            letter = "Unable to generate cover letter — summary not found in resume."
         else:
            letter = generate_cover_letter(summary)

         request.session['cover_letter_text'] = letter

         jobs = suggest_jobs(parsed['skills'])

         match_score = min(len(parsed['skills']) * 10, 100)
         if match_score < 40:
            progress_class = 'progress-red'
         elif match_score < 70:
            progress_class = 'progress-yellow'
         else:
            progress_class = 'progress-green'
            return render(request, 'result.html', {
            'skills': parsed['skills'],
            'summary': summary,
            'jobs': jobs,
            'cover_letter': letter,
            'match_score': match_score,
            'progress_class': progress_class,
        })

    # ✅ This handles the GET request (e.g., first page load)
    else:
        form = ResumeForm()
        return render(request, 'index.html', {'form': form})'''
from django.shortcuts import render
from .forms import ResumeForm
# from .resume_parser import parse_resume  # Uncomment if real parsing
from job_matcher.matcher import suggest_jobs
from ai_generator.cover_letter import generate_cover_letter

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # ✅ Optional real resume parsing (uncomment below if needed)
            # resume = form.save()
            # parsed = parse_resume(resume.file.path)

            # ✅ For now, we use mock parsed data
            parsed = {
                'skills': ['Python', 'Django', 'Git', 'SQL'],
                'summary': 'Experienced backend developer with 3+ years of experience in building scalable applications.'
            }

            summary = parsed.get('summary', '')
            jd_text = request.POST.get('job_description', '')  # ✅ ← Get the JD from form input

            # ✅ Generate cover letter (JD-aware if JD exists)
            if not summary:
                letter = "Unable to generate cover letter — summary not found in resume."
            else:
                if jd_text:
                    # JD-aware prompt for AI generation
                    prompt = f"Write a cover letter for the following job:\n\n{jd_text}\n\nResume Summary:\n{summary}"
                else:
                    prompt = summary
                letter = generate_cover_letter(prompt)

            request.session['cover_letter_text'] = letter
            jobs = suggest_jobs(parsed['skills'])

            match_score = min(len(parsed['skills']) * 10, 100)
            if match_score < 40:
                progress_class = 'progress-red'
            elif match_score < 70:
                progress_class = 'progress-yellow'
            else:
                progress_class = 'progress-green'

            return render(request, 'result.html', {
                'skills': parsed['skills'],
                'summary': summary,
                'jobs': jobs,
                'cover_letter': letter,
                'match_score': match_score,
                'progress_class': progress_class,
            })

    else:
        form = ResumeForm()
        return render(request, 'index.html', {'form': form})
