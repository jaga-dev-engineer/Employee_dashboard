// Dashboard page: workbook summary, project mappings and worksheet rows.

const employeeFields = [
  "serial_number", "employee_id", "name", "technical_skills", "yoe", "email",
  "doj_dep", "internal_external", "mapped_to_project", "billable_from",
  "client_name", "certification_name", "date_of_completion",
  "expected_date_of_completion", "profiles_uploaded", "contact_number",
];

async function loadSummary() {
  const summary = await getJSON("/api/dashboard/summary");
  document.getElementById("stat-total").textContent = summary.total_employees;
  document.getElementById("stat-mapped").textContent = summary.mapped_employees;
  document.getElementById("stat-internal").textContent = summary.internal_employees;
  document.getElementById("stat-external").textContent = summary.external_employees;
}

async function loadMappingTable() {
  const items = await getJSON("/api/dashboard/project-mapping");
  document.getElementById("mapping-table").innerHTML =
    items.map(item => `<tr><td>${esc(item.label)}</td><td class="text-end">${item.count}</td></tr>`).join("")
    || `<tr><td colspan="2" class="text-muted">No data</td></tr>`;
}

async function loadEmployeeTable() {
  const employees = await getJSON("/api/employees");
  document.getElementById("employee-table").innerHTML = employees.map(employee =>
    `<tr>${employeeFields.map(field => `<td>${esc(employee[field])}</td>`).join("")}</tr>`
  ).join("") || `<tr><td colspan="16" class="text-center text-muted">No employee data</td></tr>`;
}

async function refreshDashboard() {
  const error = document.getElementById("error");
  try {
    await Promise.all([loadSummary(), loadMappingTable(), loadEmployeeTable()]);
    error.classList.add("d-none");
    document.getElementById("last-updated").textContent =
      `Data refreshed ${new Date().toLocaleTimeString()}`;
  } catch (e) {
    showError(e.message);
    throw e;
  }
}

async function initDashboard() {
  let initialVersion = null;
  try {
    initialVersion = (await getJSON("/api/dashboard/version")).version;
  } catch (error) {
    showError(error.message);
  }

  try {
    await refreshDashboard();
  } catch {
    initialVersion = null;
  }
  watchWorkbookChanges(refreshDashboard, initialVersion);
}

document.getElementById("refresh-dashboard").addEventListener("click", () =>
  refreshDashboard().catch(() => {}));
initDashboard();
