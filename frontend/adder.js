const file_form = document.querySelector(".file-form");
const file_input = document.querySelector(".file-input");
const file_table = document.querySelector(".file-table");

const file_table_message = document.querySelector(".file-table-message");
const spinner = document.querySelector(".spinner");

let uploaded_files = [];

function createFileRecord(file, file_date, file_provider) {
    const row = document.createElement("tr");

    // Nombre
    row.name = document.createElement("td");
    row.name.textContent = file.name;
    row.appendChild(row.name);

    // Fecha editable
    row.date = document.createElement("td");
    file_date = new Date(file.lastModified);
    row.date.input = document.createElement("input");
    row.date.input.type = "datetime-local"; // Usa un input para fecha/hora
    row.date.input.value = file_date.toISOString().slice(0, 16); // Formato ISO para "datetime-local"
    row.date.input.addEventListener("input", (event) => {
        row.date.input.classList.add("validated");
    });
    row.date.appendChild(row.date.input);
    row.appendChild(row.date);

    // Proveedor editable
    row.provider = document.createElement("td");
    row.provider.input = document.createElement("input");
    row.provider.input.type = "text"; // Usa un input de texto para el proveedor
    row.provider.input.value = file_provider;
    row.provider.input.placeholder = "proveedor";
    // row.provider.input.required = true;
    row.provider.input.addEventListener("input", (event) => {
        row.provider.input.classList.add("validated");
    });
    row.provider.appendChild(row.provider.input);
    row.appendChild(row.provider);

    // Estado
    row.state = document.createElement("td");
    row.state.wrapper = document.createElement("div");
    row.state.wrapper.classList.add("cell-wrapper");

    // Estado - Código (uso interno)
    row.state.code = 0;

    // Estado - Texto
    row.state.text = document.createElement("span");

    // Estado - SVG
    row.state.spinner = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    row.state.spinner.setAttribute("display", "none");
    row.state.spinner.setAttribute("class", "spinner");
    row.state.spinner.setAttribute("viewBox", "0 0 50 50");
    row.state.spinner.setAttribute("xmlns", "http://www.w3.org/2000/svg");

    const spinner_circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    spinner_circle.setAttribute("class", "spinner-circle");
    spinner_circle.setAttribute("cx", "25");
    spinner_circle.setAttribute("cy", "25");
    spinner_circle.setAttribute("r", "20");

    row.state.spinner.appendChild(spinner_circle);
    row.state.wrapper.appendChild(row.state.spinner);
    row.state.wrapper.appendChild(row.state.text);
    row.state.appendChild(row.state.wrapper);
    row.appendChild(row.state);

    // Acciones
    row.actions = document.createElement("td");
    row.actions.wrapper = document.createElement("div");
    row.actions.wrapper.classList.add("cell-wrapper");

    // Acciones - Validar
    row.actions.validate = document.createElement("button");
    row.actions.validate.textContent = "✅";
    row.actions.validate.type = "button";
    row.actions.validate.title = "Validar";
    row.actions.validate.addEventListener("click", () => {
        validateFileRecord(row);
    });

    // Acciones - Eliminar
    row.actions.delete = document.createElement("button");
    row.actions.delete.textContent = "🗑️";
    row.actions.delete.type = "button";
    row.actions.delete.title = "Eliminar";
    row.actions.delete.addEventListener("click", () => {
        uploaded_files = uploaded_files.filter(f => f !== file);
        row.remove();
        updateTable();
    });

    row.actions.wrapper.appendChild(row.actions.validate);
    row.actions.wrapper.appendChild(row.actions.delete);
    row.actions.appendChild(row.actions.wrapper);
    row.appendChild(row.actions);

    // Agregar la nueva fila a la tabla
    file_table.querySelector("tbody").appendChild(row);

    // Asocia la fila HTML al objeto del archivo
    file.row = row;
}

function updateTable() {
    const rows = file_table.querySelectorAll('tbody tr');

    if (rows.length > 0) {
        file_table.style.display = 'table';
        file_table_message.style.display = 'none';

    } else {
        file_table.style.display = 'none';
        file_table_message.style.display = 'flex';
    }
}

function updateFileRecordState(row, state) {
    switch (state) {
        case 1:
            row.state.text.textContent = "sin validar";
            row.state.code = 1;
            break;
        case 2:
            row.state.text.textContent = "validado";
            row.state.code = 2;
            break;
        case 3:
            row.state.text.textContent = "procesando...";
            row.state.code = 3;
            row.state.spinner.style.display = "block";
            break;
        case 4:
            row.state.text.textContent = "terminado";
            row.state.code = 4;
            row.state.spinner.style.display = "none";
            break;
        case 5:
            row.state.text.textContent = "error";
            row.state.code = 5;
            row.state.spinner.style.display = "none";
            break;
        default:
            row.state.text.textContent = "desconocido";
            row.state.code = 0;
    }
}

file_input.addEventListener("change", async () => {
    for (const file of Array.from(file_input.files)) {
        const already_exists = uploaded_files.some(f => f.name === file.name);

        if (!already_exists) {
            uploaded_files.push(file);

            createFileRecord(file, null, null);
            updateFileRecordState(file.row, 1);
            updateTable();
        }
    }

    file_input.value = "";
});

file_form.addEventListener("submit", event => {
    event.preventDefault();
    processFiles(uploaded_files);
});

function validateFileRecord(row) {
    if (row.provider.input.value !== "" && row.date.input.value !== "") {
        row.date.input.classList.add("validated");
        row.provider.input.classList.add("validated");
        updateFileRecordState(row, 2);
    }
}

async function processFiles(files) {
    for (const file of files) {
        if (file.row.state.code === 2) {
            updateFileRecordState(file.row, 3);

            const form_data = new FormData();
            // Añadir archivo, nombre, proveedor y fecha
            form_data.append("file", file);
            form_data.append("name", file.name);
            form_data.append("provider", file.row.provider.input.value);
            form_data.append("date", file.row.date.input.value);
    
            try {
                const response = await fetch("/api/files/add-file", {
                    method: "POST",
                    body: form_data,
                });

                const response_json = await response.json();

                if (response.ok) updateFileRecordState(file.row, 4);
                else throw new Error(`POST ${response.url} ${response.status} (${response.statusText})\n${response_json.error}`);

            } catch (error) {
                console.error(error.message);
                updateFileRecordState(file.row, 5);
            }
        }
    }
}