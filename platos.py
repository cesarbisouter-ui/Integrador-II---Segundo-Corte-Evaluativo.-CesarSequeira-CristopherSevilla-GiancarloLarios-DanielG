import flet as ft

from funciones import listar_platos
from gui.plato_form import mostrar_formulario_plato


def mostrar_platos(page: ft.Page, permitir_edicion: bool = True):
    lista = ft.Column(spacing=10)

    def actualizar_platos():
        lista.controls = []
        platos = listar_platos()
        for plato in platos:
            tarjeta = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"{plato.nombre} · {plato.tipo}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#174D3C",
                            ),
                            ft.Text(f"{plato.categoria} · {plato.departamento or 'Sin región'}"),
                            ft.Text(plato.descripcion),
                            ft.Text(
                                "Ingredientes: " + (", ".join(plato.ingredientes) or "Pendientes de documentar")
                            ),
                        ],
                        spacing=6,
                    ),
                    padding=16,
                    bgcolor="#F7F4EB",
                )
            )
            lista.controls.append(tarjeta)
        if not platos:
            lista.controls.append(ft.Text("El catálogo todavía no tiene fichas."))
        page.update()

    def abrir_formulario(e):
        formulario = mostrar_formulario_plato(page, actualizar_platos)
        guardar = formulario.controls.pop().controls[0]
        guardar.text = "Guardar"
        guardar.icon = ft.Icons.SAVE
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Añadir al catálogo cultural"),
                content=ft.Container(content=formulario, width=520, height=560),
                actions=[
                    guardar,
                    ft.TextButton(
                        "Cancelar",
                        icon=ft.Icons.CLOSE,
                        on_click=lambda evento: page.pop_dialog(),
                    )
                ],
                scrollable=True,
            )
        )

    controles = [
        ft.Text("Administrar el catálogo cultural", size=28, weight=ft.FontWeight.BOLD, color="#174D3C"),
        ft.Text(
            "Completa datos descriptivos, ingredientes, contexto cultural y relaciones. "
            "No se gestionan precios, inventario ni ventas."
        ),
    ]
    if permitir_edicion:
        controles.append(
            ft.FilledButton(
                "Nueva ficha",
                icon=ft.Icons.ADD,
                on_click=abrir_formulario,
            )
        )
    controles.append(lista)
    actualizar_platos()
    return ft.Column(controls=controles, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)
