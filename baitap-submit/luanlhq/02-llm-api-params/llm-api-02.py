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

messages=[{"role": "system", "content": "Bạn là một trợ lý thân thiện nói tiếng Việt, nói tiếng Việt, trả lời ngắn gọn và rõ ràng."}]

def chat_stream(prompt):
    messages.append({"role": "user", "content": prompt})
    print("\n Bot: ", end="", flush=True)
    reply_text = ""


    with client.chat.completions.create(
        
        messages=messages,
        model="llama-3.1-8b-instant",
        stream = True   
    ) as stream:
        for chunk in stream: 
            delta = chunk.choices[0].delta 
            if delta and delta.content: 
                print(delta.content, end="", flush=True) 
                reply_text += delta.content

    messages.append({"role": "assistant", "content": reply_text})
    print("\n") 

def main():
    print("=== Groq Chat ===")
    print("Nhập 'exit' để thoát.\n")
    while True:

        user_input = input(" Bạn: ").strip()
        if user_input.lower() == "exit":
            print("\n Kết thúc hội thoại. Tạm biệt!\n")
            break
        chat_stream(user_input)

if __name__ == "__main__":
    main()