from llm_client import tavily_client

def search_web(query):
    results = tavily_client.search(query=query, max_results=3)
    formatted = ""
    for r in results['results']:
        formatted += f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content'][:800]}\n\n"
    return formatted


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current, real-time information on any topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]