import unicodedata

from datos import (
    historial_movimientos,
    lista_interacciones,
    lista_platos,
    lista_restaurantes,
    lista_solicitudes,
    lista_usuarios,
    platos_por_codigo,
    restaurantes_por_codigo,
    solicitudes_por_codigo,
    usuarios_por_codigo,
)
from entidades import (
    Interaccion,
    PlatoTradicional,
    Restaurante,
    SolicitudEstablecimiento,
    Usuario,
)
from validaciones import (
    validar_contrasena,
    validar_correo,
    validar_lista_separada,
    validar_nombre,
    validar_telefono,
    validar_texto,
    validar_usuario,
)


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))


def _siguiente_codigo(prefijo: str, elementos: list) -> str:
    return f"{prefijo}{len(elementos) + 1:03d}"


def registrar_usuario(codigo, nombre, correo, dieta_preferida, puntos, usuario_login, contraseña, rol):
    if codigo in usuarios_por_codigo:
        return False
    if any(
        usuario.usuario.casefold() == usuario_login.casefold()
        or usuario.correo.casefold() == correo.casefold()
        for usuario in lista_usuarios
    ):
        return False

    nuevo_usuario = Usuario(codigo, nombre, correo, dieta_preferida, puntos, usuario_login, contraseña, rol)
    lista_usuarios.append(nuevo_usuario)
    usuarios_por_codigo[codigo] = nuevo_usuario
    historial_movimientos.append(
        {"tipo": "REGISTRO USUARIO", "codigo": codigo, "cantidad": puntos}
    )
    return True


def crear_usuario(nombre, correo, dieta_preferida, usuario_login, contraseña, rol="Cliente"):
    errores = (
        validar_nombre(nombre),
        validar_correo(correo),
        validar_usuario(usuario_login),
        validar_contrasena(contraseña),
        validar_texto(rol, "El rol", maximo=30),
    )
    if any(errores):
        return None
    if dieta_preferida not in {
        "Omnívora",
        "Tradicional",
        "Vegetariana",
        "Vegana",
        "Sin gluten",
    }:
        return None
    if rol not in {
        "Cliente",
        "Representante",
        "Recepción",
        "Editor",
        "Administrador",
    }:
        return None
    codigo = _siguiente_codigo("U", lista_usuarios)
    if not registrar_usuario(
        codigo, nombre.strip(), correo.strip(), dieta_preferida, 0,
        usuario_login.strip(), contraseña, rol,
    ):
        return None
    return usuarios_por_codigo[codigo]


def obtener_directorio_usuarios():
    return lista_usuarios


def actualizar_perfil(usuario, nombre, correo):
    if not isinstance(nombre, str) or not isinstance(correo, str):
        return False
    nombre = nombre.strip()
    correo = correo.strip()
    if validar_nombre(nombre) or validar_correo(correo):
        return False
    if any(
        cuenta.codigo != usuario.codigo
        and cuenta.correo.casefold() == correo.casefold()
        for cuenta in lista_usuarios
    ):
        return False
    usuario.nombre = nombre
    usuario.correo = correo
    historial_movimientos.append(
        {"tipo": "ACTUALIZAR PERFIL", "codigo": usuario.codigo}
    )
    return True


def listar_platos(busqueda="", dieta="", departamento="", tipo=""):
    resultados = [plato for plato in lista_platos if plato.estado == "Publicado"]
    if busqueda.strip():
        termino = _normalizar(busqueda.strip())
        resultados = [
            plato
            for plato in resultados
            if termino in _normalizar(
                " ".join(
                    [
                        plato.nombre,
                        plato.descripcion,
                        plato.categoria,
                        plato.departamento,
                        plato.historia,
                        *plato.ingredientes,
                    ]
                )
            )
        ]
    if dieta and dieta != "Todas":
        resultados = [plato for plato in resultados if plato.dieta.casefold() == dieta.casefold()]
    if departamento and departamento != "Todos":
        resultados = [
            plato for plato in resultados
            if plato.departamento.casefold() == departamento.casefold()
        ]
    if tipo and tipo != "Todos":
        resultados = [plato for plato in resultados if plato.tipo.casefold() == tipo.casefold()]
    return resultados


