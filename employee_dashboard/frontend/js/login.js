const form = document.getElementById("login-form");
const errorBox = document.getElementById("login-error");
const submitButton = document.getElementById("login-button");

form.addEventListener("submit", async event => {
  event.preventDefault();
  errorBox.classList.add("d-none");
  submitButton.disabled = true;

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      }),
      cache: "no-store",
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || "Sign in failed.");
    window.location.assign(body.redirect_url);
  } catch (error) {
    errorBox.textContent = error.message || "Unable to sign in. Please try again.";
    errorBox.classList.remove("d-none");
  } finally {
    submitButton.disabled = false;
  }
});
