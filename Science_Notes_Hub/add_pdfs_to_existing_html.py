import html as html_lib
import os
import shutil
from urllib.parse import quote

EXISTING_HTML = "science_master_playlist.html"
BACKUP_HTML = EXISTING_HTML + ".bak"


def detect_subject(rel_path: str) -> str:
  low = rel_path.lower()
  if "physics" in low or "phy" in low:
    return "Physics"
  if "chemistry" in low or "chem" in low:
    return "Chemistry"
  if "biology" in low or "bio" in low:
    return "Biology"
  return "General"


def fmt_size(b: int) -> str:
  if b < 1024:
    return f"{b} B"
  if b < 1048576:
    return f"{b / 1024:.1f} KB"
  return f"{b / 1048576:.2f} MB"


def main():
  if not os.path.exists(EXISTING_HTML):
    print(f"Error: '{EXISTING_HTML}' nahi mili!")
    return

  if not os.path.exists(BACKUP_HTML):
    shutil.copy2(EXISTING_HTML, BACKUP_HTML)
    print(f"Backup created: {BACKUP_HTML}")

  pdfs = []
  for root, _, files in os.walk("."):
    for fname in sorted(files):
      if fname.lower().endswith(".pdf"):
        full_path = os.path.join(root, fname)
        rel_path = os.path.relpath(full_path, ".").replace("\\", "/")
        pdfs.append({
            "name": fname,
            "path": rel_path,
            "subject": detect_subject(rel_path),
            "size": fmt_size(os.path.getsize(full_path)),
        })

  with open(EXISTING_HTML, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

  start_marker = "<!-- ADDED_PDF_SECTION_START -->"
  end_marker = "<!-- ADDED_PDF_SECTION_END -->"

  if start_marker in content and end_marker in content:
    s_idx = content.index(start_marker)
    e_idx = content.index(end_marker) + len(end_marker)
    content = content[:s_idx] + content[e_idx:]

  rows_html = []
  for p in pdfs:
    href = quote(p["path"], safe="/")
    safe_name = html_lib.escape(p["name"])
    safe_subj = html_lib.escape(p["subject"])
    safe_size = html_lib.escape(p["size"])
    search_blob = html_lib.escape(f"{p['name']} {p['subject']}".lower())
    subj_attr = html_lib.escape(p["subject"])

    rows_html.append(
        f'<li class="pdf-item-row" data-subject="{subj_attr}"'
        f' data-search="{search_blob}"'
        ' style="display:flex !important;justify-content:space-between;align-items:center;gap:12px;padding:10px'
        ' 14px;background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;margin-bottom:8px;">'
        f'<a href="{href}" target="_blank" rel="noopener"'
        ' style="text-decoration:none;color:#0f172a;font-weight:500;word-break:break-word;flex:1;">'
        '<span'
        ' style="display:inline-block;font-size:12px;font-weight:700;padding:2px'
        ' 8px;border-radius:999px;background:#dbeafe;color:#1d4ed8;margin-right:8px;">'
        f"{safe_subj}</span>"
        f"{safe_name}"
        "</a>"
        '<span'
        ' style="flex-shrink:0;font-size:12px;font-weight:600;padding:4px'
        ' 10px;border-radius:999px;background:#f1f5f9;color:#334155;">'
        f"{safe_size}</span>"
        "</li>"
    )

  pdf_block = f"""{start_marker}
<div id="compiled-pdfs-section" style="display:block !important;visibility:visible !important;opacity:1 !important;max-width:1020px;margin:20px auto 28px auto;padding:20px;border:2px solid #0f766e;border-radius:12px;background:#f8fafc;color:#0f172a;font-family:system-ui,-apple-system,sans-serif;">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px;">
    <div>
      <h2 style="margin:0;font-size:20px;color:#0f172a;">Compiled PDF Notes ({len(pdfs)})</h2>
      <p style="margin:4px 0 0;font-size:13px;color:#475569;">All scanned PDFs at top for quick access</p>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
      <button type="button" class="pdf-flt-btn" data-subj="All" style="padding:7px 12px;border-radius:8px;border:1px solid #0f766e;background:#0f766e;color:#ffffff;font-size:13px;font-weight:600;cursor:pointer;">All</button>
      <button type="button" class="pdf-flt-btn" data-subj="Biology" style="padding:7px 12px;border-radius:8px;border:1px solid #cbd5e1;background:#ffffff;color:#0f172a;font-size:13px;font-weight:600;cursor:pointer;">Biology</button>
      <button type="button" class="pdf-flt-btn" data-subj="Chemistry" style="padding:7px 12px;border-radius:8px;border:1px solid #cbd5e1;background:#ffffff;color:#0f172a;font-size:13px;font-weight:600;cursor:pointer;">Chemistry</button>
      <button type="button" class="pdf-flt-btn" data-subj="Physics" style="padding:7px 12px;border-radius:8px;border:1px solid #cbd5e1;background:#ffffff;color:#0f172a;font-size:13px;font-weight:600;cursor:pointer;">Physics</button>
      <button type="button" id="pdfToggleListBtn" style="padding:7px 12px;border-radius:8px;border:1px solid #475569;background:#e2e8f0;color:#0f172a;font-size:13px;font-weight:600;cursor:pointer;">Hide PDFs</button>
    </div>
  </div>
  <div style="margin-bottom:12px;">
    <input id="pdfQuickFilter" type="search" placeholder="PDF ya chapter search karein..." style="width:100%;max-width:360px;padding:8px 12px;border:1px solid #64748b;border-radius:8px;font-size:14px;background:#ffffff;color:#0f172a;">
  </div>
  <ul id="pdfStaticList" style="display:block !important;list-style:none;padding:0;margin:0;">
    {"".join(rows_html)}
  </ul>
</div>
<script>
(function() {{
  var activeSubj = "All";
  var isHidden = false;
  var inp = document.getElementById("pdfQuickFilter");
  var listEl = document.getElementById("pdfStaticList");
  var toggleBtn = document.getElementById("pdfToggleListBtn");
  var fltBtns = document.querySelectorAll("#compiled-pdfs-section .pdf-flt-btn");

  function applyFilter() {{
    if (!listEl) return;
    if (isHidden) {{
      listEl.style.setProperty("display", "none", "important");
      return;
    }}
    listEl.style.setProperty("display", "block", "important");
    var q = inp ? inp.value.trim().toLowerCase() : "";
    var rows = document.querySelectorAll("#pdfStaticList .pdf-item-row");
    for (var i = 0; i < rows.length; i++) {{
      var rowSubj = rows[i].getAttribute("data-subject") || "";
      var hay = rows[i].getAttribute("data-search") || "";
      var subjOk = (activeSubj === "All") || (rowSubj === activeSubj);
      var textOk = (!q) || (hay.indexOf(q) !== -1);
      rows[i].style.setProperty("display", (subjOk && textOk) ? "flex" : "none", "important");
    }}
  }}

  for (var j = 0; j < fltBtns.length; j++) {{
    fltBtns[j].addEventListener("click", function() {{
      activeSubj = this.getAttribute("data-subj") || "All";
      for (var k = 0; k < fltBtns.length; k++) {{
        var selected = fltBtns[k] === this;
        fltBtns[k].style.background = selected ? "#0f766e" : "#ffffff";
        fltBtns[k].style.color = selected ? "#ffffff" : "#0f172a";
        fltBtns[k].style.borderColor = selected ? "#0f766e" : "#cbd5e1";
      }}
      applyFilter();
    }});
  }}

  if (toggleBtn) {{
    toggleBtn.addEventListener("click", function() {{
      isHidden = !isHidden;
      toggleBtn.textContent = isHidden ? "Show PDFs" : "Hide PDFs";
      applyFilter();
    }});
  }}

  if (inp) {{
    inp.addEventListener("input", applyFilter);
  }}

  applyFilter();
}})();
</script>
{end_marker}
"""

  lower_content = content.lower()
  body_idx = lower_content.find("<body")
  if body_idx != -1:
    gt_idx = content.find(">", body_idx)
    if gt_idx != -1:
      updated = content[: gt_idx + 1] + "\n" + pdf_block + content[gt_idx + 1 :]
    else:
      updated = pdf_block + "\n" + content
  else:
    updated = pdf_block + "\n" + content

  with open(EXISTING_HTML, "w", encoding="utf-8") as f:
    f.write(updated)

  print(
      f"Done! Added {len(pdfs)} PDFs at the TOP of '{EXISTING_HTML}' with"
      " filter & toggle buttons."
  )


if __name__ == "__main__":
  main()