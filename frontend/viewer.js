const viewer_table = document.querySelector(".viewer-table");
const file_filter_input = document.getElementById('file-filter');
const date_filter_input = document.getElementById('date-filter');
const provider_filter_input = document.getElementById('provider-filter');

// Función para filtrar la tabla por columna
function filterTable() {
    const file_filter_input_value = file_filter_input.value.toLowerCase();
    const date_filter_input_value = date_filter_input.value ? new Date(date_filter_input.value).toISOString().split('T')[0] : ''; // Formato YYYY-MM-DD
    const provider_filter_input_value = provider_filter_input.value.toLowerCase();
    const rows = document.querySelectorAll('.viewer-table tbody tr');

    rows.forEach(row => {
        const row_file = row.cells[0].textContent.toLowerCase();
        const row_date = new Date(row.cells[1].textContent).toISOString().split('T')[0]; // Formato YYYY-MM-DD
        const row_provider = row.cells[2].textContent.toLowerCase();

        // Condición de filtrado
        const show_row = (
            (file_filter_input_value === '' || row_file.includes(file_filter_input_value)) &&
            (date_filter_input_value === '' || row_date === date_filter_input_value) &&
            (provider_filter_input_value === '' || row_provider.includes(provider_filter_input_value))
        );

        row.style.display = show_row ? '' : 'none';
    });
}

function createNewRecord(file, date, provider) {
    const row = document.createElement("tr");

    // Crear las celdas de la nueva fila
    const cellFile = document.createElement("td");
    cellFile.textContent = file;
    row.appendChild(cellFile);

    const cellDate = document.createElement("td");
    cellDate.textContent = date;
    row.appendChild(cellDate);

    const cellProvider = document.createElement("td");
    cellProvider.textContent = provider;
    row.appendChild(cellProvider);

    // Agregar la nueva fila al final de la tabla
    viewer_table.querySelector("tbody").appendChild(row);
}

async function getFiles() {
    try {
        const response = await fetch("/api/files/get-files", {
            method: "GET",
        });

        const response_json = await response.json();

        if (response.ok) {
            response_json.data.forEach(file => {
                createNewRecord(file.name, file.date, file.provider);
            });
        }
        else throw new Error(`GET ${response.url} ${response.status} (${response.statusText})\n${response_json.error}`);

    } catch (error) {
        console.error(error.message);
    }
}

// Agregar eventos de entrada para los filtros
file_filter_input.addEventListener('input', filterTable);
date_filter_input.addEventListener('input', filterTable);
provider_filter_input.addEventListener('input', filterTable);
document.addEventListener('DOMContentLoaded', () => {getFiles();});