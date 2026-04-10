import os
import re
import time
from dataclasses import dataclass
from typing import Callable

from google import genai

TEXT_MODEL_CANDIDATES = ["gemini-2.5-flash", "gemini-2.0-flash"]


def parse_cookie_string(raw: str) -> dict[str, str]:
    cookies: dict[str, str] = {}
    if not raw:
        return cookies

    for item in raw.split(";"):
        part = item.strip()
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        cookies[key] = value
    return cookies


@dataclass(slots=True)
class PublishConfig:
    gemini_api_key: str
    blog_id: str
    naver_user_id: str
    cookies_raw: str

    @classmethod
    def from_env(cls) -> "PublishConfig":
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY", "AIzaSyDkFZGgFtrEqlJN9O74FACS1ml1dxgzsgs"),
            blog_id=os.getenv("NAVER_BLOG_ID", ""),
            naver_user_id=os.getenv("NAVER_USER_ID", ""),
            cookies_raw=os.getenv("NAVER_COOKIES_RAW", "")
        )


class NaverBlogPublisher:
    def __init__(self, config: PublishConfig):
        self.config = config
        self.cookies = parse_cookie_string(config.cookies_raw)
        try:
            from naver_blog_client_local import NaverBlogClient
        except ImportError:
            from naver_blog_client_template import NaverBlogClient
        self.naver_client = NaverBlogClient(config, self.cookies)

    def validate(self) -> None:
        if not self.config.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required")
        if not self.config.blog_id:
            raise RuntimeError("NAVER_BLOG_ID is required")
        if not self.config.naver_user_id:
            raise RuntimeError("NAVER_USER_ID is required")
        if not self.cookies:
            raise RuntimeError("NAVER_COOKIES_RAW is required")

    def generate_blog_content(self, keyword: str, log: Callable[[str], None]) -> tuple[str, str]:
        log(f"Gemini text generation started: {keyword}")
        client = genai.Client(api_key=self.config.gemini_api_key)
        prompt = (
            "사용자: "
            f"네이버 블로그 글을 작성해줘. 키워드는 '{keyword}' 이야. "
            "응답 형식은 아래를 정확히 지켜줘.\n"
            "TITLE: 한 줄 제목\n"
            "CONTENT:\n"
            "본문 여러 문단\n"
            "AI:"
        )

        last_error: Exception | None = None
        for model_name in TEXT_MODEL_CANDIDATES:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    answer = response.text.strip()
                    title_match = re.search(r"TITLE:\s*(.+)", answer)
                    content_match = re.search(r"CONTENT:\s*(.*)", answer, re.DOTALL)

                    title = title_match.group(1).strip() if title_match else f"{keyword} 관련 이야기"
                    content = content_match.group(1).strip() if content_match else answer
                    log(f"Gemini text generation completed with model {model_name}")
                    return title, content
                except Exception as error:
                    last_error = error
                    log(f"Gemini request failed with model {model_name} on attempt {attempt + 1}: {error}")
                    time.sleep(min(2 * (attempt + 1), 5))

        raise RuntimeError(f"Gemini text generation failed: {last_error}")

    def publish(self, keyword: str, log: Callable[[str], None] = print) -> dict:
        self.validate()
        title, content = self.generate_blog_content(keyword, log)
        return self.naver_client.publish_text_post(title, content, log)
