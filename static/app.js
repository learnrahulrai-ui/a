const form = document.getElementById("analyze-form");
const output = document.getElementById("output");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  output.textContent = "Uploading and analyzing... please wait.";

  const formData = new FormData(form);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
      credentials: "same-origin",
    });

    let payload;
    try {
      payload = await response.json();
    } catch (parseError) {
      output.textContent = `Error: Server returned invalid response (${response.status}). Please try again.`;
      return;
    }

    if (!response.ok) {
      output.textContent = `Error ${response.status}: ${payload.description || "Unknown error"}`;
      return;
    }

    output.textContent = JSON.stringify(payload, null, 2);
  } catch (error) {
    output.textContent = `Network/client error: ${error}`;
  }
});
