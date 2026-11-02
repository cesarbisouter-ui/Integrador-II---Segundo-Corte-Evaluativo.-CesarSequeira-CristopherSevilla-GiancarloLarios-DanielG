import flet as ft

from funciones import buscar_usuario, crear_solicitud_establecimiento, crear_usuario
from validaciones import (
    validar_contrasena,
    validar_correo,
    validar_nombre,
    validar_telefono,
    validar_usuario,
)


VERDE = "#174D3C"
ORO = "#D99A32"


def _campo(label, **kwargs):
    return ft.TextField(label=label, **kwargs)


def _mostrar_dialogo(page, titulo, contenido, acciones):
    def cerrar_dialogo(evento):
        page.pop_dialog()

    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text(titulo, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        tooltip="Cerrar ventana",
                        on_click=cerrar_dialogo,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(content=contenido, width=440),
            actions=acciones,
            scrollable=True,
        )
    )


def _registro_personal(page, on_success, dentro_dialogo_acceso=True):
    nombre = _campo("Nombre visible", max_length=80)
    correo = _campo("Correo electrónico", keyboard_type=ft.KeyboardType.EMAIL, max_length=254)
    usuario = _campo("Nombre de usuario", max_length=30)
    contraseña = _campo("Contraseña", password=True, can_reveal_password=True)
    dieta = ft.Dropdown(
        label="Preferencia alimentaria",
        value="Omnívora",
        options=[
            ft.DropdownOption(key="Omnívora", text="Omnívora"),
            ft.DropdownOption(key="Tradicional", text="Tradicional"),
            ft.DropdownOption(key="Vegetariana", text="Vegetariana"),
            ft.DropdownOption(key="Vegana", text="Vegana"),
            ft.DropdownOption(key="Sin gluten", text="Sin gluten"),
        ],
    )
    privacidad = ft.Checkbox(
        label="He leído el aviso de privacidad y acepto guardar mis preferencias en esta aplicación.",
        value=False,
    )
    mensaje = ft.Text(color=ft.Colors.RED_700)

    def guardar(e):
        if not privacidad.value:
            mensaje.value = "Confirma el aviso de privacidad para continuar."
            page.update()
            return
        nombre.error = validar_nombre(nombre.value or "")
        correo.error = validar_correo(correo.value or "")
        usuario.error = validar_usuario(usuario.value or "")
        contraseña.error = validar_contrasena(contraseña.value or "")
        if nombre.error or correo.error or usuario.error or contraseña.error:
            page.update()
            return
        cuenta = crear_usuario(
            nombre.value or "",
            correo.value or "",
            dieta.value or "Omnívora",
            usuario.value or "",
            contraseña.value,
            "Cliente",
        )
        if cuenta is None:
            mensaje.value = "Revisa los datos. El correo o usuario puede estar registrado."
            page.update()
            return
        page.pop_dialog()
        if dentro_dialogo_acceso:
            page.pop_dialog()
        on_success(cuenta)
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Cuenta creada. Ya puedes personalizar tus recomendaciones."),
                bgcolor=VERDE,
            )
        )

    contenido = ft.Column(
        [
            ft.Text("Crea un perfil para guardar tus preferencias y retroalimentación."),
            nombre,
            correo,
            usuario,
            contraseña,
            dieta,
            privacidad,
            mensaje,
        ],
        spacing=10,
        tight=True,
        scroll=ft.ScrollMode.AUTO,
    )

    def cancelar(evento):
        page.pop_dialog()

    _mostrar_dialogo(
        page,
        "Crear cuenta personal",
        contenido,
        [
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.FilledButton("Crear cuenta", icon=ft.Icons.PERSON_ADD, on_click=guardar),
        ],
    )


