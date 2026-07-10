"""The tiniest agent: the model calls a real calculator to get exact math.

Usage:
    uv run examples/tiny_agent.py "What is 47281 multiplied by 9912?"
"""
import sys
import ollama

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Take the question from the command line, or use a default if none was given.
question = " ".join(sys.argv[1:]) or "What is 47281 multiplied by 9912?"
print(f"Question: {question}\n")

# With stream=True, chat() returns a GENERATOR of chunks (not a single response),
# so we loop over it: print text as it arrives and collect any tool calls.
stream = ollama.chat(
    model="ministral-3:3b",
    messages=[{"role": "user", "content": question}],
    tools=[multiply],          # just hand it the function — Ollama reads the signature
    stream=True,               # stream the response as it comes in
)

tool_calls = []
for chunk in stream:
    if chunk.message.content:
        print(chunk.message.content, end="", flush=True)   # live text
    if chunk.message.tool_calls:
        tool_calls.extend(chunk.message.tool_calls)         # the model chose a tool

if tool_calls:
    call = tool_calls[0]
    answer = multiply(**call.function.arguments)            # WE run it -> exact result
    print(f"\nAgent called multiply({call.function.arguments}) = {answer}")
