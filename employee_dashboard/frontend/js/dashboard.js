// Dashboard page: workbook summary, location chart, mapping totals and all employees.

async function loadSummary() {
  const summary = await getJSON("/api/dashboard/summary");
  document.getElementById("stat-total").textContent = summary.total_employees;
  document.getElementById("stat-mapped").textContent = summary.mapped_employees;
  document.getElementById("stat-locations").textContent = summary.locations;
  document.getElementById("stat-email").textContent = summary.employees_with_email;
}

let locationChart;
async function loadLocationChart() {
  const items = await getJSON("/api/dashboard/by-location");
  if (locationChart) locationChart.destroy();
  locationChart = new Chart(document.getElementById("locationChart"), {
    type: "bar",
    data: {
      labels: items.map(item => item.label),
      datasets: [{ label: "Employees", data: items.map(item => item.count), backgroundColor: "#2f6fdb", borderRadius: 4 }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
    },
  });
}

async function loadMappingTable() {
  const items = await getJSON("/api/dashboard/project-mapping");
  document.getElementById("mapping-table").innerHTML =
    items.map(item => `<tr><td>${esc(item.label)}</td><td class="text-end">${item.count}</td></tr>`).join("")
    || `<tr><td colspan="2" class="text-muted">No data</td></tr>`;
}

async function loadEmployeeTable() {
  const employees = await getJSON("/api/employees");
  document.getElementById("employee-table").innerHTML = employees.map(employee => `<tr>
    <td>${esc(employee.serial_number)}</td><td>${esc(employee.employee_id)}</td>
    <td>${esc(employee.name)}</td><td>${esc(employee.email)}</td>
    <td>${esc(employee.mapped_to_project)}</td><td>${esc(employee.location)}</td>
    <td>${esc(employee.contact_number)}</td>
  </tr>`).join("") || `<tr><td colspan="7" class="text-center text-muted">No employee data</td></tr>`;
}

async function refreshDashboard() {
  const error = document.getElementById("error");
  try {
    await Promise.all([loadSummary(), loadLocationChart(), loadMappingTable(), loadEmployeeTable()]);
    error.classList.add("d-none");
    document.getElementById("last-updated").textContent =
      `Data refreshed ${new Date().toLocaleTimeString()}`;
  } catch (e) {
    showError(e.message);
  }
}

document.getElementById("refresh-dashboard").addEventListener("click", refreshDashboard);
refreshDashboard();
setInterval(refreshDashboard, 60000);
