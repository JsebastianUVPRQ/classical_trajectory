# presentacion_mecanica.py
from manim import *
from manim_slides import Slide

class MovimientoParabolico(Slide):
    def construct(self):
        # Slide 1: Introducción
        titulo = Text("Movimiento Parabólico", font_size=48, color=BLUE)
        ecuacion = MathTex("x(t) = v_0 \\cos(\\theta) t", font_size=36)
        ecuacion2 = MathTex("y(t) = v_0 \\sin(\\theta) t - \\frac{1}{2}gt^2", font_size=36)
        
        ecuacion.next_to(titulo, DOWN, buff=0.5)
        ecuacion2.next_to(ecuacion, DOWN, buff=0.3)
        
        self.play(Write(titulo))
        self.next_slide()
        self.play(Write(ecuacion), Write(ecuacion2))
        self.next_slide()
        
        # Slide 2: Animación del movimiento
        self.clear()
        
        # Crear ejes coordenados
        ejes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE}
        )
        
        # Parámetros iniciales
        v0 = 3
        theta = 60 * DEGREES
        g = 9.8
        
        # Función de trayectoria
        def trayectoria(t):
            return np.array([
                v0 * np.cos(theta) * t,
                v0 * np.sin(theta) * t - 0.5 * g * t**2,
                0
            ])
        
        # Crear la trayectoria
        curva = ejes.plot_parametric_curve(
            lambda t: trayectoria(t),
            t_range=[0, 0.8, 0.01],
            color=YELLOW
        )
        
        # Punto que representa el proyectil
        proyectil = Dot(color=RED, radius=0.08)
        
        # Vector velocidad
        velocidad_vector = always_redraw(lambda: Arrow(
            start=proyectil.get_center(),
            end=proyectil.get_center() + np.array([v0 * np.cos(theta), v0 * np.sin(theta) - g * self.t, 0]) * 0.5,
            color=GREEN,
            buff=0
        ))
        
        # Etiquetas
        titulo_anim = Text("Simulación del Movimiento", font_size=36, color=BLUE)
        titulo_anim.to_edge(UP)
        
        self.play(Write(titulo_anim))
        self.play(Create(ejes))
        self.next_slide()
        
        self.play(Create(curva))
        self.next_slide()
        
        # Animación del movimiento
        tiempo_max = 0.8
        self.play(
            MoveAlongPath(proyectil, curva, run_time=tiempo_max, rate_func=linear),
            Create(velocidad_vector),
            run_time=tiempo_max
        )
        self.next_slide()
        
        # Slide 3: Descomposición de vectores
        self.clear()
        
        titulo_vectores = Text("Descomposición Vectorial", font_size=36, color=BLUE)
        titulo_vectores.to_edge(UP)
        
        # Vectores componentes
        punto_inicial = Dot(color=WHITE)
        vector_completo = Arrow(
            start=ORIGIN,
            end=[3, 2, 0],
            color=RED,
            buff=0
        )
        
        vector_x = Arrow(
            start=ORIGIN,
            end=[3, 0, 0],
            color=BLUE,
            buff=0
        )
        
        vector_y = Arrow(
            start=[3, 0, 0],
            end=[3, 2, 0],
            color=GREEN,
            buff=0
        )
        
        # Etiquetas de vectores
        label_v = MathTex("\\vec{v}_0", color=RED).next_to(vector_completo, RIGHT)
        label_vx = MathTex("v_x = v_0 \\cos\\theta", color=BLUE).next_to(vector_x, DOWN)
        label_vy = MathTex("v_y = v_0 \\sin\\theta", color=GREEN).next_to(vector_y, RIGHT)
        
        grupo_vectores = VGroup(vector_completo, vector_x, vector_y, punto_inicial)
        grupo_vectores.move_to(ORIGIN)
        
        self.play(Write(titulo_vectores))
        self.next_slide()
        
        self.play(Create(punto_inicial))
        self.play(GrowArrow(vector_completo))
        self.play(Write(label_v))
        self.next_slide()
        
        self.play(GrowArrow(vector_x))
        self.play(Write(label_vx))
        self.next_slide()
        
        self.play(GrowArrow(vector_y))
        self.play(Write(label_vy))
        self.next_slide()
        
        # Slide 4: Pregunta de evaluación
        self.clear()
        
        pregunta = Text("Pregunta de Evaluación", font_size=36, color=BLUE)
        pregunta.to_edge(UP)
        
        texto_pregunta = Text(
            "¿En qué punto la velocidad vertical es cero?",
            font_size=24
        )
        texto_pregunta.next_to(pregunta, DOWN, buff=0.5)
        
        opciones = VGroup(
            Text("A) Al inicio del movimiento", font_size=20),
            Text("B) En el punto más alto de la trayectoria", font_size=20),
            Text("C) Al final del movimiento", font_size=20),
            Text("D) Nunca es cero", font_size=20)
        )
        
        opciones.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        opciones.next_to(texto_pregunta, DOWN, buff=0.5)
        
        self.play(Write(pregunta))
        self.next_slide()
        self.play(Write(texto_pregunta))
        self.next_slide()
        
        for opcion in opciones:
            self.play(Write(opcion))
            self.next_slide()
        
        # Respuesta correcta con animación
        respuesta_correcta = Text("¡Correcto! En el punto más alto, v_y = 0", color=GREEN, font_size=20)
        respuesta_correcta.next_to(opciones, DOWN, buff=0.5)
        
        # Resaltar opción correcta
        marco_correcto = SurroundingRectangle(opciones[1], color=GREEN, buff=0.1)
        
        self.play(Create(marco_correcto))
        self.play(Write(respuesta_correcta))
        self.next_slide()

class OsciladorArmonico(Slide):
    def construct(self):
        # Slide 1: Introducción al M.A.S.
        titulo = Text("Movimiento Armónico Simple", font_size=42, color=BLUE)
        ecuacion = MathTex("\\frac{d^2x}{dt^2} + \\omega^2 x = 0", font_size=36)
        solucion = MathTex("x(t) = A\\cos(\\omega t + \\phi)", font_size=36)
        
        ecuacion.next_to(titulo, DOWN, buff=0.5)
        solucion.next_to(ecuacion, DOWN, buff=0.3)
        
        self.play(Write(titulo))
        self.next_slide()
        self.play(Write(ecuacion))
        self.next_slide()
        self.play(Write(solucion))
        self.next_slide()
        
        # Slide 2: Animación del oscilador
        self.clear()
        
        # Sistema masa-resorte
        longitud_resorte = 3
        amplitud = 2
        omega = 2 * PI / 4  # Periodo de 4 segundos
        
        # Pared
        pared = Rectangle(height=2, width=0.2, color=WHITE, fill_opacity=1)
        pared.to_edge(LEFT)
        
        # Resorte
        def crear_resorte(posicion_x):
            return ParametricFunction(
                lambda t: np.array([
                    posicion_x + t * (longitud_resorte + amplitud * np.cos(omega * self.t)),
                    0.5 * np.sin(12 * PI * t),
                    0
                ]),
                t_range=[0, 1],
                color=YELLOW
            )
        
        # Masa
        masa = Square(side_length=0.8, color=RED, fill_opacity=0.8)
        
        # Actualizar posición en tiempo real
        def actualizar_masa(mob, dt):
            t = self.t
            x_pos = longitud_resorte + amplitud * np.cos(omega * t)
            mob.move_to([x_pos, 0, 0])
        
        masa.add_updater(actualizar_masa)
        
        self.add(pared, masa)
        self.play(Create(crear_resorte(0.2)))
        self.wait(4)  # Mostrar varios ciclos

# Archivo para ejecutar la presentación