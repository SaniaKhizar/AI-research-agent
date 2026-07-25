# 🔎 AI Research Agent

A conversational AI agent that decides when it needs current information, searches the web autonomously, and answers grounded in real search results — built from scratch using function calling, not a pre-built agent framework.

**🔗 Live demo:** https://ai-research-agent-skh.streamlit.app

## What it does

Ask it anything. It decides for itself whether it needs to search the web (e.g. current events, weather, recent news) or can answer directly from its own knowledge (e.g. general facts, opinions, math). When it searches, it reads the real results and grounds its answer in them — it's explicitly instructed not to invent specific facts or numbers that aren't in the retrieved data.

It also remembers the conversation, so follow-up questions like "explain the second point in more detail" work correctly.

## How it works

```
User question
     ↓
Model decides: does this need a web search?
     ↓                              ↓
   No                             Yes
     ↓                              ↓
Answer directly          Calls search_web() tool
                                    ↓
                          Real search results returned
                                    ↓
                          Model reads results, writes
                          a grounded, sourced answer
```

This decide → call tool → observe → respond loop is the core pattern behind most modern AI agents.

## Tech stack

- **LLM:** [Groq](https://groq.com) API running `openai/gpt-oss-20b`
- **Web search:** [Tavily](https://tavily.com) — search API built for AI agents
- **UI:** [Streamlit](https://streamlit.io)
- **Language:** Python

## Key engineering decisions worth noting

- **Function calling, not a framework.** Built with raw API calls instead of LangChain, to understand exactly how tool use works under the hood before relying on abstractions.
- **Hallucination guarding.** Early testing showed the model would sometimes fabricate specific, plausible-looking numbers (e.g. weather data) when search results were thin. Fixed with an explicit system-prompt constraint forbidding invented specifics, plus increasing retrieved content length so the model has enough real data to work with.
- **Tool-call reliability handling.** Some models occasionally fail to format a tool call correctly. Added automatic retry logic with adjusted temperature to handle this gracefully instead of crashing.
- **Modular structure** — code is split by responsibility (`llm_client.py`, `tools.py`, `agent.py`, `gui.py`) rather than kept in one file, for readability and maintainability.

## Project structure

```
├── gui.py             # Streamlit chat interface
├── main.py             # Terminal-based version (for testing/dev)
├── agent.py            # Core agent logic: decision-making + tool calling
├── tools.py             # search_web() function + tool schema
├── llm_client.py        # API client setup (Groq, Tavily)
├── requirements.txt
└── .env.example         # Template for required API keys
```

## Running it locally

1. Clone the repo:
```bash
git clone https://github.com/SaniaKhizar/AI-research-agent.git
cd AI-research-agent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

3. Get free API keys:
   - [Groq](https://console.groq.com) — for the LLM
   - [Tavily](https://tavily.com) — for web search

4. Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

5. Run the terminal version:
```bash
python main.py
```
Or the web UI:
```bash
streamlit run gui.py
```

## Known limitations

- Tool-call formatting occasionally fails on the first attempt with this model (handled via automatic retry, but not 100% eliminated)
- Search is limited to the top 3 Tavily results per query — broader research tasks would need multi-query support (a natural next step)

## Possible future improvements

- Multi-step search (letting the agent search multiple times per question for complex research)
- Source citation formatting in the final answer
- Support for additional tools beyond web search (e.g. calculator, code execution)
