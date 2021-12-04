from src.settings import MCDCSettings
from src.bot import MCDCBot

def main():
    settings = MCDCSettings()
    settings.stream_music = True

    bot = MCDCBot(settings)
    bot.run('TOKEN')

if __name__ == "__main__":
    main()