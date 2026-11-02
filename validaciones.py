def validar_nombre(nombre: str) -> str | None:
    if not isinstance(nombre, str):
        return "El nombre es obligatorio."
    nombre = nombre.strip()
    if len(nombre) < 2:
        return "El nombre debe tener al menos 2 caracteres."
    if len(nombre) > 80:
        return "El nombre no puede superar los 80 caracteres."
    incluye_letra = False
    for caracter in nombre:
        if caracter.isalpha():
            incluye_letra = True
    if not incluye_letra:
        return "El nombre debe incluir al menos una letra."
    return None


def validar_correo(correo: str) -> str | None:
    if not isinstance(correo, str):
        return "Escribe un correo válido, por ejemplo nombre@dominio.com."
    correo = correo.strip()
    mensaje_error = "Escribe un correo válido, por ejemplo nombre@dominio.com."
    if len(correo) > 254 or correo.count("@") != 1:
        return "Escribe un correo válido, por ejemplo nombre@dominio.com."

    nombre_correo, dominio = correo.split("@")
    caracteres_nombre = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.!#$%&'*+/=?^_`{|}~-"
    for caracter in nombre_correo:
        if caracter not in caracteres_nombre:
            return mensaje_error
    if not nombre_correo:
        return mensaje_error

    partes_dominio = dominio.split(".")
    if len(partes_dominio) < 2:
        return mensaje_error

    caracteres_dominio = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"
    letras_y_numeros = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for parte in partes_dominio:
        if not parte or len(parte) > 63:
            return mensaje_error
        if parte[0] not in letras_y_numeros or parte[-1] not in letras_y_numeros:
            return mensaje_error
        for caracter in parte:
            if caracter not in caracteres_dominio:
                return mensaje_error
    return None


def validar_usuario(usuario: str) -> str | None:
    if not isinstance(usuario, str):
        return "Escribe un nombre de usuario válido."
    usuario = usuario.strip()
    if len(usuario) < 3 or len(usuario) > 30:
        return "El usuario debe tener entre 3 y 30 caracteres: letras, números, punto, guion o guion bajo."
    caracteres_permitidos = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
    for caracter in usuario:
        if caracter not in caracteres_permitidos:
            return "El usuario debe tener entre 3 y 30 caracteres: letras, números, punto, guion o guion bajo."
    return None


def validar_contrasena(contrasena: str) -> str | None:
    if not isinstance(contrasena, str):
        return "Escribe una contraseña válida."
    if len(contrasena) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if len(contrasena) > 128:
        return "La contraseña no puede superar los 128 caracteres."
    tiene_letra = False
    tiene_numero = False
    for caracter in contrasena:
        if caracter.isalpha():
            tiene_letra = True
        if caracter.isdigit():
            tiene_numero = True
    if not tiene_letra or not tiene_numero:
        return "Combina al menos una letra y un número en la contraseña."
    return None


def validar_telefono(telefono: str, obligatorio: bool = False) -> str | None:
    if not isinstance(telefono, str):
        return "Escribe un número de teléfono válido."
    telefono = telefono.strip()
    if not telefono and not obligatorio:
        return None
    cantidad_digitos = 0
    caracteres_permitidos = "0123456789+().-"
    for caracter in telefono:
        if caracter.isdigit():
            cantidad_digitos += 1
        if caracter not in caracteres_permitidos and not caracter.isspace():
            return "El teléfono debe contener entre 7 y 15 dígitos y solo usar +, espacios, guiones o paréntesis."
    if cantidad_digitos < 7 or cantidad_digitos > 15:
        return "El teléfono debe contener entre 7 y 15 dígitos y solo usar +, espacios, guiones o paréntesis."
    return None


def validar_texto(
    valor: str,
    campo: str,
    minimo: int = 1,
    maximo: int = 500,
) -> str | None:
    if not isinstance(valor, str):
        return f"{campo} debe ser texto."
    longitud = len(valor.strip())
    if longitud < minimo:
        return f"{campo} debe tener al menos {minimo} caracteres."
    if longitud > maximo:
        return f"{campo} no puede superar los {maximo} caracteres."
    return None


def validar_lista_separada(
    valor: str,
    campo: str,
    maximo_elementos: int = 20,
) -> tuple[list[str], str | None]:
    if not isinstance(valor, str):
        return [], f"Revisa los valores indicados en {campo}."
    elementos_unicos = []
    for elemento in valor.split(","):
        elemento = elemento.strip()
        if elemento and elemento not in elementos_unicos:
            elementos_unicos.append(elemento)
    if len(elementos_unicos) > maximo_elementos:
        return [], f"Indica como máximo {maximo_elementos} opciones en {campo}."
    for elemento in elementos_unicos:
        if len(elemento) > 60:
            return [], f"Cada opción de {campo} debe tener 60 caracteres o menos."
    return elementos_unicos, None
