from telegram import *
from telegram.ext import *
from config import TOKEN
import logging
import graph
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


def grito(update, context):
    bot.send_message(
        chat_id = update.effective_chat.id,
        text = "El éxito ocurre cuando tus sueños son más grandes que tus excusas, si quieres estar feliz recuerda decir SIUUUUUUUUUUUUUUUUUUUUUU"
    )


def get_graph(update, context):
    params = ' '.join(context.args).split(" ")
    print(params)
    G = graph.generateGraph(int(params[0]), int(params[1]), int(params[2]))
    if G != None:
        nx.draw(G)
        plt.savefig("graph.png")
        bot.send_photo(chat_id=update.effective_chat.id, photo=open("graph.png", 'rb'), caption="Grafo Hecho por el Bichou SIUUUUUUUU")
    else:
        bot.send_message(chat_id = update.effective_chat.id, text = "Ese grafo no se puede hacer mi vale, te crees Teo y no llegas ni a Jarlan")
    


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('bichotriste', grito))
    dispatcher.add_handler(CommandHandler('balondeoro', balon_de_oro))
    dispatcher.add_handler(CommandHandler('grafo', get_graph))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    print(bot.get_me())
    updater.start_polling()
    

if __name__ == '__main__':
    main()