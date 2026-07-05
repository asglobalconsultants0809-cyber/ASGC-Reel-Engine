class TimelineEngine:
    def build(self, job_data):
        return {
            "total_duration": 36,
            "scenes": [
                {"id": "hook", "duration": 5},
                {"id": "job", "duration": 7},
                {"id": "skills", "duration": 7},
                {"id": "company", "duration": 6},
                {"id": "salary", "duration": 5},
                {"id": "cta", "duration": 6},
            ],
        }