import flet as ft

from funciones import obtener_directorio_usuarios, listar_platos


def mostrar_dashboard(page: ft.Page):
    banner = ft.Image(
        src="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80",
        width=900,
        height=220,
        fit=ft.BoxFit.COVER,
        border_radius=18,
    )

    titulo = ft.Text(
        value="NICACRAVE",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    descripcion = ft.Text(
        value="Raíces en cada bocado · Guía cultural de la gastronomía nicaragüense",
        size=16,
    )

    total_usuarios = len(obtener_directorio_usuarios())
    total_platos = len(listar_platos())

    estadisticas = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Usuarios registrados",
                            color=ft.Colors.BLUE_GREY_900,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            str(total_usuarios),
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                    tight=True,
                ),
                padding=12,
                bgcolor=ft.Colors.BLUE_GREY_50,
                border_radius=12,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Platos disponibles",
                            color=ft.Colors.BLUE_GREY_900,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            str(total_platos),
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                    tight=True,
                ),
                padding=12,
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=12,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap=True,
    )

    galeria = ft.Row(
        controls=[
            ft.Image(
                src="https://images.unsplash.com/photo-1559847844-5315695dadae?auto=format&fit=crop&w=500&q=80",
                width=180,
                height=120,
                fit=ft.BoxFit.COVER,
                border_radius=14,
            ),
            ft.Image(
                src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=500&q=80",
                width=180,
                height=120,
                fit=ft.BoxFit.COVER,
                border_radius=14,
            ),
            ft.Image(
                src="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=500&q=80",
                width=180,
                height=120,
                fit=ft.BoxFit.COVER,
                border_radius=14,
            ),
        ],
        spacing=12,
        wrap=True,
    )

    return ft.Column(
        controls=[
            banner,
            titulo,
            descripcion,
            estadisticas,
            ft.Text("Nuestra cocina", size=22, weight=ft.FontWeight.BOLD),
            galeria,
        ],
        spacing=16,
        width=900,
        scroll=ft.ScrollMode.AUTO,
    )
