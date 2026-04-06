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

    const payload = await response.json();

    if (!response.ok) {
      output.textContent = `Error ${response.status}: ${payload.description || "Unknown error"}`;
      return;
    }

    output.textContent = JSON.stringify(payload, null, 2);
  } catch (error) {
    output.textContent = `Network/client error: ${error}`;
  }
});
