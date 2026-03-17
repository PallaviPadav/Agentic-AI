from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.tools.tavily import TavilyTools   # ✅ UPDATED
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType
import os
import streamlit as st
from dotenv import load_dotenv
import requests
import shutil

# Load env variables
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')  # ✅ ADD THIS

# Download PDF
url = "https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
with open("thai_recipes.pdf", "wb") as f:
    f.write(requests.get(url).content)

# Clean old DB
shutil.rmtree("tmp/lancedb", ignore_errors=True)

# Create Knowledge Base
knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="recipes",
        search_type=SearchType.hybrid,
        embedder=HuggingfaceCustomEmbedder(dimensions=1024)
    )
)

# Insert PDF
knowledge.insert(
    path="thai_recipes.pdf",
    reader=PDFReader(),
)

# Create Agent with Tavily
agent = Agent(
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"), #"llama-3.3-70b-versatile"),
    description="You are a thai cuisine expert!",
    instructions=[
        "Search your knowledge base for the query",
        "If the question is better suited for the web, search the web to fill in gaps.",
        "Prefer the information in your knowledge base over the web results."
    ],
    knowledge=knowledge,
    tools=[TavilyTools()],   # ✅ USING TAVILY HERE
    markdown=True
)

# Test Run
result = agent.run("How do I make chicken and galangal soup?")
print(result.content)

# Streamlit UI
st.title("🥘 Thai Cuisine Expert")
st.write("Ask me anything about Thai cuisine! From recipes to history, I've got you covered.")

user_input = st.text_input("Enter your question:")

if user_input:
    with st.spinner("Thinking..."):
        response = agent.run(user_input)
        st.markdown("### 🍜 Answer")
        st.markdown(response.content.strip())
        st.divider()