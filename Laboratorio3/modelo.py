class Estudiante:
    """Clase que representa la entidad Estudiante dentro del sistema."""

    def __init__(self, student_id: int, nombre: str, edad: int, promedio: float):
        self.id = student_id  # Identificador único (clave primaria de búsqueda)
        self.nombre = nombre  # Nombre completo del estudiante
        self.edad = edad  # Edad en años
        self.promedio = promedio  # Promedio académico (0.0 - 5.0)

    def __str__(self):
        # Formato de salida para imprimir la información en la consola
        return f"[ID: {self.id}] Nombre: {self.nombre} | Edad: {self.edad} | Promedio: {self.promedio:.2f}"
