from crewai import Task
from agents import researcher

research_task = Task(
    description="Explain what Generative AI is.",
    expected_output="A simple explanation for beginners.",
    agent=researcher
)