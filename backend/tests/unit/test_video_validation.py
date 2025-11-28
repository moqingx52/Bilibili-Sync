from video.validator import normalize_bilibili_url


def test_valid_bilibili_url_extracts_bvid():
    valid, embed, error = normalize_bilibili_url("https://www.bilibili.com/video/BV1xx411c7mD")
    assert valid is True
    assert embed and embed.startswith("https://player.bilibili.com/player.html?bvid=BV1xx411c7mD")
    assert error is None


def test_invalid_url_returns_error():
    valid, embed, error = normalize_bilibili_url("https://example.com/notvideo")
    assert valid is False
    assert embed is None
    assert error
