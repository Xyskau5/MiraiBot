import time
import amino
from PIL import Image, ImageDraw, ImageFont
from pymino import Bot
from pymino.ext import Context

# Configuración inicial de Amino
client = amino.Client("TuToken")
client.login(email="TuEmail", password="TuContraseña")
print("¡Inicio de sesión exitoso!")
comId = "ID de tu Comunidad"
sub_client = amino.SubClient(comId=comId, profile=client.profile)
print("Monitoreo de chat...")


# Lista de usuarios permitidos (agrega los IDs de los usuarios que pueden acceder al chat)
usuarios_permitidos = ["ID1", "ID2", "ID3"]

# Definición de variables y funciones relacionadas con el sistema de niveles
WARNS = []
ANTI_SPAM = {}
JOIN_LEAVE_DETECTOR = {}
USER_LEVELS = {}

# Función para comprobar el nivel de un usuario y calcular la experiencia necesaria para subir de nivel
def check_level(user_id):
    if user_id in USER_LEVELS:
        current_level = USER_LEVELS[user_id]["level"]
        current_exp = USER_LEVELS[user_id]["exp"]
    else:
        current_level = 1
        current_exp = 0

    # Calcula la experiencia necesaria para el próximo nivel (puedes ajustar este cálculo)
    next_level_exp = current_level * 100  # Por ejemplo, necesitas 100 puntos de experiencia por nivel

    # Calcula la experiencia restante para subir de nivel
    exp_needed = next_level_exp - current_exp

    # Crea una barra de experiencia visual (imagen) con el nivel actual y la experiencia
    exp_bar_image = create_exp_bar(current_level, current_exp, next_level_exp)

    # Devuelve un mensaje con el nivel y la barra de experiencia
    return f"Nivel: {current_level}\nExperiencia: {current_exp}/{next_level_exp}", exp_bar_image

