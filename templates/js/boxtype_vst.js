$(document).ready(function () {
    var filtrosAplicados = {}; // Objeto para almacenar los valores filtrados por columna

    // Función para obtener valores únicos de una columna y llenar el desplegable
    function llenarDesplegable(columnIndex, selectElement) {
        var uniqueValues = [];

        $("table tr:gt(0):visible").each(function () {
            var cellText = $(this).find("td").eq(columnIndex).text().trim();
            if (cellText !== "") {
                var values = cellText.split(', ');
                values.forEach(function (value) {
                    if (!uniqueValues.includes(value)) {
                        uniqueValues.push(value);
                    }
                });
            }
        });

        uniqueValues.sort();

        var select = $(selectElement);
        var filtroActual = filtrosAplicados[columnIndex];

        select.empty();
        select.append('<option value="todos">Todos</option>');
        uniqueValues.forEach(function (value) {
            select.append('<option value="' + value.toLowerCase() + '">' + value + '</option>');
        });

        // Establecer el valor del filtro actual o "todos" por defecto
        if (filtroActual !== undefined) {
            select.val(filtroActual);
        } else {
            select.val('todos');
        }
    }

    // Función para manejar el evento de cambio en los desplegables
    $("select.filter-select").on("change", function () {
        var selectedValues = {};

        $("select.filter-select").each(function () {
            var columnIndex = $(this).data("column-index");
            var selectedValue = $(this).val().toLowerCase();
            if (selectedValue !== "todos") {
                selectedValues[columnIndex] = selectedValue;
            } else {
                delete filtrosAplicados[columnIndex]; // Eliminar el filtro si se selecciona "todos"
            }
        });

        $("table tr:gt(0)").show();

        // Aplicar los filtros seleccionados
        Object.keys(selectedValues).forEach(function (columnIndex) {
            var selectedValue = selectedValues[columnIndex];
            $("table tr:gt(0)").each(function () {
                var cellText = $(this).find("td").eq(columnIndex).text().toLowerCase();
                // Comparación exacta en lugar de verificar si el texto de la celda contiene el valor del filtro
                if (cellText !== selectedValue) {
                    $(this).hide();
                }
            });
            filtrosAplicados[columnIndex] = selectedValue; // Guardar el valor filtrado por columna
        });

        actualizarDesplegables(); // Actualizar los desplegables después de filtrar
    });

    // Función para actualizar los desplegables
    function actualizarDesplegables() {
        llenarDesplegable(0, "#filter-cgt");
        llenarDesplegable(1, "#filter-cgclass");
        llenarDesplegable(2, "#filter-desc");
        llenarDesplegable(3, "#filter-screwlong");
        llenarDesplegable(4, "#filter-screwcadence");
        llenarDesplegable(5, "#filter-angletype");
        llenarDesplegable(6, "#filter-anglecadence");
    }

    // Llenar los desplegables al cargar la página inicialmente
    actualizarDesplegables();
});
