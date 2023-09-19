$(document).ready(function () {
    // Función para obtener valores únicos de una columna y llenar el desplegable
    function llenarDesplegable(columnIndex, selectElement) {
        var uniqueValues = []; // Utilizamos un array para almacenar valores únicos

        $("table tr:gt(0)").each(function () {
            var cellText = $(this).find("td").eq(columnIndex).text().trim();
            if (cellText !== "") {
                // Dividimos el contenido de la celda si contiene comas y agregamos los valores únicos al array
                var values = cellText.split(', ');
                values.forEach(function (value) {
                    if (!uniqueValues.includes(value)) {
                        uniqueValues.push(value);
                    }
                });
            }
        });

        // Ordena los valores únicos alfabéticamente
        uniqueValues.sort();

        // Llena el desplegable con los valores únicos ordenados y agrega "Todos"
        var select = $(selectElement);
        select.empty();
        select.append('<option value="todos">Todos</option>');
        uniqueValues.forEach(function (value) {
            select.append('<option value="' + value.toLowerCase() + '">' + value + '</option>');
        });
    }

    // Llena los desplegables al cargar la página
    llenarDesplegable(0, "#filter-jointType");
    llenarDesplegable(1, "#filter-jointType_type");
    llenarDesplegable(2, "#filter-connectionGroupType"); // Cambiado el ID
    llenarDesplegable(4, "#filter-project"); // Cambiado el índice de columna

    // Función para crear botones en la columna ConnectionGroup_Type
    function crearBotonesEnColumna() {
        $("table tr:gt(0)").each(function () {
            var cellText = $(this).find("td").eq(2).text().trim();
            if (cellText !== "") {
                // Crea un contenedor de botones
                var buttonsContainer = $('<div class="connection-group-buttons"></div>');

                // Crea un botón para cada valor en la celda
                var values = cellText.split(', ');
                for (var i = 0; i < values.length; i++) {
                    var value = values[i];
                    var button = $('<a href="/ctype/' + value + '" class="button">' + value + '</a>');
                    buttonsContainer.append(button);
                }

                // Reemplaza el contenido de la celda con el contenedor de botones
                $(this).find("td").eq(2).empty().append(buttonsContainer);
            }
        });
    }

    // Llama a crearBotonesEnColumna al cargar la página
    crearBotonesEnColumna();

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


