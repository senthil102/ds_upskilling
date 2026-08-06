from crewai import Agent, LLM

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

researcher = Agent(
    role="AI Researcher",
    goal="Explain AI concepts",
    backstory="You are an expert AI engineer.",
    llm=llm,
    verbose=True
)