import os
import re
import pandas as pd


class ExcelCleaner:
    SPECIAL_CHARS_REGEX = r"[^A-Za-z0-9_]"
    
    def __init__(self, file_path):
        """
        Inicializa la clase con la ruta del archivo Excel.
        Verifica si el archivo existe y extrae el nombre y el directorio.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no se encontró. Verifica la ruta y el nombre.")
        
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.dataframe = None

    def load_excel(self):
        """Carga el archivo de Excel en un DataFrame"""
        self.dataframe = pd.read_excel(self.file_path, header=None)
        self.dataframe.columns = [f"Column_{i}" for i in range(self.dataframe.shape[1])]
        print("Archivo de Excel cargado correctamente.")

    def clean_column_names(self):
        """Limpia los nombres de las columnas del DataFrame eliminando caracteres especiales y espacios."""
        self.dataframe.columns = self.dataframe.columns.str.strip()
        self.dataframe.columns = self.dataframe.columns.str.replace(r"\s+", "_", regex=True)
        self.dataframe.columns = self.dataframe.columns.str.replace(self.SPECIAL_CHARS_REGEX, "", regex=True)
        print("Nombres de columnas modificados correctamente.")

    def clean_values(self):
        """Modifica los strings en todas las filas del DataFrame eliminando caracteres especiales y espacios."""
        def clean_value(value):
            if isinstance(value, str):
                value = value.strip()
                value = re.sub(r'[^\wÁÉÍÓÚáéíóúñÑ]', '_', value)
                return value.strip()
            return value
        
        self.dataframe = self.dataframe.applymap(clean_value)
        print("Valores de filas modificados exitosamente.")

    def export_to_csv(self):
        """El resultado de la limpieza se exporta a un archivo CSV
        de la forma {nombre_archivo}_corregido.csv
        Se guarda en el mismo directorio del archivo Excel"""
        # Definir la ruta para guardar el resultado
        output_file = os.path.join(self.directory, f"{self.file_name}_corregido.csv")
        
        # Exportar a CSV con punto y coma como delimitador
        self.dataframe.to_csv(output_file, sep=";", index=False)


# Función principal
if __name__ == "__main__":

    Excel_file = "Punto 3_ Datos_muestra_prueba_tecnica.xlsx"
    
    # Crear una instancia de la clase ExcelCleaner
    cleaner = ExcelCleaner(Excel_file)

    cleaner.load_excel()
    cleaner.clean_column_names()
    cleaner.clean_values()
    cleaner.export_to_csv()
    print("Ejecución finalizada. Revisa el archivo CSV corregido.")



