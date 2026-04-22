import asyncio
import re

from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# -----------------------------------------------------------------------------
# Helper: extract the final numeric value from a sentence-like tool response.
#
# Your CalcMCP tools may return text like:
#   "The product of 12 and 8 is 96"
# We want to pull out "96" so we can feed clean numbers back into later tool calls.
# -----------------------------------------------------------------------------
def last_number(text: str) -> str:
    nums = re.findall(r"-?\d+(?:\.\d+)?", text)
    return nums[-1] if nums else text


# -----------------------------------------------------------------------------
# Helper: normalize the MCP tool response to plain text.
#
# Many MCP servers return "content blocks" like:
#   [{'type': 'text', 'text': '...'}]
# This function grabs the text content (or falls back to str(...)).
# -----------------------------------------------------------------------------
def tool_text(result) -> str:
    if isinstance(result, list) and result and isinstance(result[0], dict) and "text" in result[0]:
        return result[0]["text"]
    return str(result)


# -----------------------------------------------------------------------------
# Helper: pretty-print tool arguments for the trace output.
# (Purely for display; does not affect the actual tool call.)
# -----------------------------------------------------------------------------
def format_args(args: dict) -> str:
    out = {}
    for k, v in (args or {}).items():
        if isinstance(v, str) and v.isdigit():
            out[k] = int(v)
        else:
            out[k] = v
    return str(out)


async def main():

    client = MultiServerMCPClient({
        "CalcMCP": {
        }
    })

    # Ask the MCP server what tools it exposes.
    # This returns LangChain tool objects that can be invoked with .ainvoke(...)



    # =========================================================================
    # 2) Create an LLM that knows how to "call tools"


    # This is the "system message" that sets the rules of behavior.
    # We emphasize: use tools for math, no nesting, and sequential steps.


    # User question. This requires at least two steps: mul(12,8) then div(96,3).
    user_prompt = "What’s 12×8 / 3 ?"

    # messages is the full conversation history:
    # - System instructions
    # - User question
    # - LLM tool-call messages
    # - Tool result messages


    # =========================================================================
    # 3) Tool-execution loop (the "agent" behavior)
    # =========================================================================

    for _ in range(8):

        # Store the model message in the conversation.
        messages.append(ai)

        # B) IMPORTANT:
        # The model might emit MULTIPLE tool calls in a single turn.
        # We execute them one-by-one, in order, and only move to the next after
        # we have a result for the previous one.
        #

            # Each tool call has an ID; ToolMessage must reference it.
            tool_call_id = call.get("id") or call.get("tool_call_id")

            # Normalize to text, then extract a clean number token.
            text = tool_text(raw_result)
            numeric_value = last_number(text)


    # =========================================================================
    # 4) Print the full trace 
    # =========================================================================
    print("\n=== FULL AGENT TRACE ===")
    for msg in messages:
        if isinstance(msg, HumanMessage):
            print("USER:", msg.content)

        elif isinstance(msg, AIMessage):

        elif isinstance(msg, ToolMessage):
            # Show what we fed back to the model.
            print(f"← TOOL RESULT for ID {msg.tool_call_id}:", msg.content)

    # =========================================================================
    # 5) Print the final natural language answer
    # =========================================================================
    # Walk backwards to find the most recent AIMessage with actual text content.
    final_text = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and (msg.content or "").strip():
            final_text = msg.content.strip()
            break

    print("\n=== FINAL NATURAL LANGUAGE ANSWER ===")
    print(final_text)


if __name__ == "__main__":
    # Standard pattern for running async Python code.
    asyncio.run(main())
