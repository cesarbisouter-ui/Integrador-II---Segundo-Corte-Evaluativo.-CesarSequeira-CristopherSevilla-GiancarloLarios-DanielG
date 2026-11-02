import flet as ft

from funciones import crear_plato
from validaciones import validar_lista_separada, validar_nombre, validar_texto


def mostrar_formulario_plato(page: ft.Page, on_guardado):
    nombre = ft.TextField(label="Nombre del platillo o bebida")
    tipo = ft.Dropdown(
        label="Tipo",
        value="Platillo",
        options=[
            ft.DropdownOption(key="Platillo", text="Platillo"),
            ft.DropdownOption(key="Bebida", text="Bebida"),
            ft.DropdownOption(key="Postre", text="Postre"),
        ],
    )
    categoria = ft.TextField(label="Categoría", value="Comida típica", max_length=60)
    dieta = ft.Dropdown(
        label="Perfil alimentario",
        value="Tradicional",
        options=[
            ft.DropdownOption(key="Tradicional", text="Tradicional"),
            ft.DropdownOption(key="Vegetariana", text="Vegetariana"),
            ft.DropdownOption(key="Vegana", text="Vegana"),
            ft.DropdownOption(key="Sin gluten", text="Sin gluten"),
        ],
    )
    descripcion = ft.TextField(
        label="Descripción breve",
        multiline=True,
        min_lines=2,
        max_lines=4,
        max_length=500,
    )
    ingredientes = ft.TextField(
        label="Ingredientes habituales (separados por coma)",
        hint_text="maíz, cacao, canela",
        max_length=1300,
    )
    departamento = ft.TextField(label="Departamento o región relacionada", max_length=60)
    historia = ft.TextField(
        label="Contexto o dato cultural",
        multiline=True,
        min_lines=2,
        max_lines=4,
        max_length=800,
    )
    combinaciones = ft.TextField(
        label="Combinaciones documentadas (separadas por coma)",
        hint_text="Pinolillo, cacao",
        max_length=1300,
    )
    mensaje = ft.Text()

    def guardar(evento):
        nombre.error = validar_nombre(nombre.value or "")
        categoria.error = validar_texto(
            categoria.value or "", "La categoría", minimo=2, maximo=60
        )
        descripcion.error = validar_texto(
            descripcion.value or "", "La descripción", minimo=10, maximo=500
        )
        lista_ingredientes, error_ingredientes = validar_lista_separada(
            ingredientes.value or "", "los ingredientes"
        )
        lista_combinaciones, error_combinaciones = validar_lista_separada(
            combinaciones.value or "", "las combinaciones"
        )
        ingredientes.error = error_ingredientes
        combinaciones.error = error_combinaciones
        if (
            nombre.error
            or categoria.error
            or descripcion.error
            or ingredientes.error
            or combinaciones.error
        ):
            page.update()
            return
        try:
            crear_plato(
                nombre.value,
                dieta.value,
                descripcion=descripcion.value,
                categoria=categoria.value,
                ingredientes=lista_ingredientes,
                departamento=departamento.value or "",
                historia=historia.value or "",
                tipo=tipo.value or "Platillo",
                combinaciones=lista_combinaciones,
            )
        except ValueError as error:
            mensaje.value = str(error)
            mensaje.color = ft.Colors.RED_700
            page.update()
            return
        on_guardado()
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Ficha cultural publicada en el catálogo."),
                bgcolor=ft.Colors.GREEN_800,
            )
        )

    return ft.Column(
        controls=[
            ft.Text("Nueva ficha gastronómica", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Publica información cultural; no se registran ventas ni pedidos."),
            nombre,
            tipo,
            categoria,
            dieta,
            descripcion,
            ingredientes,
            departamento,
            historia,
            combinaciones,
            mensaje,
            ft.Row(
                [ft.FilledButton("Publicar ficha", icon=ft.Icons.PUBLISH, on_click=guardar)],
                wrap=True,
            ),
        ],
        spacing=10,
        tight=True,
        scroll=ft.ScrollMode.AUTO,
    )
