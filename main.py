import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


def wait(chat_id, question, bot):
    message_id = bot.send_message(chat_id, "запускаю таймер...")
    bot.create_countdown(parse(question), notify_progress, author_id=chat_id, message_id=message_id, question=question, bot=bot)
    bot.create_timer(parse(question), choose, author_id=chat_id, bot=bot)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)   


def notify_progress(secs_left, author_id, message_id, question, bot):
    bot.update_message(author_id, message_id, f"Осталось секунд: {secs_left}\n{render_progressbar(parse(question),secs_left)}")
    

def choose(author_id, bot):
    bot.send_message(author_id, "время вышло!")


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()