from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


load_dotenv()
gsk_xxxx=os.getenv('API_KEY_GROQ')
model_groq="llama-3.1-8b-instant"

#print(f" load gsk api {gsk_xxxx}")
# Nếu các bạn lấy dùng TogetherAI
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # Làm theo hướng dẫn trong bài, truy cập https://console.groq.com/keys để lấy API Key nha
    api_key = gsk_xxxx,
)

def get_text_html(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

   
    content_div = soup.find('div',id='main-detail')
  
    paragraphs = content_div.find_all("p")

    text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    return text

def summarize_text(text):
    prompt = (
        "Bạn là trợ lý thông minh. Hãy đọc nội dung dưới đây và tóm tắt ngắn gọn bằng tiếng Việt:\n\n"
        f"{text}\n\nTóm tắt:"
    )
    response = client.chat.completions.create(
        model = model_groq,
        messages=[{"role":"system","content":"Bạn là một trợ lý chuyên tóm tắt thông tin."},
                  {"role":"user","content": prompt}],
                  max_tokens = 300,
                  temperature=0.6,
                  top_p= 0.92,
                  
    )
    summary = response.choices[0].message.content
    return summary


def main():
    print("=== Nhập Link cần tóm tăt ===")
    #user_input = input("link: ").strip()
    link_url = "https://tuoitre.vn/cac-nha-khoa-hoc-nga-bao-mat-troi-manh-nhat-20-nam-sap-do-bo-trai-dat-2024051020334196.htm?source=0d84f3"
   
    try:
        full_text = get_text_html(link_url)
    except Exception as e:
        print("❌ Lỗi khi lấy nội dung:", e)
        return
    #print("nội dung: ",full_text)
    #print("✅ Đã lấy thành công nội dung (~{} ký tự)".format(len(full_text)))
    print("⏳ Đang gửi lên API để tóm tắt…")
    try:
        summary = summarize_text(full_text)
    except Exception as e:
        print("❌ Lỗi khi gọi API:", e)
        return

    print("\n📝 Tóm tắt nội dung:")
    print(summary)

if __name__ == "__main__":
    main()