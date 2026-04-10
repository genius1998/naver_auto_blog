# gemini_terminal_chat.py
import os
from google import genai

MODEL_NAME = "gemini-2.5-flash"

def build_contents_from_history(history):
    """
    Gemini에 보낼 contents를 문자열 하나로 합치는 단순 버전.
    """
    lines = []
    for role, text in history:
        prefix = "사용자" if role == "user" else "AI"
        lines.append(f"{prefix}: {text}")
    lines.append("AI:")
    return "\n".join(lines)

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다.")

    client = genai.Client(api_key=api_key)

    print("Gemini 대화 시작")
    print("종료하려면 exit 입력\n")

    history = []

    while True:
        user_input = input("나: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("대화를 종료합니다.")
            break

        history.append(("user", user_input))

        prompt = build_contents_from_history(history)

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            answer = response.text.strip()
            print(f"Gemini: {answer}\n")

            history.append(("assistant", answer))

        except Exception as e:
            print(f"에러 발생: {e}\n")

if __name__ == "__main__":
    main()