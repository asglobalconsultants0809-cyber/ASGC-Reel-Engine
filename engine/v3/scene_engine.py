class SceneEngine:

    def __init__(self):
        self.default_duration = 5

    def build(self, job):

        return [

            {
                "scene": 1,
                "duration": 5,
                "title": job.get("hook", "Hiring Now"),
                "background": "office_entrance",
            },

            {
                "scene": 2,
                "duration": 6,
                "title": job.get("job_title", ""),
                "background": "workstation",
            },

            {
                "scene": 3,
                "duration": 6,
                "title": "Required Skills",
                "background": "team_meeting",
            },

            {
                "scene": 4,
                "duration": 6,
                "title": job.get("company", ""),
                "background": "office_workspace",
            },

            {
                "scene": 5,
                "duration": 6,
                "title": "Apply Today",
                "background": "happy_employees",
            },

            {
                "scene": 6,
                "duration": 6,
                "title": job.get("cta", "Apply Now"),
                "background": "company_logo",
            }

        ]