def crear_plato(
    nombre, dieta, precio=0, disponibilidad=0, descripcion="",
    categoria="Comida típica", ingredientes=None, departamento="",
    historia="", tipo="Platillo", combinaciones=None,
):
    error = validar_nombre(nombre)
    if error:
        raise ValueError(error)
    for valor, campo, minimo, maximo in (
        (descripcion, "La descripción", 10, 500),
        (categoria, "La categoría", 2, 60),
        (departamento, "El departamento", 0, 60),
        (historia, "El contexto cultural", 0, 800),
    ):
        error = validar_texto(valor, campo, minimo=minimo, maximo=maximo)
        if error:
            raise ValueError(error)
    if dieta not in {"Tradicional", "Vegetariana", "Vegana", "Sin gluten"}:
        raise ValueError("Selecciona un perfil alimentario válido.")
    if tipo not in {"Platillo", "Bebida", "Postre"}:
        raise ValueError("Selecciona un tipo de ficha válido.")
    def normalizar_opciones(valores, campo):
        if valores is None:
            return []
        if isinstance(valores, str):
            texto = valores
        elif all(isinstance(valor, str) for valor in valores):
            texto = ", ".join(valores)
        else:
            raise ValueError(f"Revisa las opciones indicadas en {campo}.")
        opciones, error_opciones = validar_lista_separada(texto, campo)
        if error_opciones:
            raise ValueError(error_opciones)
        return opciones

    ingredientes_validados = normalizar_opciones(ingredientes, "los ingredientes")
    combinaciones_validadas = normalizar_opciones(
        combinaciones, "las combinaciones"
    )
    if any(plato.nombre.casefold() == nombre.strip().casefold() for plato in lista_platos):
        raise ValueError("Ya existe un elemento con ese nombre.")
    codigo = _siguiente_codigo("P", lista_platos)
    plato = PlatoTradicional(
        codigo, nombre.strip(), dieta, float(precio), int(disponibilidad),
        descripcion.strip(), categoria.strip(),         ingredientes_validados,
        departamento.strip(),         historia.strip(), tipo.strip(), combinaciones_validadas,
    )
    lista_platos.append(plato)
    platos_por_codigo[codigo] = plato
    historial_movimientos.append(
        {"tipo": "REGISTRO CATÁLOGO", "codigo": codigo, "cantidad": 1}
    )
    return plato


def buscar_usuario_por_codigo(codigo):
    return usuarios_por_codigo.get(codigo)


def buscar_usuario(usuario, contraseña):
    if not usuario or not contraseña:
        return None
    identificador = usuario.strip().casefold()
    return next(
        (
            cuenta for cuenta in lista_usuarios
            if (
                cuenta.usuario.casefold() == identificador
                or cuenta.correo.casefold() == identificador
            )
            and cuenta.contraseña == contraseña
        ),
        None,
    )


def actualizar_puntos_usuario(codigo, cantidad):
    usuario = usuarios_por_codigo.get(codigo)
    if usuario is None or usuario.puntos_fidelidad + cantidad < 0:
        return False
    usuario.puntos_fidelidad += cantidad
    historial_movimientos.append(
        {
            "tipo": "ASIGNACION PUNTOS" if cantidad > 0 else "CANJE PUNTOS",
            "codigo": codigo,
            "cantidad": cantidad,
        }
    )
    return True


def actualizar_preferencias(usuario, intereses, evitar_ingredientes, dieta=None):
    if usuario.codigo not in usuarios_por_codigo:
        return False
    dietas_validas = {
        "Omnívora",
        "Tradicional",
        "Vegetariana",
        "Vegana",
        "Sin gluten",
    }
    if dieta is not None and dieta not in dietas_validas:
        return False
    if not isinstance(intereses, list) or not isinstance(evitar_ingredientes, list):
        return False
    if len(intereses) > 20 or len(evitar_ingredientes) > 20:
        return False
    if any(
        not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > 60
        for valor in intereses
    ):
        return False
    if any(
        not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > 60
        for valor in evitar_ingredientes
    ):
        return False
    usuario.intereses = list(dict.fromkeys(valor.strip() for valor in intereses))
    usuario.evitar_ingredientes = list(
        dict.fromkeys(valor.strip() for valor in evitar_ingredientes)
    )
    if dieta is not None:
        usuario.dieta_preferida = dieta
    historial_movimientos.append(
        {"tipo": "ACTUALIZAR PREFERENCIAS", "codigo": usuario.codigo}
    )
    return True


