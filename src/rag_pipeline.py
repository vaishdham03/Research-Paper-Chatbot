from src.retriever import get_retriever
from src.groq_api import get_llm
from src.memory import get_history

retriever = get_retriever()
llm = get_llm()

def generate_answer(username, question):

    docs = retriever.invoke(question)
    print("Retrieved docs:", len(docs))
    context = ""
    sources = []

    for doc in docs:

        context += doc.page_content + "\n\n"

        metadata = doc.metadata or {}

        # fallback if custom metadata missing
        paper = metadata.get("paper_title") or metadata.get("source", "Unknown")
        page = metadata.get("page", "N/A")
        pdf = metadata.get("pdf_path") or metadata.get("source", "")

        # clean paper name
        paper = paper.split("/")[-1]

        sources.append({
            "paper": paper,
            "page": page,
            "pdf": pdf
        })

    history = get_history(username)

    prompt = f"""
You are an AI research assistant.

Use ONLY the provided research context.

If the answer is not in the context, say:
"I could not find this information in the research papers."

Chat History:
{history}

Context:
{context}

Question:
{question}

Answer clearly and academically.
"""

    response = llm.invoke(prompt)

    return response.content, sources