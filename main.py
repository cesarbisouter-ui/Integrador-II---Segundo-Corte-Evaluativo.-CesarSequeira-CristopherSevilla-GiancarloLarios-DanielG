from pathlib import Path

import flet as ft

from gui.catalogo import (
    mostrar_catalogo,
    mostrar_inicio,
    mostrar_recomendaciones,
    mostrar_regiones,
)
from gui.establecimientos import (
    mostrar_panel_representante,
    mostrar_revision_editorial,
)
from gui.login import mostrar_login
from gui.perfil import mostrar_perfil
from gui.platos import mostrar_platos
from gui.usuarios import mostrar_usuarios


VERDE = "#174D3C"
CREMA = "#F7F4EB"


def main(page: ft.Page):
    page.title = "NicaCrave | Raíces en cada bocado"
    page.padding = 0
    page.bgcolor = "#FCFBF7"
    page.theme = ft.Theme(color_scheme_seed=VERDE)
    page.theme_mode = ft.ThemeMode.LIGHT

    usuario_actual = None
    seccion_actual = "inicio"
    contenido = ft.Container(expand=True, padding=20)

    def es_editor():
        return usuario_actual is not None and usuario_actual.rol in {
            "Administrador",
            "Editor",
        }

    def es_representante():
        return usuario_actual is not None and usuario_actual.rol == "Representante"

    def es_recepcionista():
        return usuario_actual is not None and usuario_actual.rol == "Recepción"

    def iniciar_sesion(usuario):
        nonlocal usuario_actual, seccion_actual
        usuario_actual = usuario
        seccion_actual = "establecimiento" if es_representante() else "inicio"
        renderizar()

    def abrir_acceso(e=None):
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Row(
                    [
                        ft.Text(
                            "Bienvenido a NicaCrave",
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            tooltip="Cerrar ventana",
                            on_click=lambda event: page.pop_dialog(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                content=ft.Container(
                    content=mostrar_login(page, iniciar_sesion),
                    width=440,
                ),
                actions=[
                    ft.TextButton(
                        "Cerrar",
                        icon=ft.Icons.CLOSE,
                        on_click=lambda event: page.pop_dialog(),
                    )
                ],
                scrollable=True,
            )
        )

    def cerrar_sesion(e=None):
        nonlocal usuario_actual, seccion_actual
        usuario_actual = None
        seccion_actual = "inicio"
        renderizar()

    def navegar(seccion):
        nonlocal seccion_actual
        if usuario_actual is None:
            renderizar()
            return
        if seccion == "perfil" and es_recepcionista():
            seccion = "inicio"
        if seccion in {"editorial", "contenido", "usuarios"} and not es_editor():
            seccion = "inicio"
        if seccion == "establecimiento" and not es_representante():
            seccion = "inicio"
        seccion_actual = seccion
        renderizar()

    def boton_nav(etiqueta, destino, icono):
        clase = ft.FilledTonalButton if seccion_actual == destino else ft.OutlinedButton
        return clase(etiqueta, icon=icono, on_click=lambda e: navegar(destino))

    def construir_contenido():
        if seccion_actual == "catalogo":
            return mostrar_catalogo(page, usuario_actual, abrir_acceso, renderizar)
        if seccion_actual == "regiones":
            return mostrar_regiones(page, navegar)
        if seccion_actual == "recomendaciones":
            return mostrar_recomendaciones(page, usuario_actual, abrir_acceso, renderizar)
        if seccion_actual == "perfil" and usuario_actual:
            return mostrar_perfil(page, usuario_actual)
        if seccion_actual == "establecimiento" and es_representante():
            return mostrar_panel_representante(page, usuario_actual, renderizar)
        if seccion_actual == "editorial" and es_editor():
            return mostrar_revision_editorial(page, renderizar)
        if seccion_actual == "contenido" and es_editor():
            return mostrar_platos(page, permitir_edicion=True)
        if seccion_actual == "usuarios" and es_editor():
            return mostrar_usuarios(page)
        return mostrar_inicio(page, usuario_actual, navegar, abrir_acceso)

    def renderizar():
        page.controls.clear()
        if usuario_actual is None:
            page.add(
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=mostrar_login(
                                page,
                                iniciar_sesion,
                                dentro_dialogo_acceso=False,
                            ),
                            width=480,
                            padding=24,
                        ),
                        elevation=8,
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                    padding=24,
                )
            )
            page.update()
            return

        logo = ft.Row(
            [
                ft.Icon(ft.Icons.RICE_BOWL, size=28, color="#E0A439"),
                ft.Column(
                    [
                        ft.Text("NICACRAVE", size=17, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text("RAÍCES EN CADA BOCADO", size=10, color="#D8E6D8"),
                    ],
                    spacing=0,
                ),
            ],
            spacing=8,
        )
        perfil = (
            ft.Row(
                [
                    ft.Text(
                        f"{usuario_actual.nombre} · {usuario_actual.rol}",
                        color="#FFFFFF",
                        size=13,
                    ),
                    ft.OutlinedButton(
                        "Salir",
                        icon=ft.Icons.LOGOUT,
                        style=ft.ButtonStyle(color="#FFFFFF"),
                        on_click=cerrar_sesion,
                    ),
                ],
                spacing=8,
            )
            if usuario_actual
            else ft.OutlinedButton(
                "Acceder",
                icon=ft.Icons.LOGIN,
                style=ft.ButtonStyle(color="#FFFFFF"),
                on_click=abrir_acceso,
            )
        )
        page.add(
            ft.Container(
                content=ft.Row(
                    [logo, perfil],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=VERDE,
                padding=ft.Padding.symmetric(horizontal=20, vertical=12),
            )
        )
        enlaces = [
            ("Inicio", "inicio", ft.Icons.HOME_OUTLINED),
            ("Explorar", "catalogo", ft.Icons.SEARCH),
            ("Regiones", "regiones", ft.Icons.MAP_OUTLINED),
            ("Para ti", "recomendaciones", ft.Icons.AUTO_AWESOME),
        ]
        if usuario_actual and not es_recepcionista():
            enlaces.append(("Mi perfil", "perfil", ft.Icons.PERSON_OUTLINE))
        if es_representante():
            enlaces.append(("Mi establecimiento", "establecimiento", ft.Icons.STORE_MALL_DIRECTORY))
        if es_editor():
            enlaces.extend(
                [
                    ("Revisión", "editorial", ft.Icons.RULE),
                    ("Catálogo", "contenido", ft.Icons.MENU_BOOK),
                    ("Usuarios", "usuarios", ft.Icons.GROUP_OUTLINED),
                ]
            )
        page.add(
            ft.Container(
                content=ft.Row(
                    [boton_nav(etiqueta, destino, icono) for etiqueta, destino, icono in enlaces],
                    spacing=6,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                bgcolor=CREMA,
            )
        )
        contenido.content = construir_contenido()
        page.add(contenido)
        page.update()

    renderizar()


ft.run(main)