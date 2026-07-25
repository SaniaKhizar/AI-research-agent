import json
from llm_client import groq_client
from tools import search_web, tools

MODEL = "openai/gpt-oss-20b"
DEBUG = False  # Set to True to see tool calls & raw search results

def call_model(messages, use_tools=True, temperature=0.7):
    try:
        if use_tools:
            return groq_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=temperature
            )
        else:
            return groq_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature
            )
    except Exception as e:
        if "tool_use_failed" in str(e):
            if DEBUG:
                print("(retrying tool call with adjusted settings...)")
            return call_model(messages, use_tools, temperature=0.3)
        raise e


def ask_agent(user_question, messages):
    if len(messages) == 0:
        messages.append({
            "role": "system",
            "content": (
                "You are an AI research assistant built by Sania Khizar, running on an open-weight language "
                "model via the Groq API, with access to a web search tool. You are not ChatGPT, ClaudeGPT AI, "
                "or any other product — if asked about your identity, describe yourself simply as a research "
                "assistant with web search capability, without naming a specific company or model unless asked "
                "directly about the underlying technology.\n\n"
                "Use the search_web tool only when the question needs current, factual, or real-time information. "
                "For opinions, definitions, or general knowledge, answer directly without using tools.\n\n"
                "CRITICAL: When using search results, only report specific facts, numbers, or details that "
                "are explicitly present in the search results. Never invent, estimate, or guess specific "
                "figures (temperatures, statistics, dates, etc.) that aren't directly stated in the results. "
                "If the search results don't contain enough detail to fully answer the question, say so "
                "clearly instead of filling in plausible-sounding information.\n\n"
                "FORMATTING: When writing lists, use '-' for bullet points, not '*'. Always leave a blank "
                "line before starting a list and between list items and headings. Keep formatting clean and simple.\n\n"
                "SOURCES: Whenever you use information from search results, end your answer with a "
                "'Sources:' section listing the URLs you actually used, each on its own line. Only include "
                "URLs that were present in the search results you were given — never invent a URL."
                "And also make the URL clickable so the user can directly fetch it too."
    )
            )
        })

    messages.append({"role": "user", "content": user_question})

    try:
        response = call_model(messages)
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

    response_message = response.choices[0].message
    if DEBUG:
        print(f"[DEBUG] tool_calls: {response_message.tool_calls}")
        print(f"[DEBUG] content: {response_message.content}")

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "search_web":
                args = json.loads(tool_call.function.arguments)
                search_result = search_web(args["query"])
                if DEBUG:
                    print(f"\n[DEBUG] Search results:\n{search_result}\n")

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "search_web",
                    "content": search_result
                })

        try:
            second_response = call_model(messages, use_tools=False)
        except Exception as e:
            return f"Sorry, something went wrong generating the final answer: {e}"

        final_answer = second_response.choices[0].message.content
        messages.append({"role": "assistant", "content": final_answer})
        return final_answer
    else:
        messages.append({"role": "assistant", "content": response_message.content})
        return response_message.content