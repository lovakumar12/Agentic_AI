import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ---- Validate keys ----
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

if not SERPER_API_KEY:
    raise ValueError("❌ SERPER_API_KEY not found in .env")

# ---- Tools ----
search_tool = SerperDevTool(api_key=SERPER_API_KEY)

# ---- Agent ----
def create_research_agent():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0.3,
    )

    return Agent(
        role="Research Specialist",
        goal="Conduct thorough research on given topics",
        backstory="You are an experienced researcher skilled at finding and summarizing high-quality information.",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

# ---- Task ----
def create_research_task(agent, topic):
    return Task(
        description=f"""
        Research the following topic thoroughly and produce a clear, structured summary.

        Topic: {topic}
        """,
        expected_output="""
        A well-structured research summary with:
        - Key points
        - Important facts
        - Clear explanations
        """,
        agent=agent,
    )

# ---- Run Crew ----
def run_research(topic):
    agent = create_research_agent()
    task = create_research_task(agent, topic)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()

# ---- Main ----
if __name__ == "__main__":
    print("🔍 Welcome to the Research Agent")
    topic = input("Enter the research topic: ")
    result = run_research(topic)
    print("\n📄 Research Result:\n")
    print(result)
