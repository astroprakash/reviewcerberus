from typing import Any

from ..config import RECURSION_LIMIT
from .agent import agent
from .progress_callback_handler import ProgressCallbackHandler
from .schema import Context


def run_review(
    context: Context,
    show_progress: bool = True,
    additional_instructions: str | None = None,
) -> tuple[str, dict | None]:
    callbacks = []
    if show_progress:
        callbacks.append(ProgressCallbackHandler())

    config: dict[str, Any] = {
        "configurable": {
            "thread_id": "1",
        },
        "callbacks": callbacks,
        "recursion_limit": RECURSION_LIMIT,
    }

    # Build the review request message
    message_content = "Please review the code changes."
    if additional_instructions:
        message_content += f"\n\nAdditional instructions:\n{additional_instructions}"

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
        },
        config=config,
        context=context,
    )

    token_usage = None
    if "messages" in response:
        final_message = response["messages"][-1]
        raw_content = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )

        # Strip meta-commentary before the actual review
        # Find the first line starting with '#' (markdown header)
        lines = raw_content.split("\n")
        start_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                start_index = i
                break
        content = "\n".join(lines[start_index:])

        # Aggregate token usage across all AI messages
        total_input = 0
        total_output = 0
        cumulative_total = 0

        for msg in response["messages"]:
            if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                usage = msg.usage_metadata
                # Sum output tokens from each turn
                total_output += usage.get("output_tokens", 0)
                # Keep final cumulative total (increases each turn)
                cumulative_total = usage.get("total_tokens", 0)

        # Calculate total input as: cumulative_total - total_output
        total_input = cumulative_total - total_output

        if cumulative_total > 0:
            token_usage = {
                "total_input_tokens": total_input,
                "output_tokens": total_output,
                "total_tokens": cumulative_total,
            }
    else:
        content = str(response)

    return content, token_usage
