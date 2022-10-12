from discord import ButtonStyle
from discord.app_commands import Choice
from discord.ui import Button, View

invite_button = Button(
    label="Invite",
    style=ButtonStyle.url,
    url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands",
)
support_button = Button(
    label="Support", style=ButtonStyle.url, url="https://discord.gg/5Jn32Upk4M"
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
kinda_sus_pictures = [
    "https://i.etsystatic.com/26195327/r/il/b9103b/2797002083/il_fullxfull.2797002083_t400.jpg",
    "https://imgix.bustle.com/uploads/image/2020/10/31/31aa14f0-bc99-4e6b-b785-26ae420971dd-screen-shot-2020-10-31-at-52151-pm.png?w=1200&h=630&fit=crop&crop=faces&fm=jpg",
    "https://image-cdn.neatoshop.com/styleimg/113537/none/black/default/477968-20;1605375643x.jpg",
    "https://ih1.redbubble.net/image.1042054698.6192/st,small,507x507-pad,600x600,f8f8f8.jpg",
    "https://cdn.shopify.com/s/files/1/0324/7941/2283/products/LookinKindaSus1_740x.jpg?v=1607627480",
    "http://www.rogueduck.art/uploads/1/2/4/7/124740057/s829560345432686266_p124_i1_w450.png",
    "https://imageproxy.ifunny.co/crop:x-20,resize:640x,quality:90x75/images/109afed84e8549231a40801bc7071ba2e2eaffb52863c22cafd6d5c631839d10_1.jpg",
    "https://i1.sndcdn.com/artworks-BZOdK0DGnlFHa23y-jG4Vcw-t500x500.jpg",
    "https://i.etsystatic.com/25325402/r/il/39e5de/2600613663/il_570xN.2600613663_mmum.jpg",
    "https://res.cloudinary.com/teepublic/image/private/s--g97Q4qXJ--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_000000,e_outline:35/co_000000,e_outline:inner_fill:35/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1601510568/production/designs/14563420_0.jpg"
    "https://i.imgflip.com/4kg413.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsKHUFDoYcyODaSg9NOS_gbHrUvx428plJ0w&usqp=CAU",
    "https://res.cloudinary.com/teepublic/image/private/s--WaNQLAIU--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1606090299/production/designs/9596239_1.jpg",
    "https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/among-us-being-very-sus-trung-dinh-art.jpg",
    "https://pbs.twimg.com/media/E2IGViFXMAAyldO.png",
]
