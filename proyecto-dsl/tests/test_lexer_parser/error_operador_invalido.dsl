# Error esperado: LÉXICO/SINTÁCTICO
# El operador "><" no existe en el lenguaje.
ventas = cargar "datos/ventas.csv"
    |> filtrar donde precio >< 0
