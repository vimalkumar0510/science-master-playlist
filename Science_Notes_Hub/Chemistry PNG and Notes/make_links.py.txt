import os

folder_path = "."  # Jahan PDFs rakhi hain
pdf_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])

html_lines = [
    "<!DOCTYPE html>",
    "<html lang='hi'>",
    "<head><meta charset='UTF-8'><title>All PDF Links</title></head>",
    "<body>",
    "<h2>Sabhi PDF Files</h2>",
    "<ul>"
]

for pdf in pdf_files:
    html_lines.append(f'  <li><a href="{pdf}" target="_blank">{pdf}</a></li>')

html_lines.extend([
    "</ul>",
    "</body>",
    "</html>"
])

with open("index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html_lines))

print(f"Done! {len(pdf_files)} PDF links added to index.html")