def obtener_recomendaciones(usuario=None, limite=6):
    rechazados = {
        item.plato_codigo for item in lista_interacciones
        if usuario and item.usuario_codigo == usuario.codigo and item.tipo == "no_me_interesa"
    }
    evitar = {
        _normalizar(ingrediente)
        for ingrediente in (usuario.evitar_ingredientes if usuario else [])
    }
    intereses = {
        _normalizar(interes) for interes in (usuario.intereses if usuario else [])
    }
    dietas = {
        _normalizar(dieta) for dieta in (usuario.dieta_preferida.split(",") if usuario else [])
    }
    favoritos = {
        item.plato_codigo for item in lista_interacciones
        if usuario and item.usuario_codigo == usuario.codigo and item.tipo == "favorito"
    }
    candidatos = []
    for plato in listar_platos():
        ingredientes = {_normalizar(ingrediente) for ingrediente in plato.ingredientes}
        if plato.codigo in rechazados or ingredientes.intersection(evitar):
            continue
        puntuacion = 0
        if _normalizar(plato.dieta) in dietas:
            puntuacion += 3
        if _normalizar(plato.departamento) in intereses:
            puntuacion += 2
        caracteristicas = _normalizar(" ".join([plato.categoria, *plato.ingredientes]))
        if any(interes in caracteristicas for interes in intereses):
            puntuacion += 2
        if plato.codigo in favoritos:
            puntuacion += 1
        candidatos.append((puntuacion, plato))
    candidatos.sort(key=lambda resultado: (-resultado[0], resultado[1].nombre))
    return [plato for _, plato in candidatos[:limite]]


def obtener_combinaciones(codigo_plato, usuario=None):
    base = platos_por_codigo.get(codigo_plato)
    if base is None or base.estado != "Publicado":
        return []
    nombres = {_normalizar(nombre) for nombre in base.combinaciones}
    resultados = [
        plato for plato in listar_platos()
        if plato.codigo != base.codigo and _normalizar(plato.nombre) in nombres
    ]
    if usuario:
        evitar = {_normalizar(ingrediente) for ingrediente in usuario.evitar_ingredientes}
        resultados = [
            plato for plato in resultados
            if not {_normalizar(ingrediente) for ingrediente in plato.ingredientes}.intersection(evitar)
        ]
    return resultados


def obtener_favoritos(usuario):
    codigos = {
        item.plato_codigo
        for item in lista_interacciones
        if item.usuario_codigo == usuario.codigo and item.tipo == "favorito"
    }
    return [
        plato
        for plato in listar_platos()
        if plato.codigo in codigos
    ]


def registrar_interaccion(usuario, codigo_plato, tipo, calificacion=0, comentario=""):
    if usuario is None or usuario.codigo not in usuarios_por_codigo:
        raise ValueError("Inicia sesión para guardar tu interacción.")
    plato = platos_por_codigo.get(codigo_plato)
    if plato is None or plato.estado != "Publicado":
        raise ValueError("El elemento ya no está disponible en el catálogo.")
    if tipo not in {"favorito", "no_me_interesa", "util", "reporte", "consulta"}:
        raise ValueError("El tipo de interacción no es válido.")
    if tipo == "util" and calificacion not in range(1, 6):
        raise ValueError("La valoración debe estar entre 1 y 5.")
    if tipo == "reporte" and not comentario.strip():
        raise ValueError("Describe qué dato debería revisar el equipo editorial.")
    if tipo in {"favorito", "no_me_interesa"}:
        lista_interacciones[:] = [
            item for item in lista_interacciones
            if not (
                item.usuario_codigo == usuario.codigo
                and item.plato_codigo == codigo_plato
                and item.tipo in {"favorito", "no_me_interesa"}
            )
        ]
    interaccion = Interaccion(
        _siguiente_codigo("I", lista_interacciones), usuario.codigo,
        codigo_plato, tipo, calificacion, comentario.strip(),
        "Pendiente de revisión" if tipo == "reporte" else "Registrada",
    )
    lista_interacciones.append(interaccion)
    historial_movimientos.append(
        {
            "tipo": "REPORTE EDITORIAL" if tipo == "reporte" else "INTERACCIÓN",
            "codigo": usuario.codigo,
            "elemento": codigo_plato,
        }
    )
    return interaccion


