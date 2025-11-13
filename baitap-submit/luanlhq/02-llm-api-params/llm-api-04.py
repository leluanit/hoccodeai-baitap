from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
# ================= CẤU HÌNH =================
gsk_xxxx = os.getenv('API_KEY_GROQ')
model_groq="llama-3.1-8b-instant"
INPUT_FILE =  r"D:\codedao_ai\04-api-and-parameter\sample_english.txt"       
OUTPUT_FILE = r"D:\codedao_ai\04-api-and-parameter\sample_english_translated.txt" 
CHUNK_SIZE = 3000                

# Khởi tạo Client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # Làm theo hướng dẫn trong bài, truy cập https://console.groq.com/keys để lấy API Key nha
    api_key = gsk_xxxx,
)

def get_translator_prompt():
   
    return {
        "role": "system",
        "content": (
            "Bạn là một biên dịch viên chuyên nghiệp, chuyên dịch thuật ngữ kỹ thuật và văn học từ Tiếng Anh sang Tiếng Việt. "
            "Nhiệm vụ của bạn: \n"
            "Dịch đoạn văn bản được cung cấp sang tiếng Việt một cách chính xác, mượt mà, tự nhiên.\n"
            "Giữ nguyên các thuật ngữ chuyên ngành nếu không có từ tiếng Việt tương đương sát nghĩa.\n"
            "Giữ nguyên định dạng (xuống dòng, dấu câu) của bản gốc.\n"
            "QUAN TRỌNG: Chỉ trả về nội dung đã dịch, không thêm lời dẫn hay giải thích."
        )
    }

def split_text_smart(text, limit):
    
    chunks = []
    current_chunk = ""
    paragraphs = text.split('\n')
    
    for p in paragraphs:
        if len(current_chunk) + len(p) < limit:
            current_chunk += p + "\n"
        else:
            
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = p + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def translate_segment(text_segment):
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                get_translator_prompt(),
                {
                    "role": "user",
                    "content": f"Dịch đoạn văn sau:\n\n{text_segment}",
                }
            ],
            model=model_groq,
            temperature=0.6
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Lỗi khi dịch đoạn này: {e}")
        return f"\n[LỖI DỊCH: {e}]\n"

def main():
    print(f"--- BẮT ĐẦU DỊCH FILE: {INPUT_FILE} ---")
    
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Không tìm thấy file {INPUT_FILE}")
        return

    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()

    if not full_text.strip():
        print("⚠️ File rỗng!")
        return

    
    chunks = split_text_smart(full_text, CHUNK_SIZE)
    total_chunks = len(chunks)
    print(f"Đã chia văn bản thành {total_chunks} phần để xử lý.")

    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("")

    
    for i, chunk in enumerate(chunks):
        print(f"Đang dịch phần {i+1}/{total_chunks}...", end="\r")
        
        translated_text = translate_segment(chunk)
        
        
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(translated_text + "\n")
            
    print(f"\n\n HOÀN TẤT! File đã được lưu tại: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()