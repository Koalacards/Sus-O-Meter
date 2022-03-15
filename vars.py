from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.cog_ext import manage_commands


invite_button = create_button(label="Invite", style=ButtonStyle.URL, url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands")
support_button = create_button(label="Support", style=ButtonStyle.URL, url="https://discord.gg/5Jn32Upk4M")
vote_button = create_button(label="Vote", style=ButtonStyle.URL, url="https://top.gg/bot/876097748255014932/vote")
github_button = create_button(label="Github", style=ButtonStyle.URL, url="https://github.com/Koalacards/Sus-O-Meter/")

buttons = [invite_button, support_button, vote_button, github_button]

action_row = create_actionrow(*buttons)

#For testing with beta
guild_ids=[876103457407385661]

suggest_sus_word_options=[
    manage_commands.create_option(
        name="word",
        description="A word that should be considered sus (can't contain spaces)!",
        option_type=3,
        required=True
    )
]

language_options=[
    manage_commands.create_option(
        name="language",
        description="The language of the bot",
        option_type=3,
        required=True,
        choices=[
            "English",
            "Español"
        ]
    )
]

list_type_options=[
    manage_commands.create_option(
        name="list_type",
        description="The type of list the server will use (Community is a premade list, Custom is your own!)",
        option_type=3,
        required=True,
        choices=[
            "Community",
            "Custom"
        ]
    )
]

user_sus_words_options =[
    manage_commands.create_option(
        name="user",
        description="The user you want to get their sus information from",
        option_type=6,
        required=True,
    )
]

SUGGESTION_CHANNEL=928837547403149332
num_messages_to_search = 1000
kinda_sus_pictures=["https://i.etsystatic.com/26195327/r/il/b9103b/2797002083/il_fullxfull.2797002083_t400.jpg",
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
 "https://pbs.twimg.com/media/E2IGViFXMAAyldO.png"]
 