def obtener_reportes_pendientes():
    return [
        item for item in lista_interacciones
        if item.tipo == "reporte" and item.estado == "Pendiente de revisión"
    ]


def resolver_reporte(codigo, observaciones="Revisado"):
    interaccion = next(
        (
            item for item in lista_interacciones
            if item.codigo == codigo
            and item.tipo == "reporte"
            and item.estado == "Pendiente de revisión"
        ),
        None,
    )
    if interaccion is None:
        return False
    interaccion.estado = observaciones.strip() or "Revisado"
    return True


def listar_restaurantes_publicados(departamento="Todos", busqueda=""):
    resultados = [item for item in lista_restaurantes if item.estado == "Aprobado"]
    if departamento and departamento != "Todos":
        resultados = [
            item for item in resultados
            if item.departamento.casefold() == departamento.casefold()
        ]
    if busqueda.strip():
        termino = _normalizar(busqueda.strip())
        resultados = [
            item for item in resultados
            if termino in _normalizar(
                " ".join(
                    [
                        item.nombre, item.ubicacion, item.departamento,
                        item.municipio, item.especialidad, item.descripcion,
                    ]
                )
            )
        ]
    return resultados


def obtener_solicitudes_representante(usuario):
    return [
        item for item in lista_solicitudes
        if item.representante_codigo == usuario.codigo
    ]


def obtener_solicitudes_pendientes():
    return [item for item in lista_solicitudes if item.estado == "Pendiente de revisión"]


def crear_solicitud_establecimiento(
    nombre_representante, correo, telefono, usuario_login, contraseña,
    nombre, tipo, descripcion, departamento, municipio, direccion,
    horario, contacto, especialidad,
):
    entradas = (
        nombre_representante,
        correo,
        telefono,
        usuario_login,
        contraseña,
        nombre,
        tipo,
        descripcion,
        departamento,
        municipio,
        direccion,
        horario,
        contacto,
        especialidad,
    )
    if any(not isinstance(valor, str) for valor in entradas):
        raise ValueError("Todos los campos deben ser texto.")
    datos = {
        "nombre": nombre.strip(),
        "tipo": tipo.strip(),
        "descripcion": descripcion.strip(),
        "departamento": departamento.strip(),
        "municipio": municipio.strip(),
        "direccion": direccion.strip(),
        "horario": horario.strip(),
        "contacto": contacto.strip() or telefono.strip(),
        "especialidad": especialidad.strip(),
    }
    obligatorios = ("nombre", "tipo", "descripcion", "departamento", "municipio", "direccion")
    if not all(datos[campo] for campo in obligatorios):
        raise ValueError("Completa nombre, tipo, descripción y ubicación del establecimiento.")
    error_nombre = validar_nombre(nombre_representante)
    error_correo = validar_correo(correo)
    error_telefono = validar_telefono(telefono, obligatorio=True)
    error_usuario = validar_usuario(usuario_login)
    error_contrasena = validar_contrasena(contraseña)
    if error_nombre or error_correo or error_telefono or error_usuario or error_contrasena:
        raise ValueError(
            next(
                error
                for error in (
                    error_nombre,
                    error_correo,
                    error_telefono,
                    error_usuario,
                    error_contrasena,
                )
                if error
            )
        )
    for campo, nombre_visible, maximo in (
        ("nombre", "El establecimiento", 100),
        ("tipo", "El tipo de establecimiento", 50),
        ("descripcion", "La descripción", 500),
        ("departamento", "El departamento", 60),
        ("municipio", "El municipio", 60),
        ("direccion", "La dirección", 200),
        ("horario", "El horario", 120),
        ("contacto", "El contacto", 80),
        ("especialidad", "La especialidad", 160),
    ):
        error = validar_texto(
            datos[campo],
            nombre_visible,
            minimo=0 if campo in {"horario", "contacto", "especialidad"} else 2,
            maximo=maximo,
        )
        if error:
            raise ValueError(error)
    if any(item.nombre.casefold() == datos["nombre"].casefold() for item in lista_restaurantes):
        raise ValueError("Ya existe una solicitud o ficha con ese nombre.")

    representante = crear_usuario(
        nombre_representante, correo, "Omnívora", usuario_login,
        contraseña, "Representante",
    )
    if representante is None:
        raise ValueError("Revisa el correo; el usuario o correo podría estar registrado.")
    codigo_restaurante = _siguiente_codigo("R", lista_restaurantes)
    restaurante = Restaurante(
        codigo_restaurante, datos["nombre"],
        f'{datos["municipio"]}, {datos["departamento"]}',
        datos["especialidad"],
        departamento=datos["departamento"], municipio=datos["municipio"],
        direccion=datos["direccion"], horario=datos["horario"],
        contacto=datos["contacto"], descripcion=datos["descripcion"],
        representante_codigo=representante.codigo, estado="Pendiente",
        tipo=datos["tipo"],
    )
    lista_restaurantes.append(restaurante)
    restaurantes_por_codigo[codigo_restaurante] = restaurante
    representante.establecimiento_codigo = codigo_restaurante
    solicitud = SolicitudEstablecimiento(
        _siguiente_codigo("S", lista_solicitudes), codigo_restaurante,
        representante.codigo, "Inclusión", datos,
    )
    lista_solicitudes.append(solicitud)
    solicitudes_por_codigo[solicitud.codigo] = solicitud
    historial_movimientos.append(
        {"tipo": "SOLICITUD ESTABLECIMIENTO", "codigo": solicitud.codigo}
    )
    return representante, solicitud


