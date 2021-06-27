# from _typeshed import NoneType
# from commands import create
import re
from functions import create_temp_vc
from discord.user import User
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> [@MEMBERS]"),
        ("Description:",
         "Try to pull another member into a temporary channel"),
        ("Example:", 
        "```<PREFIX><COMMAND> @Stonic#7341```\nFor Multiple drags: ```<PREFIX><COMMAND> @Stonic#7341 @Zelda#4567```"),
    ]
]

async def execute(ctx, params):
    user: User = User
    guild = ctx['guild']
    client = ctx['client']
    author = ctx['message'].author
    users = params

    members = []

    for p in users:
        try:
            user = re.sub(r'[<>@!]', '', p)
            print(f"incoming: {p}, user: {user}")

            cm = await guild.fetch_member(user)
        except:
            return False, f"Member {p} wasn't found in this server."

        members.append(cm)

    vc = await create_temp_vc(client, guild, author, members)

    print(f"{vc}")

    if vc == None:
        return False, f"Unable to generate a voice channel."

    await author.send(f'The room is up join here: <#{vc.id}>!', delete_after=15.0)

    for member in members:
        print(f"fetched member: {member}")

        await member.send(f"<@!{author.id}> invites you to his private room, join <#{vc.id}>!", delete_after=15.0)

    return True, f"<@!{author.id}> The room is generated, tell your friend(s) to check their DMs!"

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False
)
