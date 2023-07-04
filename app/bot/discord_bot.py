from flask_discord_interactions import DiscordInteractionsBlueprint, Message, ActionRow, Button, ButtonStyles
from models import db, User, LinkListing, link_schema, links_schema

discord_bot = DiscordInteractionsBlueprint()

# @discord_bot.command("hello")
# def hello(ctx):
#     "Simple hello world test command"
#     return "Hello world!"

@discord_bot.command("link_share")
def link_share(ctx, listing_id: str):
    "Shows a given listing by ID."
    listing = LinkListing.query.get(listing_id)
    user = User.query.get(listing.listing_id)
    return Message(
        content=f"**{listing.link_title}** - {listing.description}",
        components=[
            ActionRow(components=[
                Button(
                    style=ButtonStyles.LINK,
                    url=listing.listed_link,
                    label="Go to link"
                )
            ])
        ]
    )
@link_share.autocomplete()
def autocomplete(ctx, link_id=None):
    "The ID of the link listing being queried."
    queried = LinkListing.query.filter_by(is_public=True).all()
    return queried

@discord_bot.command("links_share_user")
def links_share_user(ctx, user_id: str):
    "Shows a given user's publicly listed links"
    listings = LinkListing.query.filter_by(user_id=user_id, is_public=True).all()
    user = User.query.get(user_id)
    links_component = []
    for listing in listings:
        links_component += [
            ActionRow(components=[
                Button(
                    style=ButtonStyles.LINK,
                    url=listing.listed_link,
                    label=listing.link_title
                )
            ])
        ]
    return Message(
        content=f"Links from **{user.email}**",
        components=links_component
    )
@links_share_user.autocomplete()
def autocomplete(ctx, user_id=None):
    "The ID of the user whose links are being queried. Can be found at the end of their user page URL."
    queried = User.query.filter(User.public_link_count > 0).all()
    return queried

@discord_bot.command("links_share_all")
def links_share_all(ctx):
    "Shows all publicly listed links."
    listings = LinkListing.query.filter_by(is_public=True).all()
    links_component = []
    for listing in listings:
        links_component += [
            ActionRow(components=[
                Button(
                    style=ButtonStyles.LINK,
                    url=listing.listed_link,
                    label=listing.link_title
                )
            ])
        ]
    return Message(
        content=f"All public links",
        components=links_component
    )