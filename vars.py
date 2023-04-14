from discord import ButtonStyle
from discord.app_commands import Choice
from discord.ui import Button, View

invite_button = Button(
    label="Invite",
    style=ButtonStyle.url,
    url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands",
)
support_button = Button(
    label="Discord Server", style=ButtonStyle.url, url="https://discord.gg/5Jn32Upk4M"
)
vote_button = Button(
    label="Vote",
    style=ButtonStyle.url,
    url="https://top.gg/bot/876097748255014932/vote",
)
github_button = Button(
    label="Github",
    style=ButtonStyle.url,
    url="https://github.com/Koalacards/Sus-O-Meter/",
)

url_row = View()
buttons = [invite_button, support_button, vote_button, github_button]

for button in buttons:
    url_row.add_item(button)

language_choices = [Choice(name="English", value=1), Choice(name="Español", value=2)]
opt_in_choices = [Choice(name="no", value=1), Choice(name="yes", value=2)]

list_choices = [
    Choice(name="Community", value=1),
    Choice(name="Custom", value=2),
]

SUGGESTION_CHANNEL = 928837547403149332
server_messages_to_search = 5000
