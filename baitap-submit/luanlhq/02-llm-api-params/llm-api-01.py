#1.Viết một ứng dụng console đơn giản, người dùng gõ câu hỏi vào console, bot trả lời và in ra. Có thể dùng stream hoặc non-stream.

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
gsk_xxxx=os.getenv('API_KEY_GROQ')

#print(f" load gsk api {gsk_xxxx}")

# Nếu các bạn lấy dùng TogetherAI
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # Làm theo hướng dẫn trong bài, truy cập https://console.groq.com/keys để lấy API Key nha
    api_key = gsk_xxxx,
)

def chat_non_stream(prompt):
    
    chat_completion = client.chat.completions.create(
        
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        max_tokens=160,
        temperature=0.6,
        top_p=0.92
    )
    print("\nTrả lời:\n")
    print(chat_completion.choices[0].message.content)

def main():
    print("=== Groq Chat ===")
    user_input = input(" Bạn: ").strip()
    chat_non_stream(user_input)

if __name__ == "__main__":
    main()