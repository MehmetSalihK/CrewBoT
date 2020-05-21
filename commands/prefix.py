import cfg
import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> `NEW PREFIX`"),
        ("Description:",
         "Change the default prefix for commands. The default is `vc/`.\n"
         "The prefix is **not** case sensitive, to cater to mobile users as well."
         "Be careful of setting the prefix to one that another bot is already using, "
         "both bots will likely respond to the same command.\n"
         "Mentioning me instead (i.e. using \"@\" + my name as the prefix) will always work."),
        ("Example:", "`<PREFIX><COMMAND> avc-` to make `avc-` the new command prefix."),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params)
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    new_prefix = utils.strip_quotes(params_str)
    if not new_prefix:
        return False, ("Vous devez définir un nouveau préfixe, par exemple `{}prefix avc-` à faire "
                       "`avc-` le nouveau préfixe.".format(ctx['print_prefix']))
    disallowed_characters = ['\n', '\t', '`']
    for c in disallowed_characters:
        if c in new_prefix:
            return False, "Votre préfixe ne peut pas contenir **de nouvelles lignes**, **des tabulations** ou**\`**."
    response = ("Terminé! Mon préfixe dans votre serveur est maintenant `{0}`. Essayez d'exécuter «{0}ping» pour le tester.\n"
                "N'oubliez pas, vous pouvez toujours me mentionner au lieu d'utiliser mon préfixe (par exemple: **{1} ping**)"
                ".".format(new_prefix, ctx['message'].guild.me.mention))
    if len(new_prefix) == 1:
        response += ("\n\n:information_source: Remarque: Si vous utilisez le **même préfixe qu'un autre bot**, "
                     "vous devez également exécuter `{}dcnf` pour éviter les messages d'erreur lors de l'utilisation des commandes de ce bot."
                     "".format(new_prefix))
    cfg.PREFIXES[guild.id] = new_prefix
    settings['prefix'] = new_prefix
    utils.set_serv_settings(guild, settings)
    await func.server_log(
        guild,
        "💬 {} (`{}`) définissez le préfixe du serveur sur `{}`".format(
            func.user_hash(author), author.id, new_prefix
        ), 1, settings)
    return True, response


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=True,
)
