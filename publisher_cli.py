import json
import sys

from publisher_core import NaverBlogPublisher, PublishConfig


def main() -> int:
    payload = json.loads(sys.stdin.read() or "{}")
    config = PublishConfig(
        gemini_api_key=payload.get("geminiApiKey", ""),
        blog_id=payload.get("blogId", ""),
        naver_user_id=payload.get("naverUserId", ""),
        cookies_raw=payload.get("cookiesRaw", ""),
    )
    keyword = payload.get("keyword", "")
    publisher = NaverBlogPublisher(config)
    result = publisher.publish(keyword)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
