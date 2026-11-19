import json
import os


def detect_subject(rel_path: str) -> str:
  low = rel_path.lower()
  parts = [p.lower() for p in rel_path.split(os.sep)]
  if "physics" in parts or any(k in low for k in ["phy", "physics"]):
    return "Physics"
  if "chemistry" in parts or any(k in low for k in ["chem", "chemistry"]):
    return "Chemistry"
  if "biology" in parts or any(k in low for k in ["bio", "biology"]):
    return "Biology"
  return "General"


def main():
  base_dir = "."
  items = []

  for root, _, files in os.walk(base_dir):
    for fname in sorted(files):
      if fname.lower().endswith(".pdf"):
        full_path = os.path.join(root, fname)
        rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
        subject = detect_subject(rel_path)
        items.append({
            "id": rel_path,
            "name": fname,
            "path": rel_path,
            "subject": subject,
            "size": os.path.getsize(full_path),
        })

  data_json = json.dumps(items, ensure_ascii=False)

  html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PCB Study Notes Hub</title>
  <style>
    *{{box-sizing:border-box}}
    html,body{{min-height:100vh;margin:0;padding:0}}
    body{{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f766e 100%);color:#f8fafc;padding:28px 18px}}
    .wrap{{max-width:980px;margin:0 auto}}
    .hero{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:16px;padding:22px;margin-bottom:20px;backdrop-filter:blur(8px)}}
    .eyebrow{{display:inline-block;font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#5eead4;background:rgba(45,212,191,.14);border:1px solid rgba(45,212,191,.3);padding:4px 10px;border-radius:999px;margin-bottom:8px}}
    h1{{font-size:1.65rem;margin:0 0 6px 0}}
    .meta{{font-size:.92rem;color:#cbd5e1}}
    .stats{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}
    .stat{{background:rgba(15,23,42,.55);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:8px 14px;font-size:.85rem;color:#e2e8f0}}
    .stat strong{{color:#5eead4}}
    .prog-wrap{{margin-top:14px}}
    .prog-track{{width:100%;height:8px;background:rgba(15,23,42,.65);border-radius:999px;overflow:hidden;border:1px solid rgba(255,255,255,.1)}}
    .prog-fill{{height:100%;width:0%;background:linear-gradient(90deg,#2dd4bf,#34d399);transition:width .25s ease}}
    .controls{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}}
    .tabs{{display:flex;flex-wrap:wrap;gap:8px}}
    .tab{{padding:8px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:rgba(15,23,42,.5);color:#e2e8f0;font-size:.88rem;font-weight:600;cursor:pointer;transition:all .15s ease}}
    .tab:hover{{border-color:#2dd4bf}}
    .tab.active{{background:#2dd4bf;color:#0f172a;border-color:#2dd4bf}}
    .right-ctrl{{display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
    #q{{width:100%;max-width:300px;padding:10px 14px;font-size:.96rem;border:1px solid rgba(255,255,255,.22);border-radius:10px;outline:none;background:rgba(15,23,42,.7);color:#f8fafc}}
    #q::placeholder{{color:#94a3b8}}
    #q:focus{{border-color:#2dd4bf;box-shadow:0 0 0 3px rgba(45,212,191,.22)}}
    .count{{font-size:.9rem;color:#cbd5e1;margin-bottom:12px}}
    ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}
    .row{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 16px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:10px;transition:all .15s ease}}
    .row:hover{{background:rgba(255,255,255,.12);border-color:rgba(45,212,191,.5)}}
    .row.done{{background:rgba(16,185,129,.12);border-color:rgba(52,211,153,.35)}}
    .row.done .fname{{text-decoration:line-through;color:#a7f3d0;opacity:.85}}
    .link-area{{display:flex;align-items:center;gap:10px;min-width:0;flex:1;text-decoration:none;color:#f8fafc;font-weight:500}}
    .link-area:hover .fname{{color:#5eead4}}
    .subj{{flex-shrink:0;font-size:.72rem;font-weight:700;padding:3px 9px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em}}
    .subj-Physics{{background:rgba(59,130,246,.22);color:#93c5fd;border:1px solid rgba(59,130,246,.4)}}
    .subj-Chemistry{{background:rgba(245,158,11,.22);color:#fcd34d;border:1px solid rgba(245,158,11,.4)}}
    .subj-Biology{{background:rgba(16,185,129,.22);color:#6ee7b7;border:1px solid rgba(16,185,129,.4)}}
    .subj-General{{background:rgba(148,163,184,.22);color:#cbd5e1;border:1px solid rgba(148,163,184,.35)}}
    .fname{{word-break:break-word}}
    .actions{{display:flex;align-items:center;gap:8px;flex-shrink:0}}
    .badge{{font-size:.78rem;font-weight:600;padding:4px 10px;border-radius:999px;background:rgba(45,212,191,.18);color:#5eead4;border:1px solid rgba(45,212,191,.35)}}
    .chk-btn{{display:inline-flex;align-items:center;gap:6px;padding:6px 11px;border-radius:8px;border:1px solid rgba(255,255,255,.2);background:rgba(15,23,42,.55);color:#e2e8f0;font-size:.8rem;font-weight:600;cursor:pointer;transition:all .15s ease}}
    .chk-btn:hover{{border-color:#34d399;color:#6ee7b7}}
    .row.done .chk-btn{{background:rgba(16,185,129,.25);border-color:#34d399;color:#6ee7b7}}
    .empty{{padding:16px;background:rgba(255,255,255,.07);border-radius:10px;color:#cbd5e1}}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <span class="eyebrow">Combined Study Hub</span>
      <h1>Physics, Chemistry &amp; Biology Notes</h1>
      <div class="meta">Shared by <strong>Vimal Kumar</strong> &bull; Track your study progress</div>
      <div class="stats">
        <div class="stat">Completed: <strong id="doneCount">0 / 0</strong> (<strong id="pctCount">0%</strong>)</div>
        <div class="stat">Remaining: <strong id="remCount">0</strong></div>
        <div class="stat">Total Size: <strong id="totSize">0 MB</strong></div>
      </div>
      <div class="prog-wrap">
        <div class="prog-track"><div class="prog-fill" id="progFill"></div></div>
      </div>
    </header>

    <div class="controls">
      <div class="tabs" id="tabs">
        <button class="tab active" data-subj="All">All</button>
        <button class="tab" data-subj="Physics">Physics</button>
        <button class="tab" data-subj="Chemistry">Chemistry</button>
        <button class="tab" data-subj="Biology">Biology</button>
        <button class="tab" data-subj="Completed">Completed</button>
        <button class="tab" data-subj="Pending">Pending</button>
      </div>
      <div class="right-ctrl">
        <input id="q" type="search" placeholder="Chapter ya PDF search karein..." autofocus>
      </div>
    </div>

    <div class="count" id="c"></div>
    <ul id="list"></ul>
  </div>

  <script>
    const STORAGE_KEY = "pcb_notes_completed_v1";
    const files = {data_json};
    let activeSubj = "All";
    let completedSet = new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"));

    const q = document.getElementById("q");
    const list = document.getElementById("list");
    const c = document.getElementById("c");
    const tabs = document.querySelectorAll(".tab");

    function saveCompleted() {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...completedSet]));
    }}

    function fmt(b) {{
      if (b < 1024) return b + " B";
      if (b < 1048576) return (b / 1024).toFixed(1) + " KB";
      return (b / 1048576).toFixed(2) + " MB";
    }}

    function encodePath(p) {{
      return p.split("/").map(encodeURIComponent).join("/");
    }}

    function updateHeaderStats() {{
      const total = files.length;
      const done = files.filter(f => completedSet.has(f.id)).length;
      const rem = total - done;
      const pct = total ? Math.round((done / total) * 100) : 0;
      const totalBytes = files.reduce((s, f) => s + f.size, 0);

      document.getElementById("doneCount").textContent = `${{done}} / ${{total}}`;
      document.getElementById("pctCount").textContent = `${{pct}}%`;
      document.getElementById("remCount").textContent = rem;
      document.getElementById("totSize").textContent = fmt(totalBytes);
      document.getElementById("progFill").style.width = `${{pct}}%`;
    }}

    tabs.forEach(btn => {{
      btn.addEventListener("click", () => {{
        tabs.forEach(t => t.classList.remove("active"));
        btn.classList.add("active");
        activeSubj = btn.dataset.subj;
        render();
      }});
    }});

    list.addEventListener("click", e => {{
      const btn = e.target.closest(".chk-btn");
      if (!btn) return;
      const id = btn.dataset.id;
      if (completedSet.has(id)) {{
        completedSet.delete(id);
      }} else {{
        completedSet.add(id);
      }}
      saveCompleted();
      updateHeaderStats();
      render();
    }});

    function render() {{
      const term = q.value.trim().toLowerCase();
      const filtered = files.filter(f => {{
        const isDone = completedSet.has(f.id);
        let tabMatch = true;
        if (activeSubj === "Completed") tabMatch = isDone;
        else if (activeSubj === "Pending") tabMatch = !isDone;
        else if (activeSubj !== "All") tabMatch = f.subject === activeSubj;

        const nameMatch = f.name.toLowerCase().includes(term) || f.subject.toLowerCase().includes(term);
        return tabMatch && nameMatch;
      }});

      c.textContent = `Showing ${{filtered.length}} of ${{files.length}} PDFs (${{activeSubj}})`;
      list.innerHTML = filtered.map(f => {{
        const isDone = completedSet.has(f.id);
        return `
          <li class="row ${{isDone ? "done" : ""}}">
            <a class="link-area" href="${{encodePath(f.path)}}" target="_blank" rel="noopener">
              <span class="subj subj-${{f.subject}}">${{f.subject}}</span>
              <span class="fname">${{f.name}}</span>
            </a>
            <div class="actions">
              <span class="badge">${{fmt(f.size)}}</span>
              <button type="button" class="chk-btn" data-id="${{f.id.replace(/"/g, "&quot;")}}">
                ${{isDone ? "✓ Completed" : "Mark Completed"}}
              </button>
            </div>
          </li>
        `;
      }}).join("") || '<li class="empty">Koi matching PDF nahi mili.</li>';
    }}

    q.addEventListener("input", render);
    updateHeaderStats();
    render();
  </script>
</body>
</html>
"""

  with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

  print(f"Done! Compiled {len(items)} PDFs into index.html")


if __name__ == "__main__":
  main()