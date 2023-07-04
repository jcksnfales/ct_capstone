from flask_discord_interactions import DiscordInteractionsBlueprint
from models import db, User, LinkListing, link_schema, links_schema

discord_bot = DiscordInteractionsBlueprint()

@discord_bot.command()
def hello(ctx):
    "Simple hello world test command"
    return "Hello world!"

@discord_bot.command()
def share_link(ctx, value: str):
    "Returns a given link's information"
    return f"{value}"

@discord_bot.autocomplete()
def autocomplete(ctx, value=None):
    queried_links = LinkListing.query.filter_by(is_public=True).all()
    return queried_links