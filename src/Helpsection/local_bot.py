from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from Helpsection.vector import retriever

# Initialize LLM
try:
    model = OllamaLLM(model="qwen2.5-coder:3b")
except Exception as e:
    model = None
    print(f"[local_bot] Error initializing LLM: {e}")

# Prompt template (copied from helpbot.py)
template = """
You are a professional electronic engineer and expert assistant specializing in EDA tools including eSim, KiCad, and NgSPICE simulation. 

Use the following knowledge base information to provide accurate and helpful answers:
{context}

Previous conversation context (if any):
{history}

Current question: {question}

Instructions:
- Provide practical, actionable advice
- Include specific commands, syntax, or examples when relevant
- Keep responses concise but comprehensive (maximum 200 words)
- If the question is about debugging, provide step-by-step troubleshooting steps
- Reference specific parameters or options when applicable
- If you're not certain about something, say so clearly

Answer:
"""

prompt_template = ChatPromptTemplate.from_template(template)

def get_bot_response(prompt: str) -> str:
    """Generate a bot response for a given prompt using the local LLM and vector store."""
    if model is None:
        return "Error: LLM model is not available."
    try:
        # 1. Retrieve relevant documents
        context = ""
        docs = retriever.invoke(prompt)
        if isinstance(docs, list) and docs:
            context = "\n\n".join([doc.page_content for doc in docs[:5]])
        elif hasattr(docs, "page_content"):
            context = docs.page_content
        else:
            context = str(docs) if docs else ""

        # 2. No chat history for now
        history = ""

        # 3. Run LLM
        chain = prompt_template | model
        output = chain.invoke({
            "context": context,
            "history": history,
            "question": prompt
        })
        response = str(output).strip()
        return response
    except Exception as e:
        return f"Error: {str(e)}"
