const BACKEND = "http://127.0.0.1:8000"; // Replace with ngrok or deployed URL for production

document.getElementById("run").addEventListener("click", async () => {
  const inputText = document.getElementById("inputText").value.trim();
  const tone = document.getElementById("tone").value;
  const lang = document.getElementById("lang").value;
  const output = document.getElementById("output");

  if (!inputText) {
    output.textContent = "⚠️ Please enter text to process.";
    return;
  }

  output.textContent = "⏳ Processing...";

  try {
    const response = await fetch(`${BACKEND}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: inputText,
        tone: tone,
        target_lang: lang
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const result = await response.json();
    output.textContent = `
🌐 Language: ${result.original_language}
🔁 Translated: ${result.translated_input}

🧠 Summary (${tone}):
${result.rephrased_summary}

🏷️ Tags:
${JSON.stringify(result.tags, null, 2)}
    `.trim();
  } catch (error) {
    output.textContent = `❌ Error: ${error.message}`;
  }
});
