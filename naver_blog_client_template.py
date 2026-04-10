import json
import re
import uuid
from typing import Callable


class NaverBlogClient:
    def __init__(self, config, cookies: dict[str, str]):
        self.config = config
        self.cookies = cookies

    def publish_text_post(self, title: str, content: str, log: Callable[[str], None] = print) -> dict:
        raise NotImplementedError(
            "Local Naver blog API implementation is not committed. "
            "Create naver_blog_client_local.py based on this template."
        )

    def create_document_model(self, title: str, content: str, image_info: dict | None = None) -> str:
        def se_id() -> str:
            return f"SE-{uuid.uuid4()}"

        components = [{
            "id": se_id(),
            "layout": "default",
            "title": [{
                "id": se_id(),
                "nodes": [{"id": se_id(), "value": title, "@ctype": "textNode"}],
                "@ctype": "paragraph"
            }],
            "subTitle": None,
            "align": "left",
            "@ctype": "documentTitle"
        }]

        if content.strip():
            components.append({
                "id": se_id(),
                "layout": "default",
                "value": [{
                    "id": se_id(),
                    "nodes": [{"id": se_id(), "value": content, "@ctype": "textNode"}],
                    "@ctype": "paragraph"
                }],
                "@ctype": "text"
            })

        document = {
            "documentId": "",
            "document": {
                "version": "2.9.0",
                "theme": "default",
                "language": "ko-KR",
                "id": str(uuid.uuid4()).replace("-", ""),
                "components": components,
                "di": {"dif": False, "dio": [{"dis": "N", "dia": {"t": 0, "p": 0, "st": 1, "sk": 1}}]}
            }
        }
        return json.dumps(document, ensure_ascii=False)
