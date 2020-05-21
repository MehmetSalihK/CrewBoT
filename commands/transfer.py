import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> `@USER`"),
        ("Description:",
         "Transférer la propriété de votre chaîne à quelqu'un d'autre dans la chaîne, leur permettant d'utiliser des commandes qui "
         "exiger qu'ils soient le créateur (e.g. `private`, `limit`, `name`...)."),
        ("Exemples:",
         "```<PREFIX><COMMAND> @pixaal```"),
    ]
]


async def execute(ctx, params):
    name = ' '.join(params).strip()
    guild = ctx['guild']
    author = ctx['message'].author
    vc = ctx['voice_channel']

    user = utils.get_user_in_channel(name, vc)

    if not user:
        return False, "Impossible de trouver un utilisateur dans votre chaîne portant le nom\"{}\".".format(name)
    if user.id == ctx['creator_id']:
        if user == author:
            return False, "Tu es déjà le créateur."
        else:
            return False, "{} est déjà le créateur.".format(func.user_hash(user))

    result = await func.set_creator(guild, vc.id, user)
    return result, None


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
