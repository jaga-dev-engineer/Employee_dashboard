// Employee directory: search worksheet rows and filter by work type or project.

const tableBody = document.getElementById("emp-table");
const employeeFields = [
  "serial_number", "employee_id", "name", "technical_skills", "yoe", "email",
  "doj_dep", "internal_external", "mapped_to_project", "billable_from",
  "client_name", "certification_name", "date_of_completion",
  "expected_date_of_completion", "profiles_uploaded", "contact_number",
];
let allEmployees = [];

function render() {
  const query = document.getElementById("search").value.toLowerCase();
  const workType = document.getElementById("work-type").value;
  const mapping = document.getElementById("mapping").value;

  const rows = allEmployees.filter(employee =>
    (!workType || employee.internal_external.toLowerCase() === workType.toLowerCase()) &&
    (!mapping || employee.mapped_to_project === mapping) &&
    Object.values(employee).join(" ").toLowerCase().includes(query));

  tableBody.innerHTML = rows.map(employee =>
    `<tr>${employeeFields.map(field => `<td>${esc(employee[field])}</td>`).join("")}</tr>`
  ).join("") || `<tr><td colspan="16" class="text-center text-muted">No employees match your filters</td></tr>`;

  document.getElementById("count").textContent = `${rows.length} of ${allEmployees.length} employees`;
}

function fillOptions(id, values, label) {
  const select = document.getElementById(id);
  const selected = select.value;
  select.innerHTML = `<option value="">${label}</option>`;
  [...new Set(values.filter(Boolean))].sort().forEach(value => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
  if ([...select.options].some(option => option.value === selected)) select.value = selected;
}

async function refreshEmployees() {
  try {
    allEmployees = await getJSON("/api/employees");
    fillOptions("mapping", allEmployees.map(employee => employee.mapped_to_project), "All project mappings");
    render();
    document.getElementById("error").classList.add("d-none");
  } catch (e) {
    showError(e.message);
    throw e;
  }
}

document.getElementById("search").addEventListener("input", render);
["work-type", "mapping"].forEach(id => document.getElementById(id).addEventListener("change", render));

async function initEmployees() {
  let initialVersion = null;
  try {
    initialVersion = (await getJSON("/api/dashboard/version")).version;
  } catch (error) {
    showError(error.message);
  }

  try {
    await refreshEmployees();
  } catch {
    initialVersion = null;
  }
  watchWorkbookChanges(refreshEmployees, initialVersion);
}

initEmployees();
