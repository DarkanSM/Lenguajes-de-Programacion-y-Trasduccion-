# Ejemplo 4: sentencia graficar — en el Corte 1 solo se valida
# que la sintaxis sea correcta, no se genera ninguna imagen todavía.
resumen = cargar "datos/resumen_ciudades.csv"

graficar barras resumen
    x ciudad
    y ingreso
    titulo "Ingresos por ciudad"
    guardar como "salidas/ingresos_ciudad.svg"
