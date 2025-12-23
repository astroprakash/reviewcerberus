import re
import subprocess

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel

from ..schema import Context


class FileContent(BaseModel):
    file_path: str
    content: str
    start_line: int
    end_line: int
    total_lines: int


def _read_file_part_impl(
    repo_path: str,
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None,
) -> FileContent:
    result = subprocess.run(
        ["git", "-C", repo_path, "show", f"HEAD:{file_path}"],
        capture_output=True,
        text=True,
        check=True,
    )

    lines = result.stdout.splitlines()
    total_lines = len(lines)

    if start_line is None:
        start_line = 1
    if end_line is None:
        end_line = total_lines

    if start_line < 1 or end_line > total_lines or start_line > end_line:
        raise ValueError(
            f"Invalid line range: {start_line}-{end_line} (file has {total_lines} lines)"
        )

    selected_lines = lines[start_line - 1 : end_line]
    content = "\n".join(
        f"{i + start_line:6d}\t{line}" for i, line in enumerate(selected_lines)
    )

    return FileContent(
        file_path=file_path,
        content=content,
        start_line=start_line,
        end_line=end_line,
        total_lines=total_lines,
    )


@tool
def read_file_part(
    runtime: ToolRuntime[Context],
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None,
) -> FileContent | ToolMessage:
    """Read specific lines from a file (or entire file) to understand context."""
    if start_line and end_line:
        print(f"🔧 read_file_part: {file_path} (lines {start_line}-{end_line})")
    else:
        print(f"🔧 read_file_part: {file_path}")
    try:
        return _read_file_part_impl(
            runtime.context.repo_path, file_path, start_line, end_line
        )
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return ToolMessage(
            content=f"Error reading file {file_path}: {str(e)}",
            tool_call_id=runtime.tool_call_id,
        )
