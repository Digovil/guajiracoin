import telebot
from telebot import types
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "Tu_token"
bot = telebot.TeleBot(TOKEN)

base_url = 'https://1199-2800-484-d73-2000-c0e6-8716-2339-720e.ngrok-free.app'

# Diccionario para almacenar el estado de sesión de los usuarios
user_sessions = {}

# Comando de inicio para el bot de Telegram
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = {'logged_in': False, 'user_id': None}
        bot.send_message(message.chat.id, "¡Hola! Soy tu billetera de criptomoneda. Usa /help para ver los comandos disponibles.")
    else:
        bot.send_message(message.chat.id, "¡Bienvenido de nuevo!")

# Comando de ayuda para el bot de Telegram
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Los comandos disponibles son:\n"
                                      "/register - Registrarse\n"
                                      "/login - Iniciar sesión\n"
                                      "/logout - Cerrar sesión\n"
                                      "/balance - Verificar saldo\n"
                                      "/transactions - Ver historial de transacciones\n"
                                      "/transferir - Transferir criptomoneda a otro usuario\n")

# Comando para registrar un nuevo usuario
@bot.message_handler(commands=['register'])
def handle_register(message):
    user_id = message.from_user.id
    if user_id not in user_sessions or not user_sessions[user_id]['logged_in']:
        user_sessions[user_id] = {'logged_in': True, 'user_id': user_id}
        bot.send_message(message.chat.id, "¡Registro exitoso! Ahora estás registrado y conectado.")
    else:
        bot.send_message(message.chat.id, "Ya estás registrado. Si deseas iniciar sesión con otra cuenta, primero cierra sesión.")

# Comando para iniciar sesión
@bot.message_handler(commands=['login'])
def handle_login(message):
    user_id = message.from_user.id
    if user_id not in user_sessions or not user_sessions[user_id]['logged_in']:
        user_sessions[user_id] = {'logged_in': True, 'user_id': user_id}
        string = f"¡Inicio de sesión exitoso!\nTu dirección de billetera es: {user_id}"
        bot.send_message(message.chat.id, string)
    else:
        bot.send_message(message.chat.id, "Ya estás registrado e iniciado sesión.")

# Comando para cerrar sesión
@bot.message_handler(commands=['logout'])
def handle_logout(message):
    user_id = message.from_user.id
    if user_id in user_sessions and user_sessions[user_id]['logged_in']:
        user_sessions[user_id]['logged_in'] = False
        user_sessions[user_id]['user_id'] = None
        bot.send_message(message.chat.id, "¡Cierre de sesión exitoso!")
    else:
        bot.send_message(message.chat.id, "No estás registrado o ya has cerrado sesión.")

# Comando para verificar saldo
@bot.message_handler(commands=['balance'])
def handle_balance(message):
    user_id = message.from_user.id
    if user_id in user_sessions and user_sessions[user_id]['logged_in']:
        response = requests.get(f"{base_url}/balance/{user_id}", verify=False)
        bot.send_message(message.chat.id, response.text)
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para verificar tu saldo.")

# Comando para obtener historial de transacciones
@bot.message_handler(commands=['transactions'])
def handle_transactions(message):
    user_id = message.from_user.id
    if user_id in user_sessions and user_sessions[user_id]['logged_in']:
        response = requests.get(f"{base_url}/transactions/{user_id}", verify=False)
        bot.send_message(message.chat.id, response.text)
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para ver tu historial de transacciones.")

# # Comando para transferir criptomoneda
# @bot.message_handler(commands=['transferir'])
# def handle_transfer(message):
#     user_id = message.from_user.id
#     if user_id in user_sessions and user_sessions[user_id]['logged_in']:
#         bot.send_message(message.chat.id, "Por favor, proporciona la información de la transacción en el siguiente formato:\n"
#                                           "/transferir <destinatario> <cantidad>")
#     else:
#         bot.send_message(message.chat.id, "Debes iniciar sesión para realizar una transferencia.")

# Manejar el formato de transferencia proporcionado por el usuario
@bot.message_handler(regexp=r'/transferir (.+)')
def handle_transfer_info(message):
    user_id = message.from_user.id
    if user_id in user_sessions and user_sessions[user_id]['logged_in']:
        transfer_info = message.text.split()[1:]
        if len(transfer_info) != 2:
            bot.send_message(message.chat.id, "Formato incorrecto. Usa /transferir <destinatario> <cantidad>")
        else:
            recipient, amount = transfer_info
            payload = {'sender': str(user_id), 'recipient': str(recipient), 'amount': float(amount)}
            response = requests.post(f"{base_url}/transactions/new", json=payload, verify=False)
            bot.send_message(message.chat.id, response.text)
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para realizar una transferencia.")

# Configurar los comandos para mostrar en la lista de comandos del bot
commands = [
    types.BotCommand("start", "Inicia el bot"),
    types.BotCommand("help", "Muestra la lista de comandos disponibles"),
    types.BotCommand("register", "Registra un nuevo usuario"),
    types.BotCommand("login", "Inicia sesión"),
    types.BotCommand("logout", "Cierra sesión"),
    types.BotCommand("balance", "Verifica el saldo"),
    types.BotCommand("transactions", "Muestra el historial de transacciones"),
    types.BotCommand("transferir", "Transfiere criptomoneda a otro usuario")
]

# Configurar los comandos para el bot
bot.set_my_commands(commands)

if __name__ == "__main__":
    bot.polling()
