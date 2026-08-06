from crewai import Agent, LLM

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

researcher = Agent(
    role="Researcher",
    goal="Research Generative AI",
    backstory="Expert in AI research",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write an easy-to-understand article",
    backstory="Professional technical writer",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Reviewer",
    goal="Review and improve the article",
    backstory="Senior editor",
    llm=llm,
    verbose=True
)