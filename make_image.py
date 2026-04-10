import os
import uuid
from datetime import datetime
from io import BytesIO

from google import genai
from google.genai import types

# pip install pillow
from PIL import Image


def save_generated_images(response, out_dir="generated_images", prefix="imagen"):
    os.makedirs(out_dir, exist_ok=True)

    saved = []
    for i, generated in enumerate(response.generated_images, start=1):
        # SDK 예시에 따르면 image_bytes는 bytes로 들어옴 :contentReference[oaicite:1]{index=1}
        img_bytes = generated.image.image_bytes

        # 파일명: 날짜 + uuid
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{prefix}_{ts}_{uuid.uuid4().hex[:8]}_{i}.png"
        fpath = os.path.join(out_dir, fname)

        # 안전하게 PNG로 저장
        img = Image.open(BytesIO(img_bytes))
        img.save(fpath, format="PNG")

        saved.append(fpath)

    return saved


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("환경변수 GEMINI_API_KEY가 없어요. 키를 먼저 설정해주세요.")

    client = genai.Client(api_key=api_key)

    # 텍스트 대화용 모델
    chat_model = "gemini-2.0-flash"

    # 이미지 생성용 모델 (Imagen)
    # 문서 예시: imagen-4.0-generate-001 / imagen-3.0-generate-002 :contentReference[oaicite:2]{index=2}
    image_model = "imagen-4.0-generate-001"

    print("Gemini 챗 시작!")
    print("종료: /exit, 초기화: /reset")
    print("이미지: /draw <프롬프트>  (예: /draw 로고 느낌의 미니멀 고양이 아이콘)\n")

    chat = client.chats.create(model=chat_model)

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        if user_text == "/exit":
            print("bye 👋")
            break

        if user_text == "/reset":
            chat = client.chats.create(model=chat_model)
            print("(대화 초기화 완료)\n")
            continue

        # ---- 이미지 생성 커맨드 ----
        if user_text.startswith("/draw"):
            prompt = user_text[len("/draw"):].strip()
            if not prompt:
                print("Gemini: /draw 다음에 프롬프트를 적어줘!\n")
                continue

            try:
                # 이미지 1장 기본. 늘리고 싶으면 number_of_images만 바꾸면 됨. :contentReference[oaicite:3]{index=3}
                resp = client.models.generate_images(
                    model=image_model,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(number_of_images=1),
                )

                paths = save_generated_images(resp, out_dir="generated_images", prefix="imagen")
                print("Gemini: 이미지 저장 완료 ✅")
                for p in paths:
                    print(f" - {p}")
                print()

            except Exception as e:
                print(f"[이미지 생성 에러] {e}\n")

            continue

        # ---- 텍스트 대화 ----
        try:
            resp = chat.send_message(user_text)
            print(f"Gemini: {resp.text}\n")
        except Exception as e:
            print(f"[에러] {e}\n")


if __name__ == "__main__":
    main()
