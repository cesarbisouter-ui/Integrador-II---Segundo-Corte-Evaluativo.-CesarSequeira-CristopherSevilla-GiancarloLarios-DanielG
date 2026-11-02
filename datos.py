from entidades import (
    Interaccion,
    PlatoTradicional,
    Restaurante,
    SolicitudEstablecimiento,
    Usuario,
)


# El catálogo inicial es contenido demostrativo; no representa una oferta de venta.
lista_platos = [
    PlatoTradicional(
        "P001",
        "Vigorón",
        "Tradicional",
        0,
        descripcion="Yuca cocida con chicharrón crujiente y ensalada de repollo.",
        categoria="Comida típica",
        ingredientes=["yuca", "chicharrón", "repollo", "tomate", "vinagre"],
        departamento="Granada",
        historia="Un clásico de Granada que suele disfrutarse en mercados y plazas.",
        combinaciones=["Chicha de maíz", "Cacao"],
        imagen="platos/vigoron.png",
    ),
    PlatoTradicional(
        "P002",
        "Indio viejo",
        "Tradicional",
        0,
        descripcion="Guiso espeso de maíz con carne, achiote y hierbabuena.",
        categoria="Comida típica",
        ingredientes=["maíz", "carne", "achiote", "hierbabuena", "naranja agria"],
        departamento="Managua",
        historia="Preparación de raíz indígena cuyo nombre y receta varían entre familias.",
        combinaciones=["Pinolillo"],
        imagen="platos/indio_viejo.jpg",
    ),
    PlatoTradicional(
        "P003",
        "Nacatamal",
        "Tradicional",
        0,
        descripcion="Masa de maíz rellena y cocida lentamente, envuelta en hojas.",
        categoria="Comida típica",
        ingredientes=["maíz", "cerdo", "arroz", "papa", "hojas de plátano"],
        departamento="León",
        historia="Tradición de fin de semana presente en distintas regiones del país.",
        combinaciones=["Cacao", "Café nicaragüense"],
    ),
    PlatoTradicional(
        "P004",
        "Gallo pinto",
        "Vegetariana",
        0,
        descripcion="Arroz y frijoles mezclados con hierbas y sazón casera.",
        categoria="Comida cotidiana",
        ingredientes=["arroz", "frijoles", "cebolla", "chiltoma", "culantro"],
        departamento="Masaya",
        historia="Acompañamiento cotidiano que forma parte de muchos desayunos nicaragüenses.",
        combinaciones=["Café nicaragüense"],
    ),
    PlatoTradicional(
        "P005",
        "Pinolillo",
        "Tradicional",
        0,
        descripcion="Bebida de maíz tostado y cacao, aromática y de sabor profundo.",
        categoria="Bebida",
        ingredientes=["maíz tostado", "cacao", "canela"],
        departamento="Matagalpa",
        historia="Bebida tradicional de origen ancestral, preparada con recetas familiares.",
        tipo="Bebida",
        combinaciones=["Indio viejo", "Vigorón"],
    ),
    PlatoTradicional(
        "P006",
        "Cacao",
        "Tradicional",
        0,
        descripcion="Bebida de cacao que puede servirse fría o caliente.",
        categoria="Bebida",
        ingredientes=["cacao", "leche o agua", "canela"],
        departamento="Rivas",
        historia="El cacao tiene una larga historia en la alimentación de Centroamérica.",
        tipo="Bebida",
        combinaciones=["Nacatamal", "Vigorón"],
    ),
    PlatoTradicional(
        "P007",
        "Ensalada de frutas",
        "Vegana",
        0,
        descripcion="Frutas frescas de temporada con un toque cítrico.",
        categoria="Postre",
        ingredientes=["papaya", "piña", "banano", "naranja"],
        departamento="Chinandega",
        historia="Una forma fresca de aprovechar la variedad de frutas tropicales.",
        tipo="Postre",
        combinaciones=["Cacao"],
    ),
]
platos_por_codigo = {plato.codigo: plato for plato in lista_platos}

lista_restaurantes: list[Restaurante] = []
restaurantes_por_codigo: dict[str, Restaurante] = {}

admin = Usuario(
    "U000",
    "Administración NicaCrave",
    "admin@nicacrave.com",
    "Omnívora",
    0,
    "admin",
    "1234",
    "Administrador",
)
recepcion = Usuario(
    "U001",
    "Personal de recepción",
    "recepcion@nicacrave.com",
    "Omnívora",
    0,
    "recepcion",
    "1234",
    "Recepción",
)
lista_usuarios = [admin, recepcion]
usuarios_por_codigo = {usuario.codigo: usuario for usuario in lista_usuarios}

lista_resenas = []
resenas_por_codigo = {}
lista_promociones = []
promociones_por_codigo = {}
lista_solicitudes: list[SolicitudEstablecimiento] = []
solicitudes_por_codigo: dict[str, SolicitudEstablecimiento] = {}
lista_interacciones: list[Interaccion] = []

# Se conserva el historial para mantener compatibilidad con la versión anterior.
historial_movimientos = []
