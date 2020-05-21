import cfg
import discord
import utils
import functions as func
from commands.base import Cmd
from time import time

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND>"),
        ("Description:",
         "Rendez votre chaîne vocale privée, empêchant quiconque de vous rejoindre directement.\n\n"
         "Crée un canal \"⇩ Rejoignez (username)\" au-dessus du vôtre afin que les gens puissent demander à vous rejoindre "
         "Lorsque quelqu'un rejoint cette chaîne, je vous envoie un message vous demandant de"
         "accepter/refuser/bloquer leur demande."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    vc = ctx['voice_channel']

    for p, pv in settings['auto_channels'].items():
        for s, sv in pv['secondaries'].items():
            if s == vc.id:
                if 'priv' in sv and sv['priv']:
                    return False, ("Votre chaîne est déjà privée."
                                   "Utilisez `{}public` pour le rendre à nouveau public.".format(ctx['print_prefix']))
                try:
                    await vc.set_permissions(author, connect=True)
                    await vc.set_permissions(guild.default_role, connect=False)
                except discord.errors.Forbidden:
                    return False, ("I don't have permission to do that."
                                   "Please make sure I have the *Manage Roles* permission in this server and category.")
                settings['auto_channels'][p]['secondaries'][s]['priv'] = True
                settings['auto_channels'][p]['secondaries'][s]['msgs'] = ctx['channel'].id
                utils.set_serv_settings(guild, settings)
                cfg.PRIV_CHANNELS[s] = {
                    'creator': author,
                    'voice_channel': vc,
                    'primary_id': p,
                    'text_channel': ctx['channel'],
                    'guild_id': guild.id,
                    'request_time': time(),
                    'prefix': ctx['print_prefix'],
                }
                return True, ("Votre canal est désormais privée!\n"
                              "Un canal \"**⇩ Rejoignez {}**\" chaîne apparaîtra au-dessus de votre chaîne sous peu. "
                              "Lorsque quelqu'un entre sur ce canal pour demander à vous rejoindre, "
                              "Je vais envoyer un message ici vous demandant d'approuver ou de refuser leur demande.\n"
                              "Utilisez `{}public` pour le rendre à nouveau public."
                              "".format(func.esc_md(author.display_name), ctx['print_prefix']))
    return False, "It doesn't seem like you're in a voice channel anymore."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