def proponer_actualizacion_establecimiento(usuario, datos):
    restaurante = restaurantes_por_codigo.get(usuario.establecimiento_codigo)
    if (
        usuario.rol != "Representante"
        or restaurante is None
        or restaurante.representante_codigo != usuario.codigo
    ):
        raise ValueError("Solo puedes proponer cambios para tu propio establecimiento.")
    if any(
        item.restaurante_codigo == restaurante.codigo
        and item.estado == "Pendiente de revisión"
        for item in lista_solicitudes
    ):
        raise ValueError("Ya tienes una propuesta pendiente de revisión.")
    campos = {
        "nombre": datos.get("nombre", "").strip(),
        "tipo": datos.get("tipo", "").strip(),
        "descripcion": datos.get("descripcion", "").strip(),
        "departamento": datos.get("departamento", "").strip(),
        "municipio": datos.get("municipio", "").strip(),
        "direccion": datos.get("direccion", "").strip(),
        "horario": datos.get("horario", "").strip(),
        "contacto": datos.get("contacto", "").strip(),
        "especialidad": datos.get("especialidad", "").strip(),
    }
    obligatorios = ("nombre", "tipo", "descripcion", "departamento", "municipio", "direccion")
    if not all(campos[campo] for campo in obligatorios):
        raise ValueError("Completa nombre, tipo, descripción y ubicación del establecimiento.")
    solicitud = SolicitudEstablecimiento(
        _siguiente_codigo("S", lista_solicitudes), restaurante.codigo,
        usuario.codigo, "Actualización", campos,
    )
    lista_solicitudes.append(solicitud)
    solicitudes_por_codigo[solicitud.codigo] = solicitud
    historial_movimientos.append(
        {"tipo": "ACTUALIZACIÓN PROPUESTA", "codigo": solicitud.codigo}
    )
    return solicitud


def revisar_solicitud(codigo, decision, observaciones=""):
    solicitud = solicitudes_por_codigo.get(codigo)
    if solicitud is None or solicitud.estado != "Pendiente de revisión":
        return False
    if decision not in {"Aprobada", "Requiere correcciones", "Rechazada"}:
        raise ValueError("La decisión editorial no es válida.")
    solicitud.estado = decision
    solicitud.observaciones = observaciones.strip()
    restaurante = restaurantes_por_codigo[solicitud.restaurante_codigo]
    if decision == "Aprobada":
        for campo, valor in solicitud.datos_propuestos.items():
            if hasattr(restaurante, campo):
                setattr(restaurante, campo, valor)
        restaurante.ubicacion = f"{restaurante.municipio}, {restaurante.departamento}"
        restaurante.especialidad = solicitud.datos_propuestos["especialidad"]
        restaurante.estado = "Aprobado"
        restaurante.observaciones = ""
    elif solicitud.tipo == "Inclusión" and decision == "Rechazada":
        restaurante.estado = "Rechazado"
    else:
        restaurante.observaciones = observaciones.strip()
    historial_movimientos.append(
        {"tipo": "REVISIÓN EDITORIAL", "codigo": solicitud.codigo, "decision": decision}
    )
    return True
