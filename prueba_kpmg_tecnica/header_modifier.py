import pandas as pd
import os
import re

class ExcelCleaner:
    def __init__(self, file_path):
        """
        Inicializa la clase con la ruta del archivo Excel.
        Verifica si el archivo existe y extrae el nombre base y el directorio.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no se encontró. Verifica la ruta y el nombre.")
        
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.dataframe = None

    def load_excel(self):
        """Carga el archivo Excel en un DataFrame de pandas sin encabezado."""
        self.dataframe = pd.read_excel(self.file_path, header=None)
        print(f"Archivo {self.file_path} cargado exitosamente.")

    def clean_column_names(self):
        """Limpia los nombres de las columnas del DataFrame según los requisitos."""
        if self.dataframe is None:
            raise ValueError("El DataFrame no se ha cargado")
        
        # Asignar nombres de columnas genéricos
        self.dataframe.columns = [f'Column{i+1}' for i in range(self.dataframe.shape[1])]
        
        # Realizar la limpieza de nombres de columnas
        self.dataframe.columns = self.dataframe.columns.str.strip()  # Eliminar espacios al inicio y al final
        self.dataframe.columns = self.dataframe.columns.str.replace(r'\s+', '_', regex=True)  # Reemplazar espacios intermedios con "_"
        self.dataframe.columns = self.dataframe.columns.str.replace(r'[^a-zA-Z0-9_]', '_', regex=True) #Eliminar caracteres especiales
        print("Nombres de columnas modificados correctamente.")
        
    def clean_rows(self):
        """Limpia los valores en todas las filas del DataFrame."""
        if self.dataframe is None:
            raise ValueError("El DataFrame no se ha cargado")
        
        # Remover espacios en blanco al inicio y al final de cada celda
        self.dataframe = self.dataframe.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Reemplazar espacios intermedios con ""
        self.dataframe = self.dataframe.applymap(lambda x: re.sub(r'\s+', '_', x) if isinstance(x, str) else x)
        
        # Eliminar caracteres especiales y reemplazarlos con "_"
        self.dataframe = self.dataframe.applymap(lambda x: re.sub(r'[^a-zA-Z0-9_]', '_', x) if isinstance(x, str) else x)

    def export_to_csv(self):
        """Exporta el DataFrame a un archivo CSV en el mismo directorio con nombres de columnas corregidos."""
        if self.dataframe is None:
            raise ValueError("El DataFrame no se ha cargado.")
        
        # Definir la ruta para el archivo CSV corregido
        output_file = os.path.join(self.directory, f"{self.file_name}_corregido.csv")
        
        # Exportar a CSV con punto y coma como delimitador y comillas para los valores
        self.dataframe.to_csv(output_file, index=False, sep=';', quoting=1)
        print("Archivo CSV con columnas corregidas guardado.")


if __name__ == "__main__":
    # Ruta del archivo Excel (esta misma carpeta)
    ruta_archivo_excel = "Punto 3_ Datos_muestra_prueba_tecnica.xlsx"
    
    # Crear instancia de ExcelCleaner
    cleaner = ExcelCleaner(ruta_archivo_excel)
    
    # Ejecutar los métodos para cargar, limpiar y exportar
    cleaner.load_excel()
    cleaner.clean_column_names()
    cleaner.clean_rows()
    cleaner.export_to_csv()
