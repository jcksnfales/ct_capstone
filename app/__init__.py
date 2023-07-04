from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .bot.discord_bot import discord_bot

from flask_discord_interactions import DiscordInteractions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder


app = Flask(__name__)
discord = DiscordInteractions(app)
CORS(app)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

@discord.command()
def ping(ctx):
    return "Pong!"

discord.register_blueprint(discord_bot)
discord.set_route('/interactions')
discord.update_commands(guild_id="393453955276865546")

app.json_encoder = JSONEncoder
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

