from openai import OpenAI
import subprocess
from dotenv import load_dotenv
import os
import re


load_dotenv()
gsk_xxxx=os.getenv('API_KEY_GROQ')
model_groq="llama-3.1-8b-instant"

OUTPUT_FILE = r"D:\codedao_ai\04-api-and-parameter\final.py"

#print(f" load gsk api {gsk_xxxx}")

# Nếu các bạn lấy dùng TogetherAI
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # Làm theo hướng dẫn trong bài, truy cập https://console.groq.com/keys để lấy API Key nha
    api_key = gsk_xxxx,
)
def get_code_from_groq(problem_description):
    
    print(f"⏳ Đang nhờ Llama-3.1 viết code cho bài: '{problem_description}'...")
    
    system_prompt = (
        "Bạn là một chuyên gia lập trình Python. "
        "Nhiệm vụ của bạn là viết code Python để giải quyết bài toán của người dùng. "
        "YÊU CẦU BẮT BUỘC: \n"
        "1. CHỈ trả về code Python hợp lệ nằm trong khối markdown (```python ... ```).\n"
        "2. Code phải là một script hoàn chỉnh, chạy được ngay lập tức (ứng dụng console).\n"
        "3. TUYỆT ĐỐI KHÔNG thêm lời giải thích, văn bản mở đầu hay kết thúc ở bên ngoài khối code.\n"
        
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": problem_description}
            ],
            model=model_groq,
            temperature=0.1
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Lỗi kết nối API: {e}")
        return None

def extract_python_code(response_text):
    """Lọc lấy phần code nằm trong ```python ... ```"""
    # Tìm pattern ```python ... ``` hoặc ``` ... ```
    pattern = r"```(?:python)?\n(.*?)```"
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    if matches: 
        return max(matches, key=len).strip()
    else:
        return response_text.strip()

def main():
    # 1. Nhập đề bài
    print("--- CÔNG CỤ GIẢI BÀI TẬP TỰ ĐỘNG ---")
    problem = input("Nhập yêu cầu bài tập (VD: kiểm tra số chẵn lẻ): ")
    
    if not problem:
        print("Vui lòng nhập đề bài.")
        return

    # 2. Lấy code từ AI
    raw_response = get_code_from_groq(problem)
    if not raw_response:
        return

    # 3. Trích xuất và làm sạch code
    clean_code = extract_python_code(raw_response)
    
    # 4. Lưu vào final.py
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(clean_code)
        print(f"✅ Đã lưu code giải vào: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")
        return

    # 5. Chạy code vừa tạo
    print(f"\n>>> ĐANG CHẠY {OUTPUT_FILE} >>>\n")
    try:
        # Gọi subprocess để chạy file final.py
        subprocess.run(["python", OUTPUT_FILE], check=False)
    except Exception as e:
        print(f"❌ Lỗi khi chạy chương trình: {e}")
    
    print(f"\n<<< KẾT THÚC CHẠY THỬ <<<")

if __name__ == "__main__":
    main()