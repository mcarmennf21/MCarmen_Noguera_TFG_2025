## **SECCIÓN 1 — MUESTRAS**

1. **Studies_Athaliana.txt**: Archivo de texto con columnas tabuladas que contiene todas las muestras recopiladas para el proyecto.
2. **samples_reproducibility/**: Carpeta con los archivos de entrada para el cálculo de reproducibilidad de RC entre pares de muestras.
3. **Samples.xlsx**: Archivo Excel recopilatorio con las muestras seleccionadas utilizadas para los gráficos de reproducibilidad de RC.

## **SECCIÓN 2 — REPRODUCIBILIDADES**

1. **intersection_genome_wrapper.py**: Script que mapea al genoma las lecturas y llama a las funciones que calculan la intersección.
2. **get_intersection.py**: Script con los cálculos de la intersección.
3. **plot_intersection.py**: Script que genera los gráficos con la reproducibilidad de las lecturas entre pares de muestras.
4. **reproducibility_dataframes_RC/**: Carpeta con los archivos de salida que contienen las intersecciones y uniones calculadas entre pares de muestras.
5. **reproducibility_plots_RC/**: Carpeta con los gráficos que representan la reproducibilidad de las lecturas entre pares de muestras.
6. **generate_reproducibilities_dataframe_UR.py**: Script que calcula la reproducibilidad de las lecturas como únicas (UR) entre todas las muestras.
7. **generate_reproducibilities_boxplot_UR.py**: Script que genera los gráficos con la reproducibilidad de las UR entre todas las muestras.
8. **reproducibility_dataframe_plot_UR/**: Carpeta con el *dataframe* y el gráfico que representa la reproducibilidad de las UR entre todas las muestras.

## **SECCIÓN 3 — FRECUENCIAS**

1. **generate_frecuencies_dataframe.py**: Script para generar el *dataframe* con las frecuencias de todas las muestras.
2. **generate_frecuencies_boxplot.py**: Script para generar el *boxplot* con las frecuencias de todas las muestras.
3. **Samples_frecuencies.xlsx**: Archivo Excel con las frecuencias para cada longitud de lectura por muestra representadas en gráficos de barras.
4. **all_samples_frecuencies/**: Carpeta con los gráficos interactivos que representan las frecuencias para cada longitud de lectura en todas las muestras.

## **SECCIÓN 4 — EXTRACCIÓN DE LECTURAS**

1. **make_read_level_dict.py**: Script que genera un diccionario anidado en formato JSON con todas las lecturas del trabajo, las muestras en las que se encuentran y el número de copias en estas.
2. **make_read_stat.py**: Script para almacenar todas las lecturas y el número de muestras en las que se encuentran.
3. **get_fasta_files.py**: Script que almacena las lecturas según su porcentaje de longitud y reproducibilidad en archivos tipo FASTA.

## **SECCIÓN 5 — IDENTIDADES**

1. **Libreries.md**: Librerías utilizadas para asignar identidad a las lecturas.
2. **identities_dataframe_plot/**: Carpeta con el *dataframe* y el gráfico con la asignación de identidades genómicas a las lecturas.
3. **identities_graphic_sRNA.py**: Script que recoge y grafica las identidades genómicas asignadas a las lecturas.
