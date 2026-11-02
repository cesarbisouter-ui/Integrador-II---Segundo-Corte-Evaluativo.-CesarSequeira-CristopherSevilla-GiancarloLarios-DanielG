import flet as ft

from funciones import obtener_directorio_usuarios
from gui.usuario_form import mostrar_formulario_usuario


def mostrar_usuarios(page: ft.Page):
    def crear_fila(usuario):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(usuario.nombre)),
                ft.DataCell(ft.Text(usuario.correo)),
                ft.DataCell(ft.Text(usuario.rol)),
            ]
        )

    usuarios = obtener_directorio_usuarios()
    filas = []
    for usuario in usuarios:
        filas.append(crear_fila(usuario))

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Rol")),
        ],
        rows=filas,
    )

    def actualizar_usuarios():
        tabla.rows.clear()
        for usuario in obtener_directorio_usuarios():
            tabla.rows.append(crear_fila(usuario))
        page.update()

    def abrir_formulario(evento):
        formulario = mostrar_formulario_usuario(page, actualizar_usuarios)
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Nuevo usuario"),
                content=formulario,
                scrollable=True,
            )
        )

    boton_nuevo = ft.Button(
        "Nuevo usuario",
        icon=ft.Icons.ADD,
        on_click=abrir_formulario,
    )

    return ft.Column(
        controls=[
            ft.Text(
                "Usuarios registrados",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),
            boton_nuevo,
            tabla,
        ]
    )