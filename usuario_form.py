import flet as ft

from funciones import crear_usuario
from validaciones import (
    validar_contrasena,
    validar_correo,
    validar_nombre,
    validar_usuario,
)


def mostrar_formulario_usuario(page: ft.Page, on_guardado):
    nombre = ft.TextField(label="Nombre completo", max_length=80)
    correo = ft.TextField(label="Correo", keyboard_type=ft.KeyboardType.EMAIL, max_length=254)
    dieta = ft.Dropdown(
        label="Dieta preferida",
        value="Omnívora",
        options=[
            ft.DropdownOption(key="Omnívora", text="Omnívora"),
            ft.DropdownOption(key="Vegetariana", text="Vegetariana"),
            ft.DropdownOption(key="Vegana", text="Vegana"),
        ],
    )
    usuario_login = ft.TextField(label="Usuario para iniciar sesión", max_length=30)
    contraseña = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
    )
    rol = ft.Dropdown(
        label="Rol",
        value="Cliente",
        options=[
            ft.DropdownOption(key="Cliente", text="Cliente"),
            ft.DropdownOption(key="Recepción", text="Recepción"),
            ft.DropdownOption(key="Editor", text="Editor"),
            ft.DropdownOption(key="Administrador", text="Administrador"),
        ],
    )
    mensaje = ft.Text()

    def guardar(evento):
        nombre.error = validar_nombre(nombre.value or "")
        correo.error = validar_correo(correo.value or "")
        usuario_login.error = validar_usuario(usuario_login.value or "")
        contraseña.error = validar_contrasena(contraseña.value or "")
        if (
            nombre.error
            or correo.error
            or usuario_login.error
            or contraseña.error
        ):
            page.update()
            return

        if (
            not nombre.value
            or not nombre.value.strip()
            or not correo.value
            or not correo.value.strip()
            or not usuario_login.value
            or not usuario_login.value.strip()
            or not contraseña.value
            or not contraseña.value.strip()
            or not dieta.value
            or not rol.value
        ):
            mensaje.value = "Completa todos los campos."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        usuario = crear_usuario(
            nombre.value.strip(),
            correo.value.strip(),
            dieta.value,
            usuario_login.value.strip(),
            contraseña.value,
            rol.value,
        )
        if usuario is None:
            mensaje.value = "El nombre de usuario o el correo ya están registrados."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        on_guardado()
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                content="Usuario registrado correctamente.",
                bgcolor=ft.Colors.GREEN_700,
            )
        )

    boton_guardar = ft.Button(
        "Guardar",
        icon=ft.Icons.SAVE,
        on_click=guardar,
    )

    def cerrar_formulario(evento):
        page.pop_dialog()

    boton_cerrar = ft.Button(
        "Cerrar",
        icon=ft.Icons.CLOSE,
        on_click=cerrar_formulario,
    )

    return ft.Column(
        controls=[
            ft.Text("Nuevo usuario", size=24, weight=ft.FontWeight.BOLD),
            nombre,
            correo,
            dieta,
            usuario_login,
            contraseña,
            rol,
            mensaje,
            ft.Row(controls=[boton_guardar, boton_cerrar], spacing=10),
        ],
        spacing=12,
        tight=True,
        scroll=ft.ScrollMode.AUTO,
    )
