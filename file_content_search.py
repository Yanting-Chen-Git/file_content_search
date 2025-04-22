import os
import fitz

def search_pdf(file_path, keyword, summary):
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if keyword.lower() in text.lower():
            for line in text.split('\n'):
                if keyword.lower() in line.lower():
                    info = f"[PDF] {os.path.basename(file_path)} - Page {page_num + 1}:\n   > {line.strip()}"
                    print("\n" + info)
                    summary.append(line.strip())  # 只存文字給第二階段使用
    doc.close()

# === 主程式 ===
folder_path = r"D:\Realtek_YT\CN5\Document\Internal\Standard\100_1000BASE-T1\1000BASE-T1"

first_keyword = input("請輸入第一次搜尋的關鍵字（例如 MAC）：").strip()
summary = []

print(f"\n🔍 開始搜尋包含「{first_keyword}」的內容...")

# 執行第一次搜尋
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        if file.lower().endswith('.pdf'):
            search_pdf(file_path, first_keyword, summary)

# 列出第一次搜尋結果
print(f"\n✅ 0x {len(summary)} 筆資料\n")
print("====== 第一次搜尋結果（請參考下方內容再輸入第二關鍵字） ======\n")

for i, line in enumerate(summary, 1):
    print(f"{i:02d}. {line}")

# 讓使用者根據內容再輸入第二個關鍵字
second_keyword = input("\n請輸入第二次搜尋的關鍵字（例如 security）：").strip()

# 執行第二階段過濾
print(f"\n🔎 第二階段搜尋：篩選包含「{second_keyword}」的內容...")
second_hits = []

for line in summary:
    if second_keyword.lower() in line.lower():
        print(f"\n✔️ 命中：\n   > {line}")
        second_hits.append(line)

print(f"\n✅ 第二階段完成，共找到 {len(second_hits)} 筆結果")
