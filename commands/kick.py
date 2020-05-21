import cfg
import discord
import utils
import functions as func
from math import floor
from commands.base import Cmd
from time import time

help_text = [
    [
        ("Usage:",
         "```<PREFIX><COMMAND> @USER```"
         "```<PREFIX><COMMAND> @USER\nREASON```"),
        ("Description:",
         "Lancer un vote pour supprimer un utilisateur de votre chaîne et l'empêcher de se joindre à nouveau. "
         "**Plus de la moitié** des utilisateurs restants doivent voter oui pour que le membre soit exclu.\n\n"
         "Si vous souhaitez permettre à un utilisateur expulsé de revenir sur la chaîne, vous devrez tous quitter et créer un nouveau "
         "à la place, ou si vous êtes administrateur de serveur, modifiez manuellement les autorisations de canal.\n\n"
         "La personne qui a initialement créé la chaîne ne peut pas être expulsée (sauf si elle quitte volontairement et plus tard "
         "retour, auquel cas le \"créateur\" de la chaîne est réaffecté à la personne qui se trouvait en haut de la "
         "chaîne lors de son départ.)"),
        ("Exemples:",
         "```<PREFIX><COMMAND> @pixaal```"
         "```<PREFIX><COMMAND> pixaal#1234\nÊtre méchant :(```"
         "```<PREFIX><COMMAND> pixaal\nAbus de Soundboard```"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params).strip()
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    vc = ctx['voice_channel']
    parts = params_str.split('\n', 1)
    name = parts[0]
    reason = parts[1] if len(parts) > 1 else None

    user = utils.get_user_in_channel(name, vc)

    if not user:
        return False, "Impossible de trouver un utilisateur dans votre chaîne avec le nom \"{}\".".format(name)
    if user.id == utils.get_creator_id(settings, vc):
        return False, "Vous ne pouvez pas kick le créateur de cette chaîne."
    if user == author:
        return False, "S'il vous plaît ne vous donnez pas un coup de pied :frowning:"

    participants = [m for m in vc.members if m not in [author, user] and not m.bot]
    required_votes = floor((len(participants) + 1) / 2) + 1
    try:
        text = (
            "‼ **Votekick** ‼\n"
            "{initiator} a lancé un vote contre {offender}.{reason}\n\n"
            "{participants}:\nVotez en réagissant avec ✅ pour donner un coup de pied {offender}, "
            "ou ignorer ce message pour voter **Non**.\n\n"
            "Vous avez **2 minutes** pour voter. Un vote majoritaire ({req}/{tot}) est requis.\n"
            "{initiator} votre vote est automatiquement compté. Les votes des utilisateurs n'appartenant pas à votre chaîne seront ignorés."
            "".format(
                initiator=author.mention,
                offender=user.mention,
                reason=(" Raison: **{}**".format(reason) if reason else ""),
                participants=' '.join([m.mention for m in participants]),
                req=required_votes,
                tot=len(participants) + 1
            )
        )
        if not participants:
            text = "..."
        m = await ctx['message'].channel.send(text)
    except discord.errors.Forbidden:
        return False, "Je n'ai pas la permission de répondre à votre commande kick."
    cfg.VOTEKICKS[m.id] = {
        "initiator": author,
        "participants": participants,
        "required_votes": required_votes,
        "offender": user,
        "reason": reason,
        "in_favor": [author],
        "voice_channel": vc,
        "message": m,
        "end_time": time() + 120
    }
    try:
        if participants:
            await m.add_reaction('✅')
    except discord.errors.Forbidden:
        pass
    await func.server_log(
        guild,
        "👢 {} (`{}`) lancé un vote contre **{}** (`{}`) in \"**{}**\". Raison: *{}*.".format(
            func.user_hash(author), author.id, func.user_hash(user), user.id, vc.name, reason
        ), 1, settings)
    return True, "NO RESPONSE"


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False,
    voice_required=True,
)