# Función para crear una imagen de la barra de experiencia
def create_exp_bar(level, current_exp, next_level_exp):
    # Crea una imagen en blanco
    exp_bar_image = Image.new('RGB', (400, 100), color=(255, 255, 255))

    # Crea un objeto ImageDraw para dibujar en la imagen
    draw = ImageDraw.Draw(exp_bar_image)

    # Dibuja el fondo de la barra de experiencia
    draw.rectangle([10, 40, 390, 60], outline=(0, 0, 0), width=2, fill=(220, 220, 220))

    # Calcula el ancho de la barra de experiencia proporcionalmente
    exp_width = int(380 * (current_exp / next_level_exp))

    # Dibuja la barra de experiencia actual
    draw.rectangle([12, 42, 12 + exp_width, 58], outline=(0, 0, 0), fill=(0, 128, 255))

    # Dibuja el texto del nivel actual
    font = ImageFont.truetype("arial.ttf", 18)
    text = f"Nivel {level}"
    text_width, text_height = draw.textsize(text, font=font)
    draw.text(((400 - text_width) // 2, 10), text, fill=(0, 0, 0), font=font)

    # Guarda la imagen en un archivo temporal
    exp_bar_image.save("exp_bar.png")

    return exp_bar_image

# Función para dar la bienvenida a un usuario
def welcome_user(user_id):
    user_info = client.get_user_info(userId=user_id)
    user_nickname = user_info.nickname
    user_profile_link = f"https://aminoapps.com/u/{user_info.userId}"

    # Crea una imagen de bienvenida con el enlace del perfil del usuario
    welcome_image = create_welcome_image(user_nickname, user_profile_link)

    # Ahora puedes enviar la imagen en el chat
    sub_client.send_message(chatId=sub_client.get_chat_threads()[0].chatId, content="¡Bienvenido!", embedId="welcome_image.png")
# Función para dar la bienvenida a un usuario
def welcome_user(user_id):
    user_info = client.get_user_info(userId=user_id)
    user_nickname = user_info.nickname
    user_profile_link = f"https://aminoapps.com/u/{user_info.userId}"

    # Crea una imagen de bienvenida con el enlace del perfil del usuario
    welcome_image = create_welcome_image(user_nickname, user_profile_link)


# Función para expulsar a un usuario por comando
@bot.command(command_name="kick", command_description="Expulsa a un usuario por comando", aliases=["Kick", "KICK"], cooldown=0)
def kick(ctx: Context, user_to_kick: str):
    user_to_kick_id = None
    mentioned_users = ctx.message.mentions
    if mentioned_users:
        user_to_kick_id = mentioned_users[0].userId
    elif user_to_kick:
        try:
            user_info = sub_client.get_user_info(nickname=user_to_kick)
            user_to_kick_id = user_info.userId
        except amino.exceptions.UserNotFound:
            return ctx.reply("No se encontró al usuario.")

    if user_to_kick_id:
        sub_client.kick(chatId=ctx.message.chatId, userId=user_to_kick_id, allowRejoin=False)
        return ctx.reply(f"Usuario expulsado: {user_to_kick}")

# Comando para habilitar/deshabilitar la vista solo en el chat
@bot.command(command_name="viewonly", command_description="Hace que el chat sea solo de lectura", aliases=["Viewonly", "VIEWONLY"], cooldown=0)
def viewonly(ctx: Context, option: str):
    if option.lower() == "on":
        bot.community.set_view_only(viewOnly=True, chatId=ctx.message.chatId, comId=ctx.message.comId)
        return ctx.reply("El chat ahora es solo de lectura.")
    elif option.lower() == "off":
        bot.community.set_view_only(viewOnly=False, chatId=ctx.message.chatId, comId=ctx.message.comId)
        return ctx.reply("El chat ya no es solo de lectura.")
    else:
        return ctx.reply("Por favor, ingresa una opción válida (on/off).")

# Función para monitorear el chat y realizar acciones en función de los mensajes
@client.event("on_text_message")
def on_text_message(data):
    user_id = data.message.author.userId
    chat_id = data.message.chatId
    message_content = data.message.content

    # Agrega aquí tus acciones en función del contenido del mensaje
    if message_content.startswith("!comando1"):
        # Realiza una acción específica para !comando1
        pass
    elif message_content.startswith("!comando2"):
        # Realiza una acción específica para !comando2
        pass

    # Continúa agregando más condiciones y acciones según sea necesario


# Configuración del bot de pymino
bot = Bot(
    community_id="TuCommunityID"
)

@bot.on_member_join()
def on_member_join(ctx: Context):
    ctx.reply("Envía $verify para continuar.")
    response = ctx.wait_for_message("$verify", 15)

    if response is None:
        bot.community.kick(
            userId=ctx.userId,
            allowRejoin=True
        )

# Inicia el bot de pymino
bot.run("TuCommunityID", "TuBotToken")

# Función para responder cuando mencionan "Mirai"
@client.event("on_text_message")
def on_text_message(data):
    user_id = data.message.author.userId
    chat_id = data.message.chatId
    message_content = data.message.content.lower()  # Convertir el mensaje a minúsculas para facilitar la detección

    if "Mirai" in message_content:
        # Responder con el mensaje deseado
        response = "[IC] Aquí estoy ¿Necesitas algo?"
        sub_client.send_message(chatId=chat_id, content=response)
        

# Lista de nicknames baneados por los administradores
nicks_baneados = ["nickname1", "nickname2", "nickname3"]  # Agrega los nicknames baneados aquí

# Función para verificar si un nickname está baneado
def is_nick_baneado(nickname):
    return nickname.lower() in [nick.lower() for nick in nicks_baneados]

# Función para realizar la verificación y expulsión
def verificar_y_expulsar():
    try:
        # Obtener los últimos 50 usuarios de la comunidad
        users = sub_client.get_all_users(start=0, size=50)

        # Iterar a través de los usuarios
        for user in users:
            nickname = user.nickname
            if is_nick_baneado(nickname):
                # Expulsar al usuario de la comunidad si su nickname está baneado
                sub_client.ban(userId=user.userId)
                print(f"Usuario baneado de la comunidad: {nickname} (Nickname baneado)")

    except Exception as e:
        print(f"Error al verificar y banear: {str(e)}")
        # Comando para activar la verificación
@client.command("MVigilant")
def m_vigilant(data):
    print("Comando !MVigilant activado.")
    
    for _ in range(900):  # 900 ciclos para una media hora (2 segundos x 900 = 1800 segundos)
        verificar_y_expulsar()
        time.sleep(2)  # Esperar 2 segundos entre cada verificación

    print("Comando !MVigilant desactivado después de media hora.")

# Mantener el bot en funcionamiento
client.listen()
