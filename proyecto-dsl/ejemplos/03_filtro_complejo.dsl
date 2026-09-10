# Ejemplo 3: expresión booleana con paréntesis, negación y operadores aritméticos
ventas = cargar "datos/ventas.csv"

ventas_filtradas = ventas
    |> seleccionar [ciudad, categoria, unidades, precio]
    |> filtrar donde (precio * unidades) >= 50000 y no (categoria == "descartado")
