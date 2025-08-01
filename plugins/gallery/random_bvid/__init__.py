import datetime
import re

import orjson as json
from aiohttp import ClientSession
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

from util.Config import config
from .database import bvidList
from ..rank.database import ranking

rand_bv = on_regex(r"^(随机)?(迪拉熊|dlx)(视频|sp|v)$", re.I)
add_bv = on_regex(r"^(加视频|jsp)(\s*BV[A-Za-z0-9]{10})+$", re.I)
remove_bv = on_regex(r"^(删视频|jsp)(\s*BV[A-Za-z0-9]{10})+$", re.I)

LIMIT_MINUTES = 1
LIMIT_TIMES = 5

groups: dict[int, list[datetime.datetime]] = dict()


@rand_bv.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    qq = event.get_user_id()
    groups.setdefault(group_id, list())
    now = datetime.datetime.fromtimestamp(event.time)
    if group_id != config.special_group:  # 不被限制的 group_id
        while len(groups[group_id]) > 0:
            t = groups[group_id][0]
            if now - t < datetime.timedelta(minutes=LIMIT_MINUTES):
                break
            groups[group_id].pop(0)

        if len(groups[group_id]) >= LIMIT_TIMES:
            msg = MessageSegment.text(
                "迪拉熊提醒你：注意不要过度刷屏，给其他人带来困扰哦，再试一下吧~"
            )
            await rand_bv.finish(msg)

    while True:
        bvid = bvidList.random_bvid
        headers = {"User-Agent": f"kumabot/{config.version[0]}.{config.version[1]}"}
        async with ClientSession(conn_timeout=3, headers=headers) as session:
            async with session.get(
                "https://api.bilibili.com/x/web-interface/wbi/view",
                params={"bvid": bvid},
            ) as resp:
                video_info = await resp.json(loads=json.loads)
        if video_info["code"] != 0:
            bvidList.remove(bvid)
            continue

        break

    mini_app_ark = await bot.call_api(
        api="get_mini_app_ark",
        type="bili",
        title=video_info["data"]["title"],
        desc=video_info["data"]["desc"],
        picUrl=video_info["data"]["pic"],
        jumpUrl=f"pages/video/video?bvid={bvid}",
        webUrl=f"https://www.bilibili.com/video/{bvid}/",
    )
    await rand_bv.send(MessageSegment.json(json.dumps(mini_app_ark["data"]).decode()))
    groups[group_id].append(now)
    ranking.update_count(qq=qq, type="video")


@add_bv.handle()
async def _(event: GroupMessageEvent):
    if event.user_id not in config.admin_accounts:
        return

    msg = event.get_plaintext()
    bvids = re.findall(r"BV[A-Za-z0-9]{10}", msg)
    for bvid in bvids:
        bvidList.add(bvid)
    await add_bv.finish(MessageSegment.text("已添加"))


@remove_bv.handle()
async def _(event: GroupMessageEvent):
    if event.user_id not in config.admin_accounts:
        return

    msg = event.get_plaintext()
    bvids = re.findall(r"BV[A-Za-z0-9]{10}", msg)
    for bvid in bvids:
        bvidList.remove(bvid)
    await remove_bv.finish(MessageSegment.text("已删除"))
