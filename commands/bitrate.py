import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Utilisation:", "<PREFIX><COMMAND> `N/reset`"),
        ("Description:",
         "Définissez un débit binaire personnalisé pour tout le serveur (en kbps) qui sera utilisé pour tous les canaux que vous rejoindrez.\n"
         "Cela peut être utilisé soit pour améliorer la qualité audio (par exemple pour les chaînes musicales), "
         "ou pour réduire la bande passante utilisée pour ceux avec Internet limité / cher.\n\n"
         "Remarque: le débit binaire concerne l'ensemble du canal, pas seulement vous. S'il y a d'autres utilisateurs dans le canal qui "
         "ont défini des débits personnalisés, le débit moyen sera utilisé.\n\n"
         "Si personne dans le canal n'a défini un débit binaire personnalisé, le débit binaire du canal principal («Nouvelle session») "
         "sera utilisé.\n\n"
         "Utilisez `<PREFIX>channelinfo` pour vérifier le débit actuel de la chaîne dans laquelle vous vous trouvez."),
        ("Exemples:",
         "<PREFIX><COMMAND> 80\n"
         "<PREFIX><COMMAND> reset"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params)
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    bitrate = utils.strip_quotes(params_str)
    v = author.voice
    in_vc = v is not None and v.channel.id in func.get_secondaries(guild, settings)
    if bitrate.lower() == 'reset':
        try:
            del settings['custom_bitrates'][str(author.id)]
            utils.set_serv_settings(guild, settings)
        except KeyError:
            return False, "Vous n'avez pas défini de débit binaire personnalisé."
        if in_vc:
            await func.update_bitrate(v.channel, settings, reset=True)
        return True, "Votre bitrate personnalisé a été réinitialisé, le canal par défaut sera désormais utilisé pour vous."

    try:
        bitrate = float(bitrate)
    except ValueError:
        return False, "`{}` n'est pas un nombre.".format(bitrate)

    if bitrate < 8:
        return False, "Le débit doit être supérieur à 8."

    if bitrate * 1000 > guild.bitrate_limit:
        return False, "{} est supérieur au débit binaire maximal de ce serveur ({}).".format(
            bitrate, guild.bitrate_limit / 1000
        )

    if 'custom_bitrates' not in settings:
        settings['custom_bitrates'] = {}
    settings['custom_bitrates'][str(author.id)] = bitrate
    utils.set_serv_settings(guild, settings)

    if in_vc:
        await func.update_bitrate(v.channel, settings)

    await func.server_log(
        guild,
        "🎚 {} (`{}`) définissez leur débit personnalisé sur {}kbps".format(
            func.user_hash(author), author.id, bitrate
        ), 2, settings)
    return True, ("Terminé! Dorénavant, les canaux que vous rejoindrez verront leur débit réglé sur {} kbps.\n"
                  "Si plusieurs utilisateurs de la chaîne ont défini des débits binaires personnalisés, la moyenne sera utilisée.\n\n"
                  "Utilisez `{}channelinfo` pour vérifier le débit actuel de votre chaîne.".format(bitrate,
                                                                                             ctx['print_prefix']))


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    gold_required=True,
    admin_required=False,
)
