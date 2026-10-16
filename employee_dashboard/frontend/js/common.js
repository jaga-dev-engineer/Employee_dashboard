// Helpers shared by every page.

function esc(value) {
  const d = document.createElement("div");
  d.textContent = value;
  return d.innerHTML;
}

async function getJSON(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (res.status === 401) {
    window.location.assign("/login");
    throw new Error("Your session has expired. Please sign in again.");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

function showError(message) {
  const box = document.getElementById("error");
  box.textContent = message;
  box.classList.remove("d-none");
}

function watchWorkbookChanges(onChange, initialVersion) {
  let currentVersion = initialVersion;
  let checking = false;

  window.setInterval(async () => {
    if (checking) return;
    checking = true;
    try {
      const data = await getJSON("/api/dashboard/version");
      if (currentVersion === null || data.version !== currentVersion) {
        await onChange();
        currentVersion = data.version;
      }
    } catch (error) {
      showError(error.message);
    } finally {
      checking = false;
    }
  }, 10000);
}

document.getElementById("logout").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/auth/logout", { method: "POST", cache: "no-store" });
    if (!response.ok) throw new Error("Sign out failed. Please try again.");
    window.location.assign("/login");
  } catch (error) {
    showError(error.message);
  }
});
