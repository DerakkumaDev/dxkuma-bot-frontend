from nonebot import on_fullmatch, get_bot
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.internal.driver import Driver

from util.Config import config
from util.exceptions import NotAllowedException

ping = on_fullmatch("ping", ignorecase=True)


@ping.handle()
async def _(event: GroupMessageEvent):
    if event.user_id not in config.admin_accounts:
        return

    msg = event.get_plaintext()
    msg = msg.replace("i", "o")
    msg = msg.replace("I", "O")
    await ping.send(msg)
    raise NotAllowedException


@Driver.on_bot_disconnect
async def _(bot: Bot):
    try:
        sender = get_bot()
    except Exception:
        return
    await sender.send_group_msg(
        group_id=config.dev_group, message=f"{bot.self_id} is DOWN"
    )
