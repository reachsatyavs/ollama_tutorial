#!/usr/bin/env python3
"""
Your FIRST Ollama agent (Python).

A plain *model* can only return text. An *agent* is a model plus tools it can
decide to use. This tiny program gives the model ONE tool -- a weather lookup --
and lets the model choose when to call it. That decide-then-act loop is exactly
what turns a model into an agent.

Flow:
    You ask a question
      -> the model decides to call get_weather("Paris")
      -> YOUR code runs the real function
      -> the result is handed back to the model
      -> the model writes a normal, human answer

Run it (make sure `ollama serve` is running first):
    uv run examples/simple_agent.py
"""

import ollama

MODEL = "qwen3.5:0.8b"   # a small, tool-capable model. NOTE: not every model supports
                         # tool calling -- coder-tuned models like qwen2.5-coder often
                         # print JSON as text instead. Pick a tool-capable one from `ollama list`.


# 1) A normal Python function. This is the "tool" the agent is allowed to use.
def get_weather(city: str) -> str:
    """Return the current weather for a city (faked so it works offline)."""
    fake_weather = {
        "paris": "18°C and cloudy",
        "tokyo": "24°C and sunny",
        "new york": "12°C and rainy",
    }
    return fake_weather.get(city.lower(), f"Sorry, I have no weather data for {city}.")


# 2) Describe that tool to the model so it knows the tool exists and how to call it.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name, e.g. Paris"}
                },
                "required": ["city"],
            },
        },
    }
]

# Map the tool name back to the real Python function.
available_functions = {"get_weather": get_weather}


def main():
    question = "What's the weather in Paris right now?"
    print(f"🧑 You:    {question}\n")

    messages = [{"role": "user", "content": question}]

    # 3) First call: the model sees the question AND the available tools.
    #    It responds by asking to call get_weather rather than answering directly.
    response = ollama.chat(model=MODEL, messages=messages, tools=tools)
    messages.append(response.message)

    # 4) Did the model choose to use a tool?
    if response.message.tool_calls:
        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"🤖 Model wants to call: {name}({dict(args)})")

            # 5) WE run the actual Python function -- this is the "action".
            result = available_functions[name](**args)
            print(f"🔧 Tool result:         {result}\n")

            # 6) Hand the tool's result back to the model.
            messages.append({"role": "tool", "content": result, "tool_name": name})

        # 7) Final call: the model now writes a natural answer using that result.
        final = ollama.chat(model=MODEL, messages=messages)
        print(f"🤖 Agent:  {final.message.content}")
    else:
        # The model decided it didn't need the tool.
        print(f"🤖 Agent:  {response.message.content}")


if __name__ == "__main__":
    main()
