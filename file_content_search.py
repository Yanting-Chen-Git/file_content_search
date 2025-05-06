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
                    summary.append(line.strip())  # storage the result for the next search
    doc.close()


# Make sure search_pdf(file_path, keyword, summary) is already defined

folder_path = r"Path"

summary = []              # Current search results
history_stack = []        # Stack to store previous search results

while True:
    if not summary:
        keyword = input("\n🔍 Enter the first keyword (or 'exit' to quit): ").strip()
    else:
        keyword = input("\n🔍 Enter keyword to filter, or type 'back' to undo, 'exit' to quit: ").strip()

    if keyword.lower() in ["exit", "quit", ""]:
        print("🔚 Search ended.")
        break

    elif keyword.lower() == "back":
        if history_stack:
            summary = history_stack.pop()
            print("\n↩️ Returned to the previous search result:")
            print(f"\n✅ Found {len(summary)} results\n")
            for i, line in enumerate(summary, 1):
                print(f"{i:02d}. {line}")
        else:
            print("\n⚠️ No previous search state to return to.")
        continue

    if not summary:
        print(f"\n🔎 Searching PDF files for '{keyword}'...")
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith('.pdf'):
                    search_pdf(file_path, keyword, summary)
    else:
        history_stack.append(summary[:])  # Save current state
        print(f"\n🔎 Filtering current results with keyword '{keyword}'...")
        summary = [line for line in summary if keyword.lower() in line.lower()]

    print(f"\n✅ Found {len(summary)} results\n")
    for i, line in enumerate(summary, 1):
        print(f"{i:02d}. {line}")
