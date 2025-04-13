if (!document.getElementById("textintel-sidebar")) {
  const wrapper = document.createElement("div");
  wrapper.id = "textintel-sidebar";
  wrapper.innerHTML = `
    <div style="
      position: fixed;
      top: 0;
      right: 0;
      width: 360px;
      height: 100%;
      background: #ffffff;
      border-left: 2px solid #ccc;
      z-index: 999999;
      box-shadow: -2px 0 10px rgba(0,0,0,0.2);
      font-family: 'Segoe UI', sans-serif;
      padding: 12px;
      overflow-y: auto;
    ">
      <h2 style="color: #4b4bff; font-weight: bold;">🧠 TextIntel</h2>
      <textarea id="textintel-input" placeholder="Paste or select text..." style="width:100%;height:120px;padding:10px;font-size:14px;border:1px solid #ccc;border-radius:6px;"></textarea>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <button onclick="textIntel('summary')">📝 Summarize</button>
        <button onclick="textIntel('keywords')">🔑 Keywords</button>
        <button onclick="textIntel('translate')">🌐 Translate</button>
      </div>
      <pre id="textintel-output" style="white-space:pre-wrap;font-size:13px;margin-top:14px;background:#f9f9f9;padding:10px;border-radius:5px;"></pre>
    </div>
    <style>
      button {
        flex: 1;
        padding: 8px 10px;
        background: #4b4bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }
      button:hover {
        background: #3a3aff;
      }
    </style>
    <script>
      async function textIntel(type) {
        const input = document.getElementById("textintel-input").value;
        if (!input) return;
        const res = await fetch("http://127.0.0.1:8000/" + type, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: input })
        });
        const result = await res.json();
        document.getElementById("textintel-output").textContent = JSON.stringify(result, null, 2);
      }
    </script>
  `;
  document.body.appendChild(wrapper);
}
