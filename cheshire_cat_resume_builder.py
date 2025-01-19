from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from jinja2 import Template
import os

from cat.plugins.super_cat_form.super_cat_form import SuperCatForm, super_cat_form, form_tool



class Education(BaseModel):
    institution: str = Field(description="Name of educational institution")
    degree: str = Field(description="Degree obtained or pursued")
    field: str = Field(description="Field of study")
    start_date: date = Field(description="Start date of education")
    end_date: Optional[date] = Field(description="End date of education (leave empty if current)")
    gpa: Optional[float] = Field(description="GPA if applicable")
    highlights: List[str] = Field(default_factory=list, description="Key achievements during education")

class Experience(BaseModel):
    company: str = Field(description="Company name")
    position: str = Field(description="Job title")
    location: str = Field(description="Job location")
    start_date: date = Field(description="Start date of employment")
    end_date: Optional[date] = Field(description="End date of employment (leave empty if current)")
    description: List[str] = Field(description="Bullet points describing responsibilities and achievements")

class Skill(BaseModel):
    category: str = Field(description="Skill category (e.g., Programming, Languages)")
    items: List[str] = Field(description="List of skills in this category")

class Resume(BaseModel):
    full_name: str = Field(description="Full name")
    title: str = Field(description="Professional title")
    email: str = Field(description="Professional email address")
    phone: str = Field(description="Contact phone number")
    location: str = Field(description="City, State/Country")
    summary: str = Field(description="Professional summary")
    experience: List[Experience] = Field(description="Work experience")
    education: List[Education] = Field(description="Educational background")
    skills: List[Skill] = Field(description="Skills grouped by category")

@super_cat_form
class ResumeForm(SuperCatForm):
    description = "Professional Resume Builder"
    model_class = Resume
    start_examples = ["help me build my resume", "create a resume"]
    stop_examples = ["cancel resume", "stop building resume"]
    ask_confirm = True

    @form_tool(return_direct=True)
    def improve_job_description(self, description: str) -> str:
        """
        Enhances job descriptions with strong action verbs and quantifiable achievements.
        Input is the current job description that needs improvement.
        """
        # Simulate AI enhancement of job descriptions
        return f"Enhanced version of your job description focusing on achievements and metrics:\n{description}"

    @form_tool(return_direct=True)
    def suggest_skills(self, job_title: str) -> str:
        """
        Suggests relevant skills based on job title.
        Input is the job title to get skill suggestions for.
        """
        # Simulate AI skill suggestions
        return f"Recommended skills for {job_title}:\n[skill suggestions would appear here]"

    @form_tool(return_direct=True)
    def write_summary(self, experience: str) -> str:
        """
        Helps craft a professional summary based on experience.
        Input is a brief description of professional experience.
        """
        self.form_data["summary"] = self.cat.llm(f"Write a first-person professional summary based on the following experience: {self.form_data}")
        return self.form_data

    def submit(self, form_data):
        form_result = self.form_data_validated
        if form_result is None:
            return {"output": "Invalid resume data"}

        with open(os.path.join(os.path.dirname(__file__), 'templates/resume.html.j2')) as f:
            template = Template(f.read())

        html_output = template.render(resume=form_result)

        # Save to file or return as needed
        output_path = f"resume_{form_result.full_name.lower().replace(' ', '_')}.html"
        with open(output_path, 'w') as f:
            f.write(html_output)

        return {"output": f"Resume created successfully! Saved to {output_path}"}