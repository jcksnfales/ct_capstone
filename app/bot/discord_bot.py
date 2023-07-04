from flask_discord_interactions import DiscordInteractionsBlueprint, Message, ActionRow, Button, ButtonStyles
from models import db, User, LinkListing, link_schema, links_schema

discord_bot = DiscordInteractionsBlueprint()

@discord_bot.command("hello")
def hello(ctx):
    "Simple hello world test command"
    return "Hello world!"

@discord_bot.command("share_user_links")
def share_user_links(ctx, user_id: str):
    "Returns a given link's information"
    listings = LinkListing.query.filter_by(user_id=user_id).all()
    links_component = []
    for listing in listings:
        links_component += [
            ActionRow(
                content=listing.link_title,
                components=[
                    Button(
                        style=ButtonStyles.LINK,
                        url=listing.listed_link,
                        label="Go to link"
                    )
                ]
            )
        ]
    return Message(
        content=f"Links from **{user_id.email}**",
        components=links_component
    )

@share_user_links.autocomplete()
def autocomplete(ctx, user_id=None):
    queried = User.query.filter(User.public_link_count > 0).all()
    return queried