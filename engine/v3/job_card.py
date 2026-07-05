from .utils import clean_text, limit_list


class JobCard:

    def __init__(self, job_data):
        self.job = job_data

    def build(self):
        return {
            "title": clean_text(self.job.get("job_title")),
            "company": clean_text(self.job.get("company")),
            "location": clean_text(self.job.get("location")),
            "salary": clean_text(self.job.get("salary")),
            "experience": clean_text(self.job.get("experience")),
            "skills": limit_list(self.job.get("skills"), 5),
            "cta": clean_text(self.job.get("cta")) or "Apply Now",
        }