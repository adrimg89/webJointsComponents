$(document).ready(function () {
    // Función para obtener valores únicos de una columna y llenar el desplegable
    function llenarDesplegable(columnIndex, selectElement) {
        var uniqueValues = new Set();

        $("table tr:gt(0)").each(function () {
            var cellText = $(this).find("td").eq(columnIndex).text().trim();
            if (cellText !== "") {
                var values = cellText.split(', ');
                values.forEach(function (value) {
                    uniqueValues.add(value);
                });
            }
        });

        var select = $(selectElement);
        select.empty();
        select.append('<option value="todos">Todos</option>');
        uniqueValues.forEach(function (value) {
            select.append('<option value="' + value.toLowerCase() + '">' + value + '</option>');
        });
    }

    // Llena los desplegables al cargar la página
    llenarDesplegable(1, "#filter-Status");

    // Función para manejar el evento de cambio en los desplegables
    $("select.filter-select").on("change", function () {
        actualizarFiltros();
    });

    // Función para manejar el evento de cambio en los filtros de entrada de texto
    $("#filter-description, #filter-Component").on("input", function () {
        actualizarFiltros();
    });

    // Función para actualizar los filtros
    function actualizarFiltros() {
        // Obtener los valores de los filtros de Description y Component
        var descriptionFilter = $("#filter-description").val().toLowerCase();
        var componentFilter = $("#filter-Component").val().toLowerCase();
        var statusFilter = $("#filter-Status").val().toLowerCase();

        $("table tr:gt(0)").each(function () {
            var descriptionText = $(this).find("td").eq(2).text().toLowerCase();
            var componentText = $(this).find("td").eq(0).text().toLowerCase();
            var statusText = $(this).find("td").eq(1).text().toLowerCase();

            var descriptionMatch = descriptionText.includes(descriptionFilter) || descriptionFilter === "";
            var componentMatch = componentText.includes(componentFilter) || componentFilter === "";
            var statusMatch = statusFilter === "todos" || statusText.includes(statusFilter);

            // Mostrar u ocultar la fila según los filtros
            if (descriptionMatch && componentMatch && statusMatch) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});
