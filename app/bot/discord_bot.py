from flask_discord_interactions import DiscordInteractionsBlueprint

discord_bot = DiscordInteractionsBlueprint()

@discord_bot.command()
def hello(ctx):
    return "Hello world!"