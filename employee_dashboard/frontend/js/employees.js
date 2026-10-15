// Employee directory: search the workbook rows and filter by location or project mapping.

const tableBody = document.getElementById("emp-table");
let allEmployees = [];

function render() {
  const query = document.getElementById("search").value.toLowerCase();
  const location = document.getElementById("loc").value;
  const mapping = document.getElementById("mapping").value;

  const rows = allEmployees.filter(employee =>
    (!location || employee.location === location) &&
    (!mapping || employee.mapped_to_project === mapping) &&
    Object.values(employee).join(" ").toLowerCase().includes(query));

  tableBody.innerHTML = rows.map(employee => `<tr>
    <td>${esc(employee.serial_number)}</td><td>${esc(employee.employee_id)}</td>
    <td>${esc(employee.name)}</td><td>${esc(employee.email)}</td>
    <td>${esc(employee.mapped_to_project)}</td><td>${esc(employee.location)}</td>
    <td>${esc(employee.contact_number)}</td>
  </tr>`).join("") || `<tr><td colspan="7" class="text-center text-muted">No employees match your filters</td></tr>`;

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
    fillOptions("loc", allEmployees.map(employee => employee.location), "All locations");
    fillOptions("mapping", allEmployees.map(employee => employee.mapped_to_project), "All project mappings");
    render();
    document.getElementById("error").classList.add("d-none");
  } catch (e) {
    showError(e.message);
  }
}

document.getElementById("search").addEventListener("input", render);
["loc", "mapping"].forEach(id => document.getElementById(id).addEventListener("change", render));
refreshEmployees();
setInterval(refreshEmployees, 60000);
