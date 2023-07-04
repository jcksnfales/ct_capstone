from flask_discord_interactions import DiscordInteractionsBlueprint
from models import db, User, LinkListing, link_schema, links_schema

discord_bot = DiscordInteractionsBlueprint()

@discord_bot.command("hello")
def hello(ctx):
    "Simple hello world test command"
    return "Hello world!"

@discord_bot.command("share_user_links")
def share_user_links(ctx, user_id: str):
    "Returns a given link's information"
    return LinkListing.query.filter(user_id=user_id).all()

@share_user_links.autocomplete()
def autocomplete(ctx, user_id=None):
    queried = User.query.filter(User.public_link_count > 0).all()
    return queried