def improve_tool_input(tool, tool_input, failure_reason):
    if tool == "rag":
        return f"{tool_input}\n\nFocus only on information available in the knowledge base."

    if tool == "summarizer":
        return f"""
Summarize clearly in 3 concise bullet points:

{tool_input}
"""

    if tool == "analyze_repos":
        return tool_input

    return tool_input