def _registro_establecimiento(page, on_success, dentro_dialogo_acceso=True):
    campos = {
        "representante": _campo("Nombre de la persona responsable", max_length=80),
        "correo": _campo("Correo electrónico", keyboard_type=ft.KeyboardType.EMAIL, max_length=254),
        "telefono": _campo("Teléfono de contacto", keyboard_type=ft.KeyboardType.PHONE, max_length=24),
        "usuario": _campo("Nombre de usuario", max_length=30),
        "contraseña": _campo("Contraseña", password=True, can_reveal_password=True),
        "nombre": _campo("Nombre público del establecimiento", max_length=100),
        "tipo": _campo("Tipo de establecimiento (cafetería, comedor...)", max_length=50),
        "descripcion": _campo("Descripción breve", multiline=True, min_lines=2, max_lines=3, max_length=500),
        "departamento": _campo("Departamento", max_length=60),
        "municipio": _campo("Municipio", max_length=60),
        "direccion": _campo("Dirección o referencia", max_length=200),
        "horario": _campo("Horario (opcional)", max_length=120),
        "contacto": _campo("Contacto público (opcional)", max_length=80),
        "especialidad": _campo("Platillos o bebidas representativos (opcional)", max_length=160),
    }
    privacidad = ft.Checkbox(
        label="Declaro que puedo compartir la información enviada y que tengo autorización sobre las imágenes.",
        value=False,
    )
    mensaje = ft.Text(color=ft.Colors.RED_700)

    def guardar(e):
        if not privacidad.value:
            mensaje.value = "Confirma la declaración para enviar la solicitud."
            page.update()
            return
        campos["representante"].error = validar_nombre(
            campos["representante"].value or ""
        )
        campos["correo"].error = validar_correo(campos["correo"].value or "")
        campos["telefono"].error = validar_telefono(
            campos["telefono"].value or "", obligatorio=True
        )
        campos["usuario"].error = validar_usuario(campos["usuario"].value or "")
        campos["contraseña"].error = validar_contrasena(
            campos["contraseña"].value or ""
        )
        hay_errores = False
        for campo in campos.values():
            if campo.error:
                hay_errores = True
        if hay_errores:
            page.update()
            return
        try:
            cuenta, _ = crear_solicitud_establecimiento(
                campos["representante"].value or "",
                campos["correo"].value or "",
                campos["telefono"].value or "",
                campos["usuario"].value or "",
                campos["contraseña"].value,
                campos["nombre"].value or "",
                campos["tipo"].value or "",
                campos["descripcion"].value or "",
                campos["departamento"].value or "",
                campos["municipio"].value or "",
                campos["direccion"].value or "",
                campos["horario"].value or "",
                campos["contacto"].value or "",
                campos["especialidad"].value or "",
            )
        except ValueError as error:
            mensaje.value = str(error)
            page.update()
            return
        page.pop_dialog()
        if dentro_dialogo_acceso:
            page.pop_dialog()
        on_success(cuenta)
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Solicitud enviada. La ficha no será pública hasta su aprobación editorial."),
                bgcolor=VERDE,
            )
        )

    contenido = [
        ft.Text(
            "La solicitud queda pendiente de revisión. El registro es local y no envía un correo de verificación.",
            size=13,
            color=ft.Colors.BLUE_GREY_700,
        )
    ]
    for campo in campos.values():
        contenido.append(campo)
    contenido.extend([privacidad, mensaje])

    def cancelar(evento):
        page.pop_dialog()

    contenido = ft.Column(
        contenido,
        spacing=9,
        tight=True,
        scroll=ft.ScrollMode.AUTO,
    )
    _mostrar_dialogo(
        page,
        "Registrar establecimiento",
        contenido,
        [
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.FilledButton("Enviar solicitud", icon=ft.Icons.OUTGOING_MAIL, on_click=guardar),
        ],
    )


def mostrar_login(
    page: ft.Page,
    on_login_success,
    dentro_dialogo_acceso=True,
):
    intentos = 0
    usuario = _campo(
        "Cargo o usuario",
        hint_text="admin, recepcionista o tu usuario",
        autofocus=True,
        max_length=254,
    )
    contraseña = _campo("Contraseña", password=True, can_reveal_password=True)
    mensaje = ft.Text(color=ft.Colors.RED_700)

    def ingresar(e):
        nonlocal intentos
        usuario.error = (
            "Escribe tu cargo o usuario."
            if not (usuario.value or "").strip()
            else None
        )
        contraseña.error = (
            "Escribe tu contraseña."
            if not (contraseña.value or "")
            else None
        )
        if usuario.error or contraseña.error:
            mensaje.value = "Escribe tu cargo y contraseña para continuar."
            page.update()
            return
        cargo = (usuario.value or "").strip()
        if cargo.casefold() == "recepcionista":
            cargo = "recepcion"
        encontrado = buscar_usuario(cargo, contraseña.value or "")
        if encontrado:
            if dentro_dialogo_acceso:
                page.pop_dialog()
            on_login_success(encontrado)
            return
        intentos += 1
        if intentos >= 3:
            mensaje.value = (
                "Tres intentos fallidos. Comprueba tu cargo y contraseña "
                "y vuelve a intentar."
            )
            intentos = 0
        else:
            mensaje.value = f"Cargo o contraseña incorrectos. Intento {intentos} de 3."
        page.update()

    def abrir_registro_personal(evento):
        _registro_personal(page, on_login_success, dentro_dialogo_acceso)

    def abrir_registro_establecimiento(evento):
        _registro_establecimiento(page, on_login_success, dentro_dialogo_acceso)

    boton = ft.FilledButton(
        "Ingresar",
        icon=ft.Icons.LOGIN,
        on_click=ingresar,
    )
    contenido = ft.Column(
        [
            ft.Row(
                [ft.Icon(ft.Icons.RICE_BOWL, color=ORO, size=30), ft.Text("NICACRAVE", size=20, weight=ft.FontWeight.BOLD, color=VERDE)],
                spacing=8,
            ),
            ft.Text("Escribe tu cargo y contraseña para ingresar."),
            usuario,
            contraseña,
            mensaje,
            boton,
            ft.Divider(),
            ft.Text("¿Eres nuevo?"),
            ft.OutlinedButton(
                "Crear cuenta personal",
                icon=ft.Icons.PERSON_ADD,
                on_click=abrir_registro_personal,
            ),
            ft.OutlinedButton(
                "Registrar un establecimiento",
                icon=ft.Icons.STORE_MALL_DIRECTORY,
                on_click=abrir_registro_establecimiento,
            ),
        ],
        spacing=12,
        tight=True,
    )
    return contenido
