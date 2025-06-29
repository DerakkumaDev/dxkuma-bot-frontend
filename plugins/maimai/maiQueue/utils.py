import time
from typing import Any

from nonebot.adapters.onebot.v11 import Bot


async def gen_message(bot: Bot, arcade: dict[str, Any]) -> str:
    messages = list()
    messages.append(arcade["name"])
    if arcade["count"] > 0:
        messages.append(f"当前为{arcade["count"]}卡")
    else:
        messages.append(f"当前无人排卡")

    if arcade["last_action"] is not None:
        messages.append(
            f"最后在{time.strftime("%Y年%m月%d日 %H:%M", time.localtime(arcade["last_action"]["time"]))}（UTC+8）"
        )
        if arcade["last_action"]["group"] < 0 and arcade["last_action"]["operator"] < 0:
            messages.append("由迪拉熊")
        else:
            operator = await bot.get_stranger_info(
                user_id=arcade["last_action"]["operator"]
            )
            messages.append(
                f"由{arcade["last_action"]["group"]}——{operator["nickname"]}（{operator["qid"] or arcade["last_action"]["operator"]}）"
            )

        if "action" in arcade["last_action"]:
            messages.append(
                f"自{arcade["last_action"]["action"]["before"]}卡{action2str(arcade["last_action"]["action"]["type"])}{arcade["last_action"]["action"]["num"]}卡"
            )
        elif "before" in arcade["last_action"]:
            action, delta = num2action(arcade["count"], arcade["last_action"]["before"])
            messages.append(f"自{arcade["last_action"]["before"]}卡{action}{delta}卡")

    if arcade["action_times"] > 0:
        messages.append(f"今日（UTC+4）被更新{arcade["action_times"]}次")
    else:
        messages.append(f"今日（UTC+4）还没有被更新过")

    return "\r\n".join(messages)


def action2str(action: str) -> str | None:
    match action:
        case "add":
            return "增加"
        case "remove":
            return "减少"
        case "set":
            return "设置"

    return


def num2action(now: int, before: int) -> tuple[str | None, int | None]:
    if now > before:
        return "增加", now - before
    elif now < before:
        return "减少", before - now

    return None, None
