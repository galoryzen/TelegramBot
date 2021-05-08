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


def balon_de_oro(update, context):
    bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Porque soy hermoso, y salto más que Messi, aparezco en los momentos importantes como contra el cagliari, y no en partiditos como el del lyon que no tienen relevancia"
    )


def bicho_triste(update, context):
    bot.send_message(
        chat_id = update.effective_chat.id,
        text = "El éxito ocurre cuando tus sueños son más grandes que tus excusas, si quieres estar feliz recuerda decir SIUUUUUUUUUUUUUUUUUUUUUU"
    )


def get_graph(update, context):
    parametros = ' '.join(context.args).strip().split(" ")
    try:
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

    try:
        parametros = [int(parametro) for parametro in parametros]
    except Exception:
        pass
        bot.send_message(chat_id = update.effective_chat.id, text = "Verifique sus parametros, estos deben ser números enteros separados por un espacio, ej: 1 3 4 5")
        return

    arr = functions.fibonacci_sequence(sorted(parametros))
    
    if len(arr) > 0:
        s = ""
        for number in arr:
            s += str(number)+" "
        bot.send_message(chat_id = update.effective_chat.id, text = "La subsecuencia encontrada fue "+s)
    else:
        bot.send_message(chat_id = update.effective_chat.id, text = "No se encontró ninguna subsecuencia con la secuencia dada")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('bichotriste', bicho_triste))
    dispatcher.add_handler(CommandHandler('balondeoro', balon_de_oro))
    dispatcher.add_handler(CommandHandler('grafo', get_graph))
    dispatcher.add_handler(CommandHandler('subsecuencia', get_fibonacci_sequence))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    print(bot.get_me())
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()