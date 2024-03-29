import telebot
from telebot import types
import requests
import urllib3
import datetime
import hashlib
import base58

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "6806884584:AAG2uB0PKWgQy2Cds8ft-NjYkT3bcwY2uaA"
bot = telebot.TeleBot(TOKEN)

base_url = 'https://digovil.pythonanywhere.com'

# Diccionario para almacenar el estado de sesión de los usuarios
user_sessions = {}

def encript_address(user_id):
    public_key = f"{user_id}".encode('utf-8')
    sha256_hash = hashlib.sha256(public_key).hexdigest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash.encode('utf-8')).hexdigest()
    address = base58.b58encode_check(bytes.fromhex("00" + ripemd160_hash)).decode('utf-8')
    return address

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
        bot.send_message(message.chat.id, f"¡Registro exitoso! Ahora estás registrado y conectado.\nTu dirección de billetera es: {encript_address(user_id)}")
    else:
        bot.send_message(message.chat.id, "Ya estás registrado. Si deseas iniciar sesión con otra cuenta, primero cierra sesión.")

# Comando para iniciar sesión
@bot.message_handler(commands=['login'])
def handle_login(message):
    user_id = message.from_user.id
    if user_id not in user_sessions or not user_sessions[user_id]['logged_in']:
        user_sessions[user_id] = {'logged_in': True, 'user_id': user_id}
        string = f"¡Inicio de sesión exitoso!\nTu dirección de billetera es: {encript_address(user_id)}"
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
        response = requests.get(f"{base_url}/balance/{encript_address(user_id)}", verify=False)
        bot.send_message(message.chat.id, response.text)
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para verificar tu saldo.")

# Comando para obtener historial de transacciones

@bot.message_handler(commands=['transactions'])
def handle_transactions(message):
    user_id = message.from_user.id
    if user_id in user_sessions and user_sessions[user_id]['logged_in']:
        response = requests.get(f"{base_url}/transactions/{encript_address(user_id)}", verify=False)
        transactions_data = response.json()

        if "recipient" in transactions_data and "sender" in transactions_data:
            recipient_transactions = transactions_data["recipient"]
            sender_transactions = transactions_data["sender"]

            message_text = "Tus últimas transacciones:\n\n"

            if recipient_transactions:
                message_text += "Recibiste:\n"
                for transaction in recipient_transactions:
                    amount = transaction['amount']
                    sender = transaction['sender']
                    timestamp = transaction.get('timestamp', None)
                    date_time = format_timestamp(timestamp) if timestamp else "No disponible"

                    message_text += f"{amount} de {sender} - {date_time}\n"

            if sender_transactions:
                message_text += "\nEnviaste:\n"
                for transaction in sender_transactions:
                    amount = transaction['amount']
                    recipient = transaction['recipient']
                    timestamp = transaction.get('timestamp', None)
                    date_time = format_timestamp(timestamp) if timestamp else "No disponible"

                    message_text += f"{amount} a {recipient} - {date_time}\n"

            bot.send_message(message.chat.id, message_text)
        else:
            bot.send_message(message.chat.id, "No hay transacciones disponibles.")
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para ver tu historial de transacciones.")

def format_timestamp(timestamp):
    # Convierte la marca de tiempo Unix a un objeto datetime y luego formatea la fecha y hora
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    formatted_date_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date_time

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
            payload = {'sender': str(encript_address(user_id)), 'recipient': str(encript_address(recipient)), 'amount': float(amount)}
            response = requests.post(f"{base_url}/transactions/new", json=payload, verify=False)
            bot.send_message(message.chat.id, response.text)
    else:
        bot.send_message(message.chat.id, "Debes iniciar sesión para realizar una transferencia.")

# Configurar los comandos para mostrar en la lista de comandos del bot
commands = [
    types.BotCommand("start", "Inicia el bot"),
    #types.BotCommand("help", "Muestra la lista de comandos disponibles"),
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
