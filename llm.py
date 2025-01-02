from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template = (
    "You are processing a continuous document split into smaller parts. "
    "This is one part of the document: {content_batch}.\n\n"
    "Your task is to extract and format information relevant to the user's query:\n\n"
    "{prompt}\n\n"
    "Instructions:\n"
    "1. Treat this segment as part of a continuous document. Do not add introductory or concluding remarks.\n"
    "2. Maintain the tone, style, and context from the earlier parts of the document.\n"
    "3. Extract all relevant information explicitly related to the query and format it as described.\n"
    "4. Do not include statements such as 'No relevant information in this segment.' If nothing is relevant, leave the response blank.\n"
    "5. Avoid duplicating information or referencing segment boundaries. Ensure seamless integration with other parts."
)

def prompt_llm(content_batches,prompt):
    prompt_template = ChatPromptTemplate.from_template(template)
    chain = prompt_template | model
    results = []

    for i, batch in enumerate(content_batches):
        response = chain.invoke({"content_batch": batch,"prompt": prompt})
        print(f"Processed batch {i+1} of {len(content_batches)}")
        if response.strip():
            results.append(response.strip())

    return "\n\n".join(results).strip()