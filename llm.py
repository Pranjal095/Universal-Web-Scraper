from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#Using Llama3.1 as the LLM
model = OllamaLLM(model="llama3.1")

def generate_subqueries(user_query, ollama_model):
    prompt = f"""
    Current Query: {user_query}

    You are an expert at understanding and correlating user queries. If the query consists of distinct sub-questions, and a clear distinction is observed, break it down into meaningful and logically separate sub-questions **only if necessary.** Otherwise, retain the query as is. **If the query is already a complete and meaningful statement, return it without changes.** Minor grammatical adjustments are allowed if required.

    Guidelines:
    1. **If the query is already a valid and complete question or statement, return it as is without splitting.**  
    2. **Break down the query only when it contains multiple, distinct parts that can stand alone as sub-questions.**  
    3. **Maintain the original intent and context of the query when creating sub-questions.**  
    4. **Provide only the output without any additional explanations or comments.**
    5. **There may be typos or grammatical mistakes. Fix them as per necessity.**
    6. **If the query appears to reference a previous query, use the provided memory to frame it as a complete and independent question.**

    ### Example 1:  
    **Input:** "What is the QS and NIRF ranking of IITH?"  
    **Output:**  
    - "What is the QS ranking of IITH?"  
    - "What is the NIRF ranking of IITH?"  

    ### Example 2:  
    **Input:** "Summarize about IIT."  
    **Output:**  
    - "Summarize about IIT."  

    ### Example 3:  
    **Input:** "Explain the differences between QS and NIRF rankings."  
    **Output:**  
    - "What are QS rankings?"  
    - "What are NIRF rankings?"  
    - "What are the differences between QS and NIRF rankings?"  

    ### Example 4:  
    **Input:** "Who is Rajesh Kedia?"  
    **Output:**  
    - "Who is Rajesh Kedia?"  

    ### Example 5:  
    **Input:** "What is Lambda IITH?"  
    **Output:**  
    - "What is Lambda IITH?"  

    Query: {user_query}  
    Output:
    """

    formatted_prompt = prompt.format(user_query=user_query)
    response = ollama_model.invoke(formatted_prompt)
    
    subqueries = response.strip().split("\n")
    cleaned_subqueries = [
        subquery.strip() for subquery in subqueries 
        if subquery.strip() and not subquery.startswith(("**", "To answer", "These", "The next"))
    ]

    if len(cleaned_subqueries) == 0 or (len(cleaned_subqueries) == 1 and cleaned_subqueries[0] == user_query.strip()):
        return [user_query.strip()]

    return cleaned_subqueries

#Template for querying the LLM
template = (
    "You are tasked with answering the following query based on the provided context:\n\n"
    "Query: {query}\n\n"
    "Context:\n{combined_content}\n\n"
    "Guidelines:\n"
    "1. Provide a direct answer providing the exact details asked in the query.\n"
    "2. Use a professional tone.\n"
    "3. Address all relevant aspects of the query.\n"
)

def prompt_llm(relevant_sections, query):
    combined_content = "\n\n".join(relevant_sections).strip()
    formatted_prompt = template.format(
        query=query,
        combined_content=combined_content
    )
    response = model.invoke(formatted_prompt)
    
    return response.strip()