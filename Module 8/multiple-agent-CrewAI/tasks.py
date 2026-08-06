from crewai import Task
from agents import researcher, writer, reviewer

research_task = Task(
    description="Research Generative AI and provide key points.",
    expected_output="Research notes",
    agent=researcher
)

writing_task = Task(
    description="Write a blog using the research.",
    expected_output="A beginner-friendly blog",
    agent=writer,
    context=[research_task]
)

review_task = Task(
    description="Review and improve the blog.",
    expected_output="Final polished blog",
    agent=reviewer,
    context=[writing_task]
)