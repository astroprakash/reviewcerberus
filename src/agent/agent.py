from typing import Any

from langchain.agents import create_agent

from .checkpointer import checkpointer
from .model import model
from .schema import Context
from .system import SYSTEM_PROMPT
from .tools import (
    changed_files,
    diff_file,
    get_commit_messages,
    list_files,
    read_file_part,
    search_in_files,
)

agent: Any = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[
        changed_files,
        get_commit_messages,
        diff_file,
        read_file_part,
        search_in_files,
        list_files,
    ],
    context_schema=Context,
    checkpointer=checkpointer,
)
