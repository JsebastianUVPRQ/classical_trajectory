# run_presentation.py
from manim_slides import Slide, ThreeDSlide
import mec_clas_manim_quices  # Asegúrate de que este archivo esté en el mismo directorio
from manim_slides import convert

# Para renderizar y convertir a HTML
if __name__ == "__main__":
    # Renderizar las escenas
    import os
    os.system("manim -ql presentacion_mecanica.py MovimientoParabolico")
    os.system("manim -ql presentacion_mecanica.py OsciladorArmonico")
    
    # Convertir a presentación HTML
    convert("mec_clas_manim_quices.MovimientoParabolico", "iframe")