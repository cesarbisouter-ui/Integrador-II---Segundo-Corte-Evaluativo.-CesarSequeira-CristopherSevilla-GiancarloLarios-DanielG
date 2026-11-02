import flet as ft

from funciones import actualizar_perfil, actualizar_preferencias, obtener_favoritos
from validaciones import validar_correo, validar_lista_separada, validar_nombre


def mostrar_perfil(page, usuario):
    nombre = ft.TextField(label="Nombre visible", value=usuario.nombre, max_length=80)
    correo = ft.TextField(
        label="Correo electrónico",
        value=usuario.correo,
        keyboard_type=ft.KeyboardType.EMAIL,
        max_length=254,
    )
    preferencias = ft.Dropdown(
        label="Preferencia alimentaria",
        value=usuario.dieta_preferida or "Omnívora",
        options=[
            ft.DropdownOption(key="Omnívora", text="Omnívora"),
            ft.DropdownOption(key="Tradicional", text="Tradicional"),
            ft.DropdownOption(key="Vegetariana", text="Vegetariana"),
            ft.DropdownOption(key="Vegana", text="Vegana"),
            ft.DropdownOption(key="Sin gluten", text="Sin gluten"),
        ],
    )
    intereses = ft.TextField(
        label="Intereses (separados por coma)",
        value=", ".join(usuario.intereses),
        hint_text="Granada, bebidas, maíz",
        max_length=1300,
    )
    evitar = ft.TextField(
        label="Ingredientes que prefieres evitar",
        value=", ".join(usuario.evitar_ingredientes),
        hint_text="maní, lácteos",
        max_length=1300,
    )
    mensaje = ft.Text()
    favoritos = obtener_favoritos(usuario)

    def guardar(evento):
        nombre.error = validar_nombre(nombre.value or "")
        correo.error = validar_correo(correo.value or "")
        lista_intereses, error_intereses = validar_lista_separada(
            intereses.value or "", "los intereses"
        )
        lista_evitar, error_evitar = validar_lista_separada(
            evitar.value or "", "los ingredientes que deseas evitar"
        )
        intereses.error = error_intereses
        evitar.error = error_evitar
        if nombre.error or correo.error or intereses.error or evitar.error:
            page.update()
            return
        if not actualizar_perfil(usuario, nombre.value or "", correo.value or ""):
            correo.error = (
                "Este correo ya está vinculado a otra cuenta."
            )
            mensaje.value = "No se pudo actualizar el perfil. Revisa tus datos."
            mensaje.color = ft.Colors.RED_700
            page.update()
            return
        if not actualizar_preferencias(
            usuario,
            lista_intereses,
            lista_evitar,
            dieta=preferencias.value,
        ):
            mensaje.value = "No se guardaron las preferencias. Indica como máximo 20 valores."
            mensaje.color = ft.Colors.RED_700
            page.update()
            return
        mensaje.value = "Preferencias guardadas. Tus siguientes recomendaciones tendrán en cuenta estos datos."
        mensaje.color = ft.Colors.GREEN_800
        page.update()

    controles = [
        ft.Text("Tu perfil gastronómico", size=28, weight=ft.FontWeight.BOLD, color="#174D3C"),
        nombre,
        correo,
        ft.Text(
            "Usamos las preferencias y las exclusiones que indiques para ordenar las sugerencias. "
            "Puedes cambiarlas cuando quieras."
        ),
        preferencias,
        intereses,
        evitar,
        ft.FilledButton("Guardar preferencias", icon=ft.Icons.SAVE, on_click=guardar),
        mensaje,
        ft.Divider(),
        ft.Text("Tus favoritos", size=20, weight=ft.FontWeight.BOLD, color="#174D3C"),
    ]
    if favoritos:
        for plato in favoritos:
            controles.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOKMARK, color="#D99A32"),
                    title=ft.Text(plato.nombre),
                    subtitle=ft.Text(f"{plato.categoria} · {plato.departamento}"),
                )
            )
    else:
        controles.append(ft.Text("Todavía no has guardado fichas."))

    return ft.Column(
        controles,
        spacing=14,
        width=680,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
