import os
from google import genai

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("환경변수 GEMINI_API_KEY가 없어요. 키를 먼저 설정해주세요.")

    client = genai.Client(api_key=api_key)

    # 모델은 필요에 따라 바꿔도 됨
    model = "gemini-2.0-flash"

    print("Gemini 챗 시작! 종료: /exit, 초기화: /reset\n")

    # 대화 세션(히스토리 유지)
    chat = client.chats.create(model=model)

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        if user_text == "/exit":
            print("bye 👋")
            break

        if user_text == "/reset":
            chat = client.chats.create(model=model)
            print("(대화 초기화 완료)\n")
            continue

        try:
            resp = chat.send_message(user_text)
            # 응답 텍스트
            print(f"Gemini: {resp.text}\n")
        except Exception as e:
            print(f"[에러] {e}\n")

if __name__ == "__main__":
    main()
