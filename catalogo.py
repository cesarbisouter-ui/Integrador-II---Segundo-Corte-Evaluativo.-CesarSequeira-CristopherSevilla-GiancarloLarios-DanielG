import flet as ft

from datos import lista_platos
from funciones import (
    listar_platos,
    listar_restaurantes_publicados,
    obtener_combinaciones,
    obtener_recomendaciones,
    registrar_interaccion,
)


VERDE = "#174D3C"
CREMA = "#F7F4EB"
ORO = "#D99A32"


def _ancho_imagen(page, proporcion=0.43):
    ancho_pantalla = getattr(page, "width", None)
    if not isinstance(ancho_pantalla, (int, float)) or ancho_pantalla <= 0:
        ancho_pantalla = 900
    return max(240, min(620, ancho_pantalla * proporcion - 32))


def _imagen_plato(plato, alto=190, ancho=320):
    if plato.imagen:
        return ft.Image(
            src=plato.imagen,
            width=ancho,
            height=alto,
            fit=ft.BoxFit.COVER,
            border_radius=12,
            semantics_label=f"Fotografía de {plato.nombre}",
        )
    icono = ft.Icons.RESTAURANT
    if plato.tipo == "Bebida":
        icono = ft.Icons.LOCAL_DRINK
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    icono,
                    size=40,
                    color=ORO,
                ),
                ft.Column(
                    [
                        ft.Text(
                            plato.nombre,
                            color="#FFFFFF",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(plato.categoria, color="#E3D9C4", size=13),
                    ],
                    spacing=2,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        height=alto,
        bgcolor="#174D3C",
        border_radius=12,
    )


def _titulo(texto, detalle=""):
    controles = [ft.Text(texto, size=28, weight=ft.FontWeight.BOLD, color=VERDE)]
    if detalle:
        controles.append(ft.Text(detalle, size=14, color=ft.Colors.BLUE_GREY_700))
    return ft.Column(controls=controles, spacing=4)


def _notificar(page, mensaje, color=VERDE):
    page.show_dialog(
        ft.SnackBar(content=ft.Text(mensaje), bgcolor=color)
    )


def _tarjeta_plato(page, plato, usuario, pedir_login, al_actualizar):
    icono = ft.Icons.RESTAURANT
    if plato.tipo == "Bebida":
        icono = ft.Icons.LOCAL_DRINK
    ancho_imagen = _ancho_imagen(page)
    detalle = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(icono, color=ORO, size=28),
                    ft.Column(
                        controls=[
                            ft.Text(plato.nombre, size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"{plato.categoria} · {plato.departamento or 'Nicaragua'}",
                                color=ft.Colors.BLUE_GREY_700,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Text(plato.descripcion or "Una preparación de la cocina nicaragüense."),
            ft.Text(
                "Ingredientes: " + (", ".join(plato.ingredientes) or "Por documentar"),
                size=13,
                color=ft.Colors.BLUE_GREY_700,
            ),
            ft.Text("Dieta: " + plato.dieta, size=13),
        ],
        spacing=8,
    )

    def abrir_ficha(e):
        if usuario is not None:
            registrar_interaccion(usuario, plato.codigo, "consulta")
        contenido = ft.Column(
            controls=[
                _imagen_plato(plato, alto=220, ancho=min(ancho_imagen, 420)),
                ft.Text(plato.descripcion, size=16),
                ft.Text("Contexto cultural", weight=ft.FontWeight.BOLD, color=VERDE),
                ft.Text(plato.historia or "No hay contexto documentado todavía."),
                ft.Text("Ingredientes habituales", weight=ft.FontWeight.BOLD, color=VERDE),
                ft.Text(", ".join(plato.ingredientes) or "Por documentar."),
                ft.Text("Departamento: " + (plato.departamento or "No especificado")),
                ft.Text("Combinaciones relacionadas", weight=ft.FontWeight.BOLD, color=VERDE),
            ],
            tight=True,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )
        parejas = obtener_combinaciones(plato.codigo, usuario)
        contenido.controls.append(
            ft.Text(
                ", ".join(item.nombre for item in parejas)
                if parejas
                else "Aún no hay combinaciones documentadas."
            )
        )
        mensaje = ft.Text()
        observacion = ft.TextField(
            label="¿Qué dato deberíamos revisar?",
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        def registrar(tipo):
            if usuario is None:
                page.pop_dialog()
                pedir_login()
                return
            calificacion = 0
            if tipo == "util":
                calificacion = 5
            try:
                registrar_interaccion(
                    usuario,
                    plato.codigo,
                    tipo,
                    calificacion=calificacion,
                    comentario=observacion.value or "",
                )
            except ValueError as error:
                mensaje.value = str(error)
                mensaje.color = ft.Colors.RED_700
                page.update()
                return
            page.pop_dialog()
            mensaje_exito = "Gracias; guardamos tu valoración."
            if tipo == "reporte":
                mensaje_exito = (
                    "Gracias por tu aporte; el equipo editorial revisará el reporte."
                )
            _notificar(page, mensaje_exito)
            al_actualizar()

        def marcar_util(evento):
            registrar("util")

        def enviar_reporte(evento):
            registrar("reporte")

        def cerrar_ficha(evento):
            page.pop_dialog()

        contenido.controls.extend(
            [
                observacion,
                mensaje,
                ft.Row(
                    [
                        ft.TextButton(
                            "Me resultó útil",
                            icon=ft.Icons.THUMB_UP_ALT,
                            on_click=marcar_util,
                        ),
                        ft.TextButton(
                            "Enviar reporte",
                            icon=ft.Icons.FLAG_OUTLINED,
                            on_click=enviar_reporte,
                        ),
                    ],
                    wrap=True,
                ),
            ]
        )
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text(plato.nombre),
                content=ft.Container(content=contenido, width=460),
                actions=[ft.TextButton("Cerrar", on_click=cerrar_ficha)],
                scrollable=True,
            )
        )

    def interactuar(tipo):
        if usuario is None:
            pedir_login()
            return
        try:
            registrar_interaccion(usuario, plato.codigo, tipo)
        except ValueError as error:
            _notificar(page, str(error), ft.Colors.RED_700)
            return
        mensaje_exito = "Gracias; tendremos en cuenta tu opinión."
        if tipo == "favorito":
            mensaje_exito = "Guardado en tus favoritos."
        _notificar(page, mensaje_exito)
        al_actualizar()

    def guardar_favorito(evento):
        interactuar("favorito")

    def no_me_interesa(evento):
        interactuar("no_me_interesa")

    acciones = ft.Row(
        controls=[
            ft.TextButton("Ver historia", icon=ft.Icons.AUTO_STORIES, on_click=abrir_ficha),
            ft.TextButton(
                "Guardar",
                icon=ft.Icons.BOOKMARK_BORDER,
                on_click=guardar_favorito,
            ),
            ft.TextButton(
                "No me interesa",
                icon=ft.Icons.THUMB_DOWN_ALT,
                on_click=no_me_interesa,
            ),
        ],
        wrap=True,
        spacing=4,
    )

    return ft.Card(
        bgcolor=CREMA,
        content=ft.Container(
            content=ft.Column(
                [_imagen_plato(plato, ancho=ancho_imagen), detalle, acciones],
                spacing=10,
            ),
            padding=18,
            bgcolor=CREMA,
            border_radius=14,
        )
    )


def _tarjetas_platos(page, platos, usuario, pedir_login, al_actualizar):
    return [
        ft.Container(
            content=_tarjeta_plato(
                page,
                plato,
                usuario,
                pedir_login,
                al_actualizar,
            ),
            col={"xs": 12, "md": 6},
        )
        for plato in platos
    ]


def mostrar_inicio(page, usuario, navegar, pedir_login):
    usuario_texto = "La cocina nicaragüense tiene una historia que contar."
    if usuario is not None:
        primer_nombre = usuario.nombre.split()[0]
        usuario_texto = f"¡Qué gusto verte, {primer_nombre}!"

    platos = listar_platos()
    lugares = listar_restaurantes_publicados()
    ancho_portada = _ancho_imagen(page, proporcion=0.36)

    def actualizar_inicio():
        navegar("inicio")

    tarjetas_platos = []
    for plato in platos:
        tarjeta = _tarjeta_plato(
            page,
            plato,
            usuario,
            pedir_login,
            actualizar_inicio,
        )
        tarjetas_platos.append(tarjeta)

    departamentos = set()
    for plato in platos:
        if plato.departamento:
            departamentos.add(plato.departamento)

    def abrir_catalogo(evento):
        navegar("catalogo")

    def abrir_regiones(evento):
        navegar("regiones")

    def abrir_recomendaciones(evento):
        navegar("recomendaciones")

    return ft.Column(
        controls=[
            _titulo(
                "Sabores nicaragüenses",
                f"Explora las {len(platos)} fichas de platos, bebidas y postres del catálogo.",
            ),
            ft.Column(
                controls=tarjetas_platos,
                spacing=12,
            ),
            ft.Container(
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.RICE_BOWL, size=38, color=ORO),
                                            ft.Text("NICACRAVE", size=19, weight=ft.FontWeight.BOLD, color="#F7F4EB"),
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Text(
                                        "Raíces en cada bocado.",
                                        size=34,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF",
                                    ),
                                    ft.Text(
                                        usuario_texto,
                                        size=17,
                                        color="#F2EADB",
                                    ),
                                    ft.Text(
                                        "Descubre sabores, historias y lugares de Nicaragua. "
                                        "Una guía cultural, sin pedidos ni pagos.",
                                        size=15,
                                        color="#F2EADB",
                                    ),
                                    ft.Row(
                                        [
                                            ft.FilledButton(
                                                "Explorar el catálogo",
                                                icon=ft.Icons.EXPLORE,
                                                style=ft.ButtonStyle(bgcolor=ORO, color=VERDE),
                                                on_click=abrir_catalogo,
                                            ),
                                            ft.OutlinedButton(
                                                "Descubrir por región",
                                                icon=ft.Icons.MAP,
                                                style=ft.ButtonStyle(
                                                    color="#FFFFFF",
                                                    side=ft.BorderSide(color="#FFFFFF"),
                                                ),
                                                on_click=abrir_regiones,
                                            ),
                                        ],
                                        wrap=True,
                                    ),
                                ],
                                spacing=12,
                            ),
                            col={"xs": 12, "md": 7},
                        ),
                        ft.Container(
                            content=ft.Image(
                                src="platos/vigoron.png",
                                width=ancho_portada,
                                height=250,
                                fit=ft.BoxFit.COVER,
                                border_radius=16,
                                semantics_label="Vigorón nicaragüense",
                            ),
                            col={"xs": 12, "md": 5},
                        ),
                    ],
                    spacing=16,
                ),
                bgcolor=VERDE,
                padding=ft.Padding.symmetric(horizontal=28, vertical=24),
                border_radius=18,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [ft.Text("Sabores documentados", size=13), ft.Text(str(len(platos)), size=24, weight=ft.FontWeight.BOLD, color=VERDE)],
                            spacing=2,
                        ),
                        padding=16,
                        bgcolor="#E8F0E8",
                        border_radius=14,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Departamentos", size=13),
                                ft.Text(
                                    str(len(departamentos)),
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=VERDE,
                                ),
                            ],
                            spacing=2,
                        ),
                        padding=16,
                        bgcolor="#F5EBD8",
                        border_radius=14,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [ft.Text("Lugares verificados", size=13), ft.Text(str(len(lugares)), size=24, weight=ft.FontWeight.BOLD, color=VERDE)],
                            spacing=2,
                        ),
                        padding=16,
                        bgcolor="#E8EDF0",
                        border_radius=14,
                        expand=True,
                    ),
                ],
                spacing=12,
                wrap=True,
            ),
            ft.Row(
                [
                    ft.OutlinedButton(
                        "Ver recomendaciones",
                        icon=ft.Icons.AUTO_AWESOME,
                        on_click=abrir_recomendaciones,
                    ),
                    ft.TextButton(
                        "Conoce el proyecto",
                        icon=ft.Icons.INFO_OUTLINE,
                        on_click=abrir_catalogo,
                    ),
                ],
                wrap=True,
            ),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def mostrar_catalogo(page, usuario, pedir_login, al_actualizar):
    busqueda = ft.TextField(
        label="Platillo, ingrediente, bebida o historia",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        max_length=100,
    )
    opciones_dieta = [
        ft.DropdownOption(key="Todas", text="Todas"),
        ft.DropdownOption(key="Tradicional", text="Tradicional"),
        ft.DropdownOption(key="Vegetariana", text="Vegetariana"),
        ft.DropdownOption(key="Vegana", text="Vegana"),
        ft.DropdownOption(key="Sin gluten", text="Sin gluten"),
    ]
    filtro_dieta = ft.Dropdown(label="Dieta", value="Todas", options=opciones_dieta, width=170)
    departamentos_unicos = set()
    for plato in lista_platos:
        if plato.departamento:
            departamentos_unicos.add(plato.departamento)
    departamentos = ["Todos"]
    departamentos.extend(sorted(departamentos_unicos))
    opciones_region = []
    for departamento in departamentos:
        opciones_region.append(
            ft.DropdownOption(key=departamento, text=departamento)
        )
    filtro_region = ft.Dropdown(
        label="Departamento",
        value="Todos",
        options=opciones_region,
        width=190,
    )
    filtro_tipo = ft.Dropdown(
        label="Tipo",
        value="Todos",
        options=[
            ft.DropdownOption(key="Todos", text="Todos"),
            ft.DropdownOption(key="Platillo", text="Platillo"),
            ft.DropdownOption(key="Bebida", text="Bebida"),
            ft.DropdownOption(key="Postre", text="Postre"),
        ],
        width=150,
    )
    tarjetas_iniciales = _tarjetas_platos(
        page,
        listar_platos(),
        usuario,
        pedir_login,
        al_actualizar,
    )
    resultados = ft.ResponsiveRow(
        controls=tarjetas_iniciales,
        spacing=12,
        run_spacing=12,
    )
    platos_recomendados = obtener_recomendaciones(usuario)
    tarjetas_recomendadas = _tarjetas_platos(
        page,
        platos_recomendados,
        usuario,
        pedir_login,
        al_actualizar,
    )
    seccion_recomendados = ft.Column(
        controls=[
            _titulo(
                "Para ti",
                "Sugerencias personalizadas como las de tu sección de recomendaciones.",
            ),
            ft.ResponsiveRow(
                controls=tarjetas_recomendadas,
                spacing=12,
                run_spacing=12,
            )
            if tarjetas_recomendadas
            else ft.Text("No hay sugerencias con las exclusiones actuales."),
        ],
        spacing=10,
    )

    def actualizar_resultados(evento=None):
        platos = listar_platos(
            busqueda.value or "",
            filtro_dieta.value or "Todas",
            filtro_region.value or "Todos",
            filtro_tipo.value or "Todos",
        )
        tarjetas = _tarjetas_platos(
            page,
            platos,
            usuario,
            pedir_login,
            al_actualizar,
        )
        if tarjetas:
            resultados.controls = tarjetas
        else:
            resultados.controls = [
                ft.Container(
                    content=ft.Text(
                        "No encontramos coincidencias. Prueba con otro término o filtro."
                    ),
                    padding=20,
                    bgcolor=CREMA,
                    border_radius=12,
                    col={"xs": 12},
                ),
            ]
        page.update()

    filtro_dieta.on_select = actualizar_resultados
    filtro_region.on_select = actualizar_resultados
    filtro_tipo.on_select = actualizar_resultados
    busqueda.on_submit = actualizar_resultados
    buscar = ft.OutlinedButton(
        "Buscar",
        icon=ft.Icons.SEARCH,
        on_click=actualizar_resultados,
    )
    return ft.Column(
        controls=[
            _titulo(
                "Explora el catálogo",
                "Fichas culturales de comida, bebidas y sabores regionales.",
            ),
            seccion_recomendados,
            ft.Row([busqueda, buscar], wrap=True),
            ft.Row([filtro_dieta, filtro_region, filtro_tipo], wrap=True),
            resultados,
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def mostrar_regiones(page, navegar):
    departamentos_unicos = set()
    for plato in lista_platos:
        if plato.departamento:
            departamentos_unicos.add(plato.departamento)
    departamentos = sorted(departamentos_unicos)
    opciones_region = [ft.DropdownOption(key="Todos", text="Todos")]
    for departamento in departamentos:
        opciones_region.append(
            ft.DropdownOption(key=departamento, text=departamento)
        )
    filtro = ft.Dropdown(
        label="Selecciona un departamento",
        value="Todos",
        options=opciones_region,
    )
    buscar = ft.TextField(label="Buscar platillo o localidad", prefix_icon=ft.Icons.SEARCH)
    lista = ft.Column(spacing=12)

    def actualizar(evento=None):
        platos = listar_platos(
            busqueda=buscar.value or "",
            departamento=filtro.value or "Todos",
        )
        lugares = listar_restaurantes_publicados(
            departamento=filtro.value or "Todos",
            busqueda=buscar.value or "",
        )
        tarjetas = []
        for plato in platos:
            tarjetas.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(plato.nombre, size=19, weight=ft.FontWeight.BOLD, color=VERDE),
                                ft.Text(f"{plato.departamento} · {plato.categoria}"),
                                ft.Text(plato.descripcion),
                            ],
                            spacing=6,
                        ),
                        padding=16,
                        bgcolor=CREMA,
                    )
                )
            )
        for lugar in lugares:
            tipo_lugar = lugar.especialidad
            if hasattr(lugar, "tipo"):
                tipo_lugar = lugar.tipo
            tarjetas.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(lugar.nombre, size=19, weight=ft.FontWeight.BOLD, color=VERDE),
                                ft.Text(
                                    f"{lugar.municipio}, {lugar.departamento} · {tipo_lugar}"
                                ),
                                ft.Text(lugar.descripcion),
                                ft.Text("Dirección: " + (lugar.direccion or "No disponible")),
                                ft.Text("Horario: " + (lugar.horario or "No verificado")),
                                ft.Text(
                                    "La información puede cambiar; confirma los datos antes de tu visita.",
                                    size=12,
                                ),
                            ],
                            spacing=6,
                        ),
                        padding=16,
                        bgcolor="#E8F0E8",
                    )
                )
            )
        if tarjetas:
            lista.controls = tarjetas
        else:
            lista.controls = [
                ft.Text(
                    "No hay resultados para esta región. Los establecimientos solo aparecen tras aprobación editorial."
                )
            ]
        page.update()

    filtro.on_select = actualizar
    buscar.on_submit = actualizar
    actualizar()

    def abrir_catalogo(evento):
        navegar("catalogo")

    return ft.Column(
        [
            _titulo("Sabores por región", "Descubre sus orígenes y consulta únicamente lugares aprobados."),
            ft.Row([filtro, buscar, ft.OutlinedButton("Buscar", icon=ft.Icons.SEARCH, on_click=actualizar)], wrap=True),
            lista,
            ft.TextButton(
                "Abrir catálogo completo",
                icon=ft.Icons.RESTAURANT_MENU,
                on_click=abrir_catalogo,
            ),
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def mostrar_recomendaciones(page, usuario, pedir_login, al_actualizar):
    platos = obtener_recomendaciones(usuario)
    texto_usuario = "Puedes cambiar tus intereses y exclusiones desde Mi perfil."
    if usuario is None:
        texto_usuario = (
            "Inicia sesión y configura tus preferencias para personalizar estas sugerencias."
        )

    tarjetas = _tarjetas_platos(
        page,
        platos,
        usuario,
        pedir_login,
        al_actualizar,
    )
    if tarjetas:
        resultados = ft.ResponsiveRow(controls=tarjetas, spacing=12)
    else:
        resultados = ft.Text(
            "No hay sugerencias con las exclusiones actuales. Ajusta tus preferencias."
        )

    return ft.Column(
        [
            _titulo(
                "Recomendaciones con sabor",
                "Sugerencias basadas en tus intereses, ingredientes a evitar y relaciones documentadas.",
            ),
            ft.Text(texto_usuario),
            resultados,
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
