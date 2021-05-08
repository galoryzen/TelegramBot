from telegram import *
from telegram.ext import *
from config import TOKEN
import logging
import functions
import matplotlib.pyplot as plt
import networkx as nx

bot = Bot(token=TOKEN)

def start(update, context):
    name = update.message.chat["first_name"]
    bot.send_message(chat_id = update.effective_chat.id, text = f"¡Hola, {name} \U0001F44B!, un gusto tenerte por acá. Soy el bicho SIUUUU")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def helper(update, context):
    opciones = [
       [InlineKeyboardButton("Recurrencia", callback_data="op1")],
       [InlineKeyboardButton("Recurrencia con v.i", callback_data="op2")],
       [InlineKeyboardButton("Subsecuencia Fibonacci", callback_data="op3")],
       [InlineKeyboardButton("Grafo", callback_data="op4")]
    ]
    reply_markup = InlineKeyboardMarkup(opciones)
    name = update.message.chat["first_name"]
    bot.send_message(text=f"Hola {name}, estos son los comandos que puedo ejecutar:", reply_markup=reply_markup, chat_id=update.effective_chat.id)

def menu(update: Update, context):
    query = update.callback_query
    query.answer()
    answer = query.data
    chat_id = query.message.chat_id
    if answer == "op1":
        bot.send_message(chat_id = query.message.chat_id, text = "/recurrencia: \nNo implementado todavía")
    elif answer == "op2":
        bot.send_message(chat_id = query.message.chat_id, text = "/recurrenciavi: \nNo implementado todavía")
    elif answer == "op3":
        bot.send_message(chat_id = query.message.chat_id, text = "/subsecuencia: \nPara usar este comando, usted deberá utilizarlo de la siguiente manera: /subsecuencia v1 v2 v3 v4 v5 v6 ... vi\n"+
                                                                 "Recuerde ingresar los valores de la secuencia separados por espacios unicamente.")
    elif answer == "op4":
        bot.send_message(chat_id = query.message.chat_id, text = "/grafo: \nPara usar este comando, usted deberá utilizarlo de la siguiente manera: /grafo v e k Donde:\n"+
                                                                 "v: # de vertices del grafo\n"+
                                                                 "e: # de aristas del grafo\n"+
                                                                 "k:   valor máximo del grado de un vertice\n"+
                                                                 "Recuerde que los parametros deben ser enteros positivos, ej: /grafo 3 3 2")


def get_graph(update, context):
    parametros = ' '.join(context.args).strip().split(" ")

    try:                #Perform a check to see if parameters are valid
        parametros = [int(parametro) for parametro in parametros]
        for parametro in parametros:
            if parametro < 0:
                raise ValueError("Número negativo")
    except Exception:
        pass
        bot.send_message(chat_id = update.effective_chat.id, text = "Verifique sus parametros, estos deben ser números enteros separados por un espacio, ej: 1 3 4 5")
        return
    
    G = functions.generateGraph(parametros[0], parametros[1], parametros[2])
    if G != None:
        nx.draw(G)
        plt.savefig("graph.png")
        plt.close()
        bot.send_photo(chat_id=update.effective_chat.id, photo=open("graph.png", 'rb'), caption=f"Grafo con {parametros[0]} vertices, {parametros[1]} aristas y máximo grado {parametros[2]}")
    else:
        bot.send_message(chat_id = update.effective_chat.id, text = "Ese grafo no se puede hacer mi vale, te crees Teo y no llegas ni a Jarlan")

    
def get_fibonacci_sequence(update, context):
    parametros = ' '.join(context.args).strip().split(" ")

    try:                #Perform a check to see if parameters are valid
        parametros = [int(parametro) for parametro in parametros]
    except Exception:
        pass
        bot.send_message(chat_id = update.effective_chat.id, text = "Verifique sus parametros, estos deben ser números enteros separados por un espacio, ej: 1 3 4 5")
        return

    sequence = functions.fibonacci_sequence(sorted(parametros)) 
    
    if len(sequence) > 0:    #If we found a sequence make the bot return it as a message
        s = ""
        for number in sequence:
            s += str(number)+" "
        bot.send_message(chat_id = update.effective_chat.id, text = "La subsecuencia encontrada fue "+s)
    else:
        bot.send_message(chat_id = update.effective_chat.id, text = "No se encontró ninguna subsecuencia con la secuencia dada")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Add all the handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('grafo', get_graph))
    dispatcher.add_handler(CommandHandler('subsecuencia', get_fibonacci_sequence))

    dispatcher.add_handler(CommandHandler('help', helper))
    dispatcher.add_handler(CallbackQueryHandler(menu, pattern="op1"))
    dispatcher.add_handler(CallbackQueryHandler(menu, pattern="op2"))
    dispatcher.add_handler(CallbackQueryHandler(menu, pattern="op3"))
    dispatcher.add_handler(CallbackQueryHandler(menu, pattern="op4"))

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    print(bot.get_me())
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()