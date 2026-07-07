class PromptBuilder:
    def build(self, query: str, context: str) -> str:
        return f"""
You are a helpful assistant answering questions using the provided context.

Rules:
- Use only the context below.
- If the answer is not in the context, say you don't know.
- Be concise.
- Cite chunk ids when helpful.

Context:
{context}

Question:
{query}

Answer:
""".strip()