import os
from dotenv import load_dotenv
from Dandy import Dandy_bot


def main():
    load_dotenv()
    token = os.getenv('Token')
    bot = Dandy_bot(token)
    bot.awaken()


if __name__ == "__main__":
    main()
