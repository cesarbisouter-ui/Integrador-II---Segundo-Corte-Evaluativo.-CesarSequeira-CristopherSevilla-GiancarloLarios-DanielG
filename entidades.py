from dataclasses import dataclass, field

@dataclass
class Restaurante:
    codigo: str
    nombre: str
    ubicacion: str
    especialidad: str
    mesas_libres: int = 0
    departamento: str = ""
    municipio: str = ""
    direccion: str = ""
    horario: str = ""
    contacto: str = ""
    descripcion: str = ""
    representante_codigo: str = ""
    estado: str = "Pendiente"
    observaciones: str = ""
    tipo: str = "Restaurante"

@dataclass
class Resena:
    codigo: str
    autor: str
    local_o_plato: str
    calificacion: int
    comentario: str
    likes: int = 0

@dataclass
class Promocion:
    codigo: str
    restaurante: str
    descripcion: str
    descuento_porcentaje: float
    cupones_disponibles: int = 0

@dataclass
class Usuario:
    codigo: str
    nombre: str
    correo: str
    dieta_preferida: str
    puntos_fidelidad: int = 0
    usuario: str = ""
    contraseña: str = ""
    rol: str = "Cliente"
    intereses: list[str] = field(default_factory=list)
    evitar_ingredientes: list[str] = field(default_factory=list)
    establecimiento_codigo: str = ""

@dataclass
class PlatoTradicional:
    codigo: str
    nombre: str
    dieta: str          # Ej: "Tradicional", "Vegetariano"
    precio: float
    disponibilidad: int = 0
    descripcion: str = ""
    categoria: str = "Platillo"
    ingredientes: list[str] = field(default_factory=list)
    departamento: str = ""
    historia: str = ""
    tipo: str = "Platillo"
    combinaciones: list[str] = field(default_factory=list)
    estado: str = "Publicado"
    imagen: str = ""

@dataclass
class SolicitudEstablecimiento:
    codigo: str
    restaurante_codigo: str
    representante_codigo: str
    tipo: str
    datos_propuestos: dict[str, str]
    estado: str = "Pendiente de revisión"
    observaciones: str = ""

@dataclass
class Interaccion:
    codigo: str
    usuario_codigo: str
    plato_codigo: str
    tipo: str
    calificacion: int = 0
    comentario: str = ""
    estado: str = "Registrada"