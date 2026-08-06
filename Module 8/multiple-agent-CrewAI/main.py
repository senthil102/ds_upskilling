from crewai import Crew
from agents import researcher, writer, reviewer
from tasks import research_task, writing_task, review_task

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    verbose=True
)

result = crew.kickoff()

print(result)