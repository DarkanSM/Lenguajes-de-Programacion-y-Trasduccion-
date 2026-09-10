# Ejemplo 2: seleccionar columnas y filtrar filas de ventas válidas
ventas = cargar "datos/ventas.csv"

ventas_limpias = ventas
    |> seleccionar [fecha, ciudad, categoria, unidades, precio]
    |> filtrar donde unidades > 0 y precio > 0
