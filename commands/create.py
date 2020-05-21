import discord
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND>"),
        ("Description:",
         "Créez un nouveau canal vocal principal. Lorsque les utilisateurs rejoignent cette chaîne, j'en crée une nouvelle et je les déplace "
         "dans ça. Par défaut, les canaux principaux sont nommés \"+\" et placés en haut de votre serveur, mais "
         "vous pouvez le renommer en toute sécurité, le déplacer et modifier ses autorisations.\n\n"
         "Vous pouvez créer autant de canaux principaux que vous le souhaitez et les placer dans différentes zones de votre serveur. "
         "Ils (et les canaux secondaires que je crée pour eux) hériteront des autorisations de la catégorie dans laquelle ils se trouvent "
         "par défaut.\n\n"
         "Si vous déplacez une chaîne principale dans une catégorie privée/restreinte, **assurez-vous que j'ai la permission de créer "
         "et y éditer des canaux vocaux**.\n\n"
         "Les canaux secondaires copieront les périmètres, le débit binaire et la limite d'utilisateur de leur canal principal.\n\n"
         "Par défaut, les canaux secondaires seront placés au-dessus de leur canal principal. Utilisation *<PREFIX>toggleposition* to "
         "placez-les ci-dessous à la place."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    default_name = "➕"

    try:
        await func.create_primary(guild, default_name, ctx['message'].author)
    except discord.errors.Forbidden:
        return False, "Je n'ai pas l'autorisation de créer des chaînes."
    except discord.errors.HTTPException as e:
        return False, "An HTTPException occurred: {}".format(e.text)

    response = ("Un nouveau canal vocal appelé \"{}\" a été créé. "
                "Vous pouvez maintenant le déplacer, le renommer, etc.\n\n"
                "Chaque fois qu'un utilisateur entre dans ce canal vocal, un nouveau canal vocal est créé au-dessus "
                "pour eux, et ils y seront automatiquement déplacés.\n"
                "Lorsque cette chaîne est vide, elle sera supprimée automatiquement.\n\n"
                "Utilisation `{}template` changer le schéma de nommage des nouveaux canaux".format(default_name,
                                                                                           ctx['print_prefix']))
    return True, response


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=True,
)
