import os
import json
import datetime
import asyncio
import aiohttp
import logging
from astrbot.api.all import AstrMessageEvent, CommandResult, Context
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star

logger = logging.getLogger("astrbot")


@register("D-G-N-C-J", "Tinyxi", "", "", "")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.PLUGIN_NAME = "astrbot_plugin_essential"
        self.context = context

        if not os.path.exists(f"data/{self.PLUGIN_NAME}_data.json"):
            with open(f"data/{self.PLUGIN_NAME}_data.json", "w", encoding="utf-8") as f:
                f.write(json.dumps({}, ensure_ascii=False, indent=2))
        with open(f"data/{self.PLUGIN_NAME}_data.json", "r", encoding="utf-8") as f:
            self.data = json.loads(f.read())
        self.good_morning_data = self.data.get("good_morning", {})
        self.good_morning_cd = {}
        self.active_sessions = self.data.get("active_sessions", [])
        self.last_broadcast_date = self.data.get("last_broadcast_date", "")

        asyncio.create_task(self.daily_broadcast())

    def check_good_morning_cd(self, user_id: str, current_time: datetime.datetime) -> bool:
        if user_id not in self.good_morning_cd:
            return False
        
        last_time = self.good_morning_cd[user_id]
        time_diff = (current_time - last_time).total_seconds()
        return time_diff < 1800

    def update_good_morning_cd(self, user_id: str, current_time: datetime.datetime):
        self.good_morning_cd[user_id] = current_time

    def save_data(self):
        with open(f"data/{self.PLUGIN_NAME}_data.json", "w", encoding="utf-8") as f:
            self.data["good_morning"] = self.good_morning_data
            self.data["active_sessions"] = self.active_sessions
            self.data["last_broadcast_date"] = self.last_broadcast_date
            f.write(json.dumps(self.data, ensure_ascii=False, indent=2))

    async def daily_broadcast(self):
        while True:
            try:
                now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
                current_hour = now.hour
                current_date = now.strftime("%Y-%m-%d")

                if self.last_broadcast_date != current_date:
                    self.last_broadcast_date = current_date
                    self.save_data()

                messages = {
                    0: "晚上12点咯，还不睡吗",
                    6: "早上6点咯，有没有起床的",
                    8: "8点咯，起床吃早饭咯",
                    12: "中午了，该吃午饭了",
                    17: "下午好啊各位",
                    20: "晚上8点了，该准备睡觉咯",
                    22: "睡觉咯各位"
                }

                if current_hour in messages:
                    message = messages[current_hour]
                    for session_id in self.active_sessions:
                        try:
                            await self.context.send_message(session_id, message)
                        except Exception as e:
                            logger.error(f"发送定时播报失败: {e}")

                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"定时播报任务出错: {e}")
                await asyncio.sleep(60)

    @filter.regex(r"^(早安|晚安)")
    async def good_morning(self, message: AstrMessageEvent):
        umo_id = message.unified_msg_origin
        user_id = message.message_obj.sender.user_id
        user_name = message.message_obj.sender.nickname
        curr_utc8 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        curr_human = curr_utc8.strftime("%Y-%m-%d %H:%M:%S")

        if umo_id not in self.active_sessions:
            self.active_sessions.append(umo_id)
            self.save_data()

        if self.check_good_morning_cd(user_id, curr_utc8):
            return CommandResult().message("你刚刚已经说过早安/晚安了，请30分钟后再试喵~").use_t2i(False)

        is_night = "晚安" in message.message_str

        if umo_id in self.good_morning_data:
            umo = self.good_morning_data[umo_id]
        else:
            umo = {}
        if user_id in umo:
            user = umo[user_id]
        else:
            user = {
                "daily": {
                    "morning_time": "",
                    "night_time": "",
                }
            }

        if is_night:
            user["daily"]["night_time"] = curr_human
            user["daily"]["morning_time"] = ""
        else:
            user["daily"]["morning_time"] = curr_human

        umo[user_id] = user
        self.good_morning_data[umo_id] = umo

        with open(f"data/{self.PLUGIN_NAME}_data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.good_morning_data, ensure_ascii=False, indent=2))
            
        self.update_good_morning_cd(user_id, curr_utc8)

        curr_day: int = curr_utc8.day

        curr_day_sleeping = 0
        for v in umo.values():
            if v["daily"]["night_time"] and not v["daily"]["morning_time"]:
                user_day = datetime.datetime.strptime(
                    v["daily"]["night_time"], "%Y-%m-%d %H:%M:%S"
                ).day
                if user_day == curr_day:
                    curr_day_sleeping += 1

        if not is_night:
            sleep_duration_human = ""
            if user["daily"]["night_time"]:
                night_time = datetime.datetime.strptime(
                    user["daily"]["night_time"], "%Y-%m-%d %H:%M:%S"
                )
                morning_time = datetime.datetime.strptime(
                    user["daily"]["morning_time"], "%Y-%m-%d %H:%M:%S"
                )
                sleep_duration = (morning_time - night_time).total_seconds()
                hrs = int(sleep_duration / 3600)
                mins = int((sleep_duration % 3600) / 60)
                sleep_duration_human = f"{hrs}小时{mins}分"

            return (
                CommandResult()
                .message(
                    f"早上好喵，{user_name}！\n现在是 {curr_human}，昨晚你睡了 {sleep_duration_human}。"
                )
                .use_t2i(False)
            )
        else:
            return (
                CommandResult()
                .message(
                    f"快睡觉喵，{user_name}！\n现在是 {curr_human}，你是本群今天第 {curr_day_sleeping} 个睡觉的。"
                )
                .use_t2i(False)
            )

    @filter.command("王者战力")
    async def king_glory_power_query(self, message: AstrMessageEvent):
        hero_name = message.message_str.replace("王者战力", "").strip()
        
        if not hero_name:
            return CommandResult().message("正确查询示例：王者战力 孙悟空")
        
        api_url = "https://www.sapi.run/hero/select.php"
        params = {
            "hero": hero_name,
            "type": "aqq"
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error("查询失败，请稍后重试")
                    
                    data = await resp.json()
                    
                    if data.get("code") == 200 and "data" in data:
                        hero_data = data["data"]
                        
                        output = f"{hero_data.get('name', '')}\n"
                        output += f"国服最低：{hero_data.get('guobiao', '')}\n"
                        output += f"省标最低：{hero_data.get('provincePower', '')}\n"
                        output += f"市标最低：{hero_data.get('cityPower', '')}\n"
                        output += f"区标最低：{hero_data.get('areaPower', '')}"
                        
                        return CommandResult().message(output)
                    else:
                        return CommandResult().error(f"查询失败：{data.get('msg', '未知错误')}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到查询服务器，请稍后重试")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("查询超时，请稍后重试")
        except Exception as e:
            logger.error(f"查询王者战力时发生错误：{e}")
            return CommandResult().error(f"查询失败：{str(e)}")
