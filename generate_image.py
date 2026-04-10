# gemini_image_prompt_input.py
import os
from google import genai
from google.genai import types

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다.")

    client = genai.Client(api_key=api_key)

    prompt = input("이미지 프롬프트를 입력하세요: ").strip()
    if not prompt:
        print("프롬프트가 비어 있습니다.")
        return

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )

    image = response.generated_images[0].image
    output_path = "output.png"
    image.save(output_path)

    print(f"완료: {output_path}")

if __name__ == "__main__":
    main()