$(document).ready(function () {
    // Función para obtener valores únicos de una columna y llenar el desplegable
    function llenarDesplegable(columnIndex, selectElement) {
        var uniqueValues = new Set(); // Utilizamos un conjunto (Set) para almacenar valores únicos

        $("table tr:gt(0)").each(function () {
            var cellText = $(this).find("td").eq(columnIndex).text().trim();
            if (cellText !== "") {
                // Dividimos el contenido de la celda si contiene comas y agregamos los valores únicos al conjunto
                var values = cellText.split(', ');
                values.forEach(function (value) {
                    uniqueValues.add(value);
                });
            }
        });

        // Llena el desplegable con los valores únicos y agrega "Todos"
        var select = $(selectElement);
        select.empty();
        select.append('<option value="todos">Todos</option>');
        uniqueValues.forEach(function (value) {
            select.append('<option value="' + value.toLowerCase() + '">' + value + '</option>');
        });
    }

    // Llena los desplegables al cargar la página
    llenarDesplegable(0, "#filter-Component");
    llenarDesplegable(1, "#filter-Status");

    // Función para manejar el evento de cambio en los desplegables
    $("select.filter-select").on("change", function () {
        // Crear un arreglo para almacenar los valores seleccionados en todos los filtros
        var selectedValues = [];

        // Iterar a través de los desplegables y obtener los valores seleccionados
        $("select.filter-select").each(function () {
            var columnIndex = $(this).data("column-index");
            var selectedValue = $(this).val().toLowerCase();
            if (selectedValue !== "todos") {
                selectedValues.push({ columnIndex: columnIndex, selectedValue: selectedValue });
            }
        });

        // Mostrar todas las filas
        $("table tr:gt(0)").show();

        // Iterar a través de los valores seleccionados y ocultar las filas que no coincidan
        selectedValues.forEach(function (selected) {
            var columnIndex = selected.columnIndex;
            var selectedValue = selected.selectedValue;
            $("table tr:gt(0)").each(function () {
                var cellText = $(this).find("td").eq(columnIndex).text().toLowerCase();
                if (cellText.indexOf(selectedValue) === -1) {
                    $(this).hide();
                }
            });
        });
    });

    // Función para manejar el evento de cambio en el filtro de entrada de texto "Composition"
    $("#filter-composition").on("input", function () {
        var filterValue = $(this).val().toLowerCase();

        // Iterar a través de las filas de la tabla y mostrar/ocultar según el filtro
        $("table tr:gt(0)").each(function () {
            var cellText = $(this).find("td").eq(3).text().toLowerCase();
            if (cellText.indexOf(filterValue) === -1) {
                $(this).hide();
            }
        });
    });
});
