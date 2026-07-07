import json

_ZERO_USAGE = {"model": "mock", "input_tokens": 0, "output_tokens": 0, "cost": 0.0}

class MockJobAnalyzer:
    def analyze(self, jd: str) -> tuple[dict, dict]:
        return {"target_role": "Power Platform Developer", "keywords": ["Dataverse", "Plugins"]}, _ZERO_USAGE

class MockResumeWriter:
    def write(self, analysis: dict, selected_resume: dict, feedback: str = None) -> tuple[dict, dict]: # type: ignore
        resume = {
            "name": "Harsha Vardhan Reddy Ginjala",
            "title": "Microsoft Power Platform Developer | PowerApps | Power Automate",
            "phone": "+1-605-371-6023",
            "email": "harsha.v.ginjala@gmail.com",
            "linkedin": "linkedin.com/in/harshavardhan",
            "location": "Virginia",
            "summary": "Microsoft Power Platform Developer with 5+ years designing, developing, and deploying automation and AI-driven solutions.",
            "skills": {
                "Power Platform": ["Power Apps", "Power Automate", "Dataverse", "Power BI"],
                "API Integration": ["REST APIs", "Azure Functions", "Custom Connectors"]
            },
            "experience": [
                {
                    "company": "Geninvo",
                    "title": "Power Platform / Dynamics 365 Developer",
                    "client": "Johnson & Johnson",
                    "project": "MedSales360",
                    "start_date": "2025",
                    "end_date": "2026",
                    "bullets": [
                        "Designed and deployed a Model-Driven PowerApps on Dataverse covering Account, Contact, Opportunity, and Quote management.",
                        "Built Power Automate cloud flows for stage-change notifications and approval routing."
                    ]
                }
            ],
            "education": [
                {
                    "degree": "Master of Science - Computer Science",
                    "institution": "University of South Dakota",
                    "start_date": "Aug 2023",
                    "end_date": "Dec 2024"
                }
            ],
            "certifications": [
                "PL-200 - Microsoft Power Platform Functional Consultant",
                "MB-210 - Microsoft Dynamics 365 Sales Functional Consultant"
            ]
        }
        return resume, _ZERO_USAGE

class MockQualityChecker:
    def check(self, customized_resume: dict, analysis: dict) -> tuple[int, str, dict]:
        return 8, "Looks great!", _ZERO_USAGE

job_analyzer = MockJobAnalyzer()
resume_writer = MockResumeWriter()
quality_checker = MockQualityChecker()