import flet as ft

from datos import lista_platos, restaurantes_por_codigo, usuarios_por_codigo
from funciones import (
    obtener_reportes_pendientes,
    obtener_solicitudes_pendientes,
    obtener_solicitudes_representante,
    proponer_actualizacion_establecimiento,
    resolver_reporte,
    revisar_solicitud,
)


VERDE = "#174D3C"
CREMA = "#F7F4EB"


def mostrar_panel_representante(page, usuario, al_actualizar):
    restaurante = restaurantes_por_codigo.get(usuario.establecimiento_codigo)
    if restaurante is None or restaurante.representante_codigo != usuario.codigo:
        return ft.Column(
            [
                ft.Text("No hay un establecimiento asociado a esta cuenta.", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("La información de tu establecimiento está protegida y no puede consultarse desde otra cuenta."),
            ],
            spacing=12,
        )

    solicitudes = obtener_solicitudes_representante(usuario)
    estados = ft.Column(spacing=8)
    for solicitud in reversed(solicitudes):
        estados.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"{solicitud.tipo} · {solicitud.estado}",
                            weight=ft.FontWeight.BOLD,
                            color=VERDE,
                        ),
                        ft.Text(solicitud.observaciones or "Sin observaciones del equipo editorial."),
                    ],
                    spacing=4,
                ),
                padding=12,
                bgcolor=CREMA,
                border_radius=10,
            )
        )

    lista_estados = ft.Text("Aún no hay solicitudes registradas.")
    if estados.controls:
        lista_estados = estados

    nombre = ft.TextField(label="Nombre público", value=restaurante.nombre)
    tipo = ft.TextField(label="Tipo", value=restaurante.tipo)
    descripcion = ft.TextField(
        label="Descripción breve",
        value=restaurante.descripcion,
        multiline=True,
        min_lines=2,
        max_lines=3,
    )
    departamento = ft.TextField(
        label="Departamento",
        value=restaurante.departamento,
    )
    municipio = ft.TextField(label="Municipio", value=restaurante.municipio)
    direccion = ft.TextField(
        label="Dirección o referencia",
        value=restaurante.direccion,
    )
    horario = ft.TextField(label="Horario", value=restaurante.horario)
    contacto = ft.TextField(label="Contacto público", value=restaurante.contacto)
    especialidad = ft.TextField(
        label="Platillos/bebidas destacados",
        value=restaurante.especialidad,
    )
    mensaje = ft.Text()

    def enviar(evento):
        datos = {
            "nombre": nombre.value or "",
            "tipo": tipo.value or "",
            "descripcion": descripcion.value or "",
            "departamento": departamento.value or "",
            "municipio": municipio.value or "",
            "direccion": direccion.value or "",
            "horario": horario.value or "",
            "contacto": contacto.value or "",
            "especialidad": especialidad.value or "",
        }
        try:
            proponer_actualizacion_establecimiento(usuario, datos)
        except ValueError as error:
            mensaje.value = str(error)
            mensaje.color = ft.Colors.RED_700
            page.update()
            return
        mensaje.value = "Propuesta enviada; la versión pública anterior se conserva hasta su aprobación."
        mensaje.color = ft.Colors.GREEN_800
        al_actualizar()

    publicacion = "Ficha no pública hasta completar la revisión editorial."
    if restaurante.estado == "Aprobado":
        publicacion = "Ficha visible en la guía"
    controles = [
        ft.Text("Panel del establecimiento", size=28, weight=ft.FontWeight.BOLD, color=VERDE),
        ft.Text(f"{restaurante.nombre} · Estado: {restaurante.estado}"),
        ft.Text(publicacion),
        ft.Text("Seguimiento de solicitudes", size=20, weight=ft.FontWeight.BOLD),
        lista_estados,
        ft.Divider(),
        ft.Text("Proponer una actualización", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Los cambios se guardan como propuesta y requieren aprobación. "
            "Solo puedes enviar información de tu establecimiento."
        ),
    ]
    controles.extend(
        [
            nombre,
            tipo,
            descripcion,
            departamento,
            municipio,
            direccion,
            horario,
            contacto,
            especialidad,
            ft.FilledButton(
                "Enviar a revisión editorial",
                icon=ft.Icons.OUTGOING_MAIL,
                on_click=enviar,
            ),
            mensaje,
        ]
    )

    return ft.Column(
        controles,
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def _crear_tarjeta_solicitud(page, solicitud, al_actualizar):
    restaurante = restaurantes_por_codigo[solicitud.restaurante_codigo]
    representante = usuarios_por_codigo[solicitud.representante_codigo]
    observaciones = ft.TextField(
        label="Observaciones para el representante",
        multiline=True,
        min_lines=2,
        max_lines=4,
    )
    datos = solicitud.datos_propuestos
    resumen = "\n".join(
        [
            f"Tipo de solicitud: {solicitud.tipo}",
            f"Representante: {representante.nombre} · {representante.correo}",
            f'Establecimiento: {datos.get("nombre", restaurante.nombre)}',
            f'Categoría: {datos.get("tipo", restaurante.tipo)}',
            f'Especialidad: {datos.get("especialidad", "No indicada")}',
            f'Ubicación: {datos.get("direccion", restaurante.direccion)}, '
            f'{datos.get("municipio", restaurante.municipio)}, '
            f'{datos.get("departamento", restaurante.departamento)}',
            f'Horario: {datos.get("horario", "No indicado")}',
            f'Descripción: {datos.get("descripcion", restaurante.descripcion)}',
        ]
    )

    def resolver_solicitud(decision):
        if decision != "Aprobada" and not (observaciones.value or "").strip():
            observaciones.error = "Indica el motivo o los cambios que se deben realizar."
            page.update()
            return
        revisar_solicitud(
            solicitud.codigo,
            decision,
            observaciones.value or "",
        )
        al_actualizar()

    def aprobar(evento):
        resolver_solicitud("Aprobada")

    def devolver(evento):
        resolver_solicitud("Requiere correcciones")

    def rechazar(evento):
        resolver_solicitud("Rechazada")

    botones = ft.Row(
        [
            ft.FilledButton(
                "Aprobar y publicar",
                icon=ft.Icons.PUBLISH,
                on_click=aprobar,
            ),
            ft.OutlinedButton(
                "Devolver para correcciones",
                icon=ft.Icons.EDIT_NOTE,
                on_click=devolver,
            ),
            ft.TextButton(
                "Rechazar",
                icon=ft.Icons.BLOCK,
                on_click=rechazar,
            ),
        ],
        wrap=True,
    )
    contenido = ft.Column(
        [ft.Text(resumen, selectable=True), observaciones, botones],
        spacing=10,
    )
    return ft.Card(
        content=ft.Container(
            content=contenido,
            padding=16,
            bgcolor=CREMA,
        )
    )


def _crear_tarjeta_reporte(reporte, al_actualizar):
    plato = None
    for elemento in lista_platos:
        if elemento.codigo == reporte.plato_codigo:
            plato = elemento
            break

    autor = usuarios_por_codigo.get(reporte.usuario_codigo)
    nombre_plato = reporte.plato_codigo
    if plato is not None:
        nombre_plato = plato.nombre

    nombre_autor = "Cuenta eliminada"
    if autor is not None:
        nombre_autor = autor.nombre

    def marcar_como_revisado(evento):
        resolver_reporte(reporte.codigo)
        al_actualizar()

    titulo = f"Reporte sobre {nombre_plato} · {nombre_autor}"
    contenido = ft.Column(
        [
            ft.Text(titulo, weight=ft.FontWeight.BOLD),
            ft.Text(reporte.comentario),
            ft.OutlinedButton(
                "Marcar como revisado",
                icon=ft.Icons.DONE,
                on_click=marcar_como_revisado,
            ),
        ],
        spacing=8,
    )
    return ft.Card(
        content=ft.Container(
            content=contenido,
            padding=14,
        )
    )


def mostrar_revision_editorial(page, al_actualizar):
    solicitudes = obtener_solicitudes_pendientes()
    reportes = obtener_reportes_pendientes()
    controles = [
        ft.Text("Revisión editorial", size=28, weight=ft.FontWeight.BOLD, color=VERDE),
        ft.Text(
            "Las fichas propuestas no aparecen en el catálogo ni en recomendaciones hasta aprobarse."
        ),
        ft.Text(f"Solicitudes pendientes: {len(solicitudes)}", size=19, weight=ft.FontWeight.BOLD),
    ]

    for solicitud in solicitudes:
        tarjeta = _crear_tarjeta_solicitud(page, solicitud, al_actualizar)
        controles.append(tarjeta)

    controles.extend(
        [
            ft.Divider(),
            ft.Text(f"Reportes de contenido pendientes: {len(reportes)}", size=19, weight=ft.FontWeight.BOLD),
        ]
    )
    for reporte in reportes:
        tarjeta = _crear_tarjeta_reporte(reporte, al_actualizar)
        controles.append(tarjeta)
    if not solicitudes and not reportes:
        controles.append(ft.Text("La cola editorial está al día."))
    return ft.Column(controls=controles, spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
