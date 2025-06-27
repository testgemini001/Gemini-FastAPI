import base64
import tempfile
from pathlib import Path

import httpx
from loguru import logger


def add_tag(role: str, content: str, unclose: bool = False) -> str:
    """Surround content with role tags"""
    if role not in ["user", "assistant", "system"]:
        logger.warning(f"Unknown role: {role}, returning content without tags")
        return content

    return f"<|im_start|>{role}\n{content}" + ("\n<|im_end|>" if not unclose else "")


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens heuristically based on character count"""
    return int(len(text) / 3)


async def save_file_to_tempfile(
    file_in_base64: str, file_name: str = "", tempdir: Path | None = None
) -> Path:
    data = base64.b64decode(file_in_base64)
    suffix = Path(file_name).suffix if file_name else ".bin"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tempdir) as tmp:
        tmp.write(data)
        path = Path(tmp.name)

    return path


async def save_url_to_tempfile(url: str, tempdir: Path | None = None):
    if url.startswith("data:image/"):
        # Base64 encoded image
        base64_data = url.split(",")[1]
        data = base64.b64decode(base64_data)
        suffix = ".png"
    else:
        # http files
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.content
            suffix = Path(url).suffix or ".bin"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tempdir) as tmp:
        tmp.write(data)
        path = Path(tmp.name)

    return path
