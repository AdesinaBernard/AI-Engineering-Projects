def improve_tool_input(tool, tool_input, failure_reason):
    if tool == "rag":
        focus_text = "Focus only on information available in the knowledge base."

        if focus_text in tool_input:
            return tool_input

        return f"{tool_input}\n\n{focus_text}"

    if tool == "summarizer":
        return f"""
Summarize clearly in 3 concise bullet points:

{tool_input}
"""

    if tool == "analyze_repos":
        return tool_input

    return tool_input