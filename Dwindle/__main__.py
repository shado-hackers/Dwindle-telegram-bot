import logging
import requests
from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler, Filters, CallbackQueryHandler
import emoji
import telegram
from Dwindle import TOKEN, modules, LOGGER, PORT, WEBHOOK , URL
from Dwindle.modules import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        "<b>Hi {} {} ! \n\nI'm <a href=\"tg://user?id=828959161\">TINY link</a> - A Simple URL shortener bot."
        "\n\nSend me any link , I can short it for You."
        "\n\nHit </b>/help<b> to find out more about how to use me.</b>".format(update.effective_user.first_name, (
            emoji.emojize(":wave:", use_aliases=True))), parse_mode='html',
        reply_to_message_id=update.message.message_id)


def help(update, context):
    update.message.reply_text("*Hey! My name is TINY link.* "
                              "\n\nI am a link shortener bot, here to help you to shorten your links!"
                              "\nI have lots of handy features to help You"
                              "\n\n*Helpful commands:*"
                              "\n\t\t- /start: Starts me! You've probably already used this."
                              "\n\t\t- /help: Sends this message; I'll tell you more about myself!"
                              "\n - /short <platform> <url> : Shortens the given URL"
                              "\n     *Ex:* `/short bitly https://t.me/OMG_info/`"
                              "\n  - /unshort <url> : Unshorts the given URL"
                              "\n  - /about : About the bot"
                              "\n\t\t- /support: Gives you info on how to support me and my creator.",
                              parse_mode=telegram.ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


def aboutTheBot(update, context):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            telegram.InlineKeyboardButton((emoji.emojize(":loop:", use_aliases=True)) + "Channel",
                                          url="t.me/OMG_info"),
            telegram.InlineKeyboardButton("👥Support Group", callback_data='2'),
        ],
        [telegram.InlineKeyboardButton((emoji.emojize(":bookmark:", use_aliases=True)) + "Add Me In Group",
                                       url="https://t.me/dwindle_Bot?startgroup=new")],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text("<b>Hey! My name is TINY link.</b>"
                              "\nI can handle links in different ways."
                              "\n\n<b>About Me :</b>"
                              "\n\n  - <b>Name</b>        : TINY link"
                              "\n\n  - <b>Creator</b>      : @shado_hackers"
                              "\n\n  - <b>Language</b>  : Python 3"
                              "\n\n  - <b>support</b>       : <a href=\"https://t.me/OMG_info/\">OMG_info</a>"
                              "\n\n  - <b>Follow</b>  : <a href=\"https://mobile.twitter.com/Lusifer_noob/\">Twitter</a>"
                              "\n\nIf you enjoy using me and want to help me survive, do donate with the /donate command - my creator will be very grateful! Doesn't have to be much - every little helps! Thanks for reading :)",
                              parse_mode='html', reply_markup=reply_markup, disable_web_page_preview=True)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == 2:
        print(query.data)
    query.edit_message_text(text="Support Group arrives Soon")

def support(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton("creator",
                                          url="https://t.me/shado_hackers"),
            telegram.InlineKeyboardButton("support",url="https://t.me/OMG_info"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive." , reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("short", short.short))
    dispatcher.add_handler(CommandHandler("unshort", unshort.unshort))
    dispatcher.add_handler(CommandHandler("screen", screen.screen))
    dispatcher.add_handler(CommandHandler("about", aboutTheBot))
    dispatcher.add_handler(CommandHandler("support", support))
    dispatcher.add_error_handler(error)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()

if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
