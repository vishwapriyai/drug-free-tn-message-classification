let currentPage = 1;
const rowsPerPage = 10;

function displayTable() {
  const table = document.getElementById("mainBody");
  const rows = Array.from(table.getElementsByTagName("tr"));

  const totalRows = rows.length;
  const totalPages = Math.ceil(totalRows / rowsPerPage);

  rows.forEach(row => row.style.display = "none");

  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;

  rows.slice(start, end).forEach(row => {
    row.style.display = "";
  });

  setupPagination(totalPages);
}

function setupPagination(totalPages) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.innerText = i;
    btn.classList.add("page-btn");

    if (i === currentPage) {
      btn.classList.add("active");
    }

    btn.onclick = () => {
      currentPage = i;
      displayTable();
    };

    pagination.appendChild(btn);
  }
}