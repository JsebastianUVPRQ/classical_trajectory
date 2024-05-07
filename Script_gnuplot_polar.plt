set terminal pngcairo enhanced color 

set output "theta_vs_r.png"
set polar
set grid polar
set size square

# Define el estilo de la línea y el color
set style line 1 lt 1 lw 2 lc rgb "blue"

# Título del gráfico y etiquetas de los ejes
set title "Gráfico en coordenadas polares"
set xlabel "Ángulo (grados)"
set ylabel "Radio"

# Graficar los datos desde el archivo "Datos_Ed.dat"
plot "Datos_Ed.dat" using 3:2 with lines linestyle 1 title "Datos_Ed.dat"

unset output 
