const reset_db_button = document.getElementById("reset-db-button");

    reset_db_button.addEventListener("click", async () => {
        const confirm_reset = confirm("¿Estás seguro de que quieres resetear TODA la base de datos?");
        if (!confirm_reset) return;
        else {
            const message = await resetDB();
            alert(message);
        }
    });

async function resetDB() {
    try {
        const response = await fetch("/api/dev/db/reset", {
            method: "POST"
        });

        const response_json = await response.json();

        if (response.ok) {
            return response_json.message;
        }
        else throw new Error(`POST ${response.url} ${response.status} (${response.statusText})\n${response_json.error}`);

    } catch (error) {
        return error.message;
    }
}