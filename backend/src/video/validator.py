#注意要pip install requests，才能正确解析短链
import re
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests  # 新增

BVID_PATTERN = re.compile(r"BV[0-9A-Za-z]{10}")


def extract_bvid(url: str) -> Optional[str]:
    parsed = urlparse(url)
    candidate: Optional[str] = None
    # Direct path BV
    match = BVID_PATTERN.search(parsed.path)
    if match:
        candidate = match.group(0)
    # Query parameter bvid
    if not candidate:
        qs = parse_qs(parsed.query)
        bvids = qs.get("bvid") or qs.get("bv")
        if bvids:
            candidate = bvids[0]
    return candidate


def resolve_short_url(url: str) -> str:
    """
    解析 b23.tv 等短链接，返回最终跳转后的 URL。
    使用 requests.get + allow_redirects=True，更适配真实站点行为。
    """
    try:
        resp = requests.get(url, allow_redirects=True, timeout=5)
        return resp.url
    except Exception:
        # 失败就退回原始 URL，后续逻辑再尝试从中提取 BV
        return url


def normalize_bilibili_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Return (valid, normalized_embed_url, error_message)."""
    if not url:
        return False, None, "Missing URL"

    parsed = urlparse(url)

    # 如果是 b23.tv 短链，先解析一次
    if parsed.netloc in ["b23.tv", "www.b23.tv"]:
        url = resolve_short_url(url)
        parsed = urlparse(url)  # 重新解析新的 URL

    bvid = extract_bvid(url)
    if not bvid:
        return False, None, "Unsupported or invalid Bilibili link"

    embed_url = f"https://player.bilibili.com/player.html?bvid={bvid}&autoplay=0"
    return True, embed_url, None
