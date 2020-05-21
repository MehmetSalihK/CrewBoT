import cfg
import discord
from functions import dm_user
from utils import log
from commands.base import Cmd

help_text = [
    [
        ("Utilisation:", "<PREFIX><COMMAND>"),
        ("Description:",
         "Obtenir mon lien d'invitation pour m'inviter sur un autre serveur."),
    ]
]


async def execute(ctx, params):
    channel = ctx['channel']
    t = "📫 invitez-moi sur un autre serveur!"
    bot_id = ctx['client'].user.id
    if cfg.SAPPHIRE_ID is not None:
        bot_id = 712927126835298314
    beta_id = 675405085752164372
    invite_id = bot_id if bot_id != beta_id else beta_id
    l = cfg.INVITE_LINK.replace('@@CID@@', str(invite_id))
    can_embed = channel.permissions_for(ctx['guild'].me).embed_links
    if can_embed:
        try:
            await channel.send(embed=discord.Embed(
                description="**[{}]({})**".format(t, l)
            ))
        except discord.errors.Forbidden:
            log("Interdit de faire écho", channel.guild)
            await dm_user(
                ctx['message'].author,
                "Je n'ai pas l'autorisation d'envoyer des messages dans le "
                "`#{}` canal de **{}**.".format(channel.name, channel.guild.name)
            )
            return False, "NO RESPONSE"
        return True, "NO RESPONSE"
    else:
        return True, ("{}\n<{}>".format(t, l))

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
)
