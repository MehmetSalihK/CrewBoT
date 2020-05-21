import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Utilisation:", "<PREFIX><COMMAND> `NOUVEAU NOM`"),
        ("Description:",
         "Changez directement le nom de la chaîne dans laquelle vous vous trouvez. "
         "Prend en charge toutes les variables de la`template` commande (utilisez `<PREFIX>help template` pour obtenir une liste).\n\n"
         "utilisez `<PREFIX><COMMAND> reset` pour supprimer votre remplacement de nom et revenir au modèle d'origine."),
        ("Examples:",
         "<PREFIX><COMMAND> Le barbecue animé de Bob\n"
         "<PREFIX><COMMAND> Karen aime @@game_name@@\n"
         "<PREFIX><COMMAND> reset"),
    ]
]


async def execute(ctx, params):
    params_str = ctx['clean_paramstr']
    guild = ctx['guild']
    author = ctx['message'].author

    new_name = params_str.replace('\n', ' ')  # Can't have newlines in channel name.
    new_name = new_name.strip()
    if new_name:
        return await func.custom_name(guild, ctx['voice_channel'], author, new_name)
    else:
        return False, ("Vous devez spécifier un nouveau nom pour cette chaîne, e.g. '{0}nom <nouveau nom>'.\n"
                       "Exécutez '{0}help template' pour une liste complète des variables que vous pouvez utiliser comme "
                       "`@@game_name@@`, `@@creator@@` et `@@num_others@@`.".format(ctx['print_prefix']))


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    gold_required=True,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
