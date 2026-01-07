import re
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

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
    如果是 b23.tv 这样的短链接，先请求一次，跟随重定向拿到真实的 B 站 URL。
    使用标准库 urllib，不额外引入第三方依赖。
    """
    try:
        with urlopen(url, timeout=5) as resp:
            # geturl() 会返回最终重定向后的地址
            return resp.geturl()
    except Exception:
        # 如果解析失败，就退回原始 URL，后续照常走提取逻辑
        return url


def normalize_bilibili_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Return (valid, normalized_embed_url, error_message)."""
    if not url:
        return False, None, "Missing URL"

    # 如果是 b23.tv 短链接，先解析成最终跳转后的 URL
    parsed = urlparse(url)
    if parsed.netloc in ["b23.tv", "www.b23.tv"]:
        url = resolve_short_url(url)

    bvid = extract_bvid(url)
    if not bvid:
        return False, None, "Unsupported or invalid Bilibili link"
    embed_url = f"https://player.bilibili.com/player.html?bvid={bvid}&autoplay=0"
    return True, embed_url, None
