import asyncio
import os
import json
import datetime
import logging
import aiohttp
import urllib.parse
from astrbot.api.all import AstrMessageEvent, CommandResult, Context, Plain
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star

logger = logging.getLogger("astrbot")


@register("D-G-N-C-J", "Tinyxi", "早晚安记录+王者战力查询+腾讯元宝+DeepSeek-3.2+DeepSeek-3.1+GPT5-nano+Claude4.5-hiku+Qwen3-coder+DeepSeek-R1+智谱GLM4.6", "1.0.0", "")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.PLUGIN_NAME = "astrbot_plugin_essential"
        PLUGIN_NAME = self.PLUGIN_NAME

        if not os.path.exists(f"data/{PLUGIN_NAME}_data.json"):
            with open(f"data/{PLUGIN_NAME}_data.json", "w", encoding="utf-8") as f:
                f.write(json.dumps({}, ensure_ascii=False, indent=2))
        with open(f"data/{PLUGIN_NAME}_data.json", "r", encoding="utf-8") as f:
            self.data = json.loads(f.read())
        self.good_morning_data = self.data.get("good_morning", {})

        self.daily_sleep_cache = {}
        self.good_morning_cd = {} 

    def get_cached_sleep_count(self, umo_id: str, date_str: str) -> int:
        """获取缓存的睡觉人数"""
        if umo_id not in self.daily_sleep_cache:
            self.daily_sleep_cache[umo_id] = {}
        return self.daily_sleep_cache[umo_id].get(date_str, -1)

    def update_sleep_cache(self, umo_id: str, date_str: str, count: int):
        """更新睡觉人数缓存"""
        if umo_id not in self.daily_sleep_cache:
            self.daily_sleep_cache[umo_id] = {}
        self.daily_sleep_cache[umo_id][date_str] = count

    def invalidate_sleep_cache(self, umo_id: str, date_str: str):
        """使缓存失效"""
        if umo_id in self.daily_sleep_cache and date_str in self.daily_sleep_cache[umo_id]:
            del self.daily_sleep_cache[umo_id][date_str]

    def check_good_morning_cd(self, user_id: str, current_time: datetime.datetime) -> bool:
        """检查用户是否在CD中，返回True表示在CD中"""
        if user_id not in self.good_morning_cd:
            return False
        
        last_time = self.good_morning_cd[user_id]
        time_diff = (current_time - last_time).total_seconds()
        return time_diff < 1800

    def update_good_morning_cd(self, user_id: str, current_time: datetime.datetime):
        """更新用户的CD时间"""
        self.good_morning_cd[user_id] = current_time

    @filter.regex(r"^(早安|晚安)")
    async def good_morning(self, message: AstrMessageEvent):
        """和Bot说早晚安，记录睡眠时间，培养良好作息"""
        umo_id = message.unified_msg_origin
        user_id = message.message_obj.sender.user_id
        user_name = message.message_obj.sender.nickname
        curr_utc8 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        curr_human = curr_utc8.strftime("%Y-%m-%d %H:%M:%S")

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
        curr_date_str = curr_utc8.strftime("%Y-%m-%d")

        self.invalidate_sleep_cache(umo_id, curr_date_str)
        curr_day_sleeping = 0
        for v in umo.values():
            if v["daily"]["night_time"] and not v["daily"]["morning_time"]:
                user_day = datetime.datetime.strptime(
                    v["daily"]["night_time"], "%Y-%m-%d %H:%M:%S"
                ).day
                if user_day == curr_day:
                    curr_day_sleeping += 1
        
        self.update_sleep_cache(umo_id, curr_date_str, curr_day_sleeping)

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

    @filter.command("腾讯元宝")
    async def tencent_yuanbao(self, message: AstrMessageEvent):
        """腾讯元宝助手，支持异步请求"""
        msg = message.message_str.replace("腾讯元宝", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：腾讯元宝 <提问内容>\n\n示例：腾讯元宝 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/yuanbao.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error("请求腾讯元宝助手失败，服务器返回错误状态码")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到腾讯元宝助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求腾讯元宝助手时发生错误：{e}")
            return CommandResult().error(f"请求腾讯元宝助手时发生错误：{str(e)}")

    @filter.command("deep3.2")
    async def deepseek_32(self, message: AstrMessageEvent):
        """DeepSeek-3.2助手，支持异步请求"""
        msg = message.message_str.replace("deep3.2", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：deep3.2 <提问内容>\n\n示例：deep3.2 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/depsek3.2.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error("请求DeepSeek-3.2助手失败，服务器返回错误状态码")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到DeepSeek-3.2助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求DeepSeek-3.2助手时发生错误：{e}")
            return CommandResult().error(f"请求DeepSeek-3.2助手时发生错误：{str(e)}")

    @filter.command("deep3.1")
    async def deepseek_31(self, message: AstrMessageEvent):
        """DeepSeek-3.1助手，支持异步请求"""
        msg = message.message_str.replace("deep3.1", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：deep3.1 <提问内容>\n\n示例：deep3.1 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/depsek3.1.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error("请求DeepSeek-3.1助手失败，服务器返回错误状态码")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到DeepSeek-3.1助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求DeepSeek-3.1助手时发生错误：{e}")
            return CommandResult().error(f"请求DeepSeek-3.1助手时发生错误：{str(e)}")

    @filter.command("gpt5")
    async def gpt5_nano(self, message: AstrMessageEvent):
        """GPT5-nano助手，支持记忆功能"""
        msg = message.message_str.replace("gpt5", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：gpt5 《问题》 记忆 《记忆密钥6位数》\n\n示例：gpt5 1+1 记忆 123456")
        
        # 解析用户输入，检查是否包含"记忆"关键字
        if "记忆" not in msg:
            return CommandResult().error("你没有填写记忆哦，这样是大众池哦，你的记忆会被篡改，你需要填写记忆\n\n正确格式：gpt5 《问题》 记忆 《记忆密钥6位数》\n\n示例：gpt5 1+1 记忆 123456")
        
        # 分割输入，提取问题和uid
        parts = msg.split("记忆")
        if len(parts) != 2:
            return CommandResult().error("正确格式：gpt5 《问题》 记忆 《记忆密钥6位数》\n\n示例：gpt5 1+1 记忆 123456")
        
        question = parts[0].strip()
        uid = parts[1].strip()
        
        # 验证uid是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆密钥必须是6位数字\n\n正确格式：gpt5 《问题》 记忆 《记忆密钥6位数》\n\n示例：gpt5 1+1 记忆 123456")
        
        api_url = "https://api.jkyai.top/API/gpt5-nano/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求GPT5-nano助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到GPT5-nano助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求GPT5-nano助手时发生错误：{e}")
            return CommandResult().error(f"请求GPT5-nano助手时发生错误：{str(e)}")

    @filter.command("克劳德")
    async def claude_hiku(self, message: AstrMessageEvent):
        """Claude4.5-hiku助手，支持记忆功能"""
        msg = message.message_str.replace("克劳德", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：克劳德 《问题》 记忆 《记忆密钥6位数》\n\n示例：克劳德 1+1 记忆 123456")
        
        # 解析用户输入，检查是否包含"记忆"关键字
        if "记忆" not in msg:
            return CommandResult().error("你没有填写记忆哦，这样是大众池哦，你的记忆会被篡改，你需要填写记忆\n\n正确格式：克劳德 《问题》 记忆 《记忆密钥6位数》\n\n示例：克劳德 1+1 记忆 123456")
        
        # 分割输入，提取问题和uid
        parts = msg.split("记忆")
        if len(parts) != 2:
            return CommandResult().error("正确格式：克劳德 《问题》 记忆 《记忆密钥6位数》\n\n示例：克劳德 1+1 记忆 123456")
        
        question = parts[0].strip()
        uid = parts[1].strip()
        
        # 验证uid是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆密钥必须是6位数字\n\n正确格式：克劳德 《问题》 记忆 《记忆密钥6位数》\n\n示例：克劳德 1+1 记忆 123456")
        
        api_url = "https://api.jkyai.top/API/hiku-4.5/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求Claude4.5-hiku助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到Claude4.5-hiku助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求Claude4.5-hiku助手时发生错误：{e}")
            return CommandResult().error(f"请求Claude4.5-hiku助手时发生错误：{str(e)}")

    @filter.command("通义千问")
    async def qwen3_coder(self, message: AstrMessageEvent):
        """通义千问助手，支持记忆功能"""
        msg = message.message_str.replace("通义千问", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：通义千问 《问题》 记忆 《记忆密钥6位数》\n\n示例：通义千问 1+1 记忆 111111")
        
        # 解析用户输入，检查是否包含"记忆"关键字
        if "记忆" not in msg:
            return CommandResult().error("你没有填写记忆哦，这样是大众池哦，你的记忆会被篡改，你需要填写记忆\n\n正确格式：通义千问 《问题》 记忆 《记忆密钥6位数》\n\n示例：通义千问 1+1 记忆 111111")
        
        # 分割输入，提取问题和uid
        parts = msg.split("记忆")
        if len(parts) != 2:
            return CommandResult().error("正确格式：通义千问 《问题》 记忆 《记忆密钥6位数》\n\n示例：通义千问 1+1 记忆 111111")
        
        question = parts[0].strip()
        uid = parts[1].strip()
        
        # 验证uid是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆密钥必须是6位数字\n\n正确格式：通义千问 《问题》 记忆 《记忆密钥6位数》\n\n示例：通义千问 1+1 记忆 111111")
        
        api_url = "https://api.jkyai.top/API/qwen3-coder/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求通义千问助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到通义千问助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求通义千问助手时发生错误：{e}")
            return CommandResult().error(f"请求通义千问助手时发生错误：{str(e)}")

    @filter.command("deepR1")
    async def deepseek_r1(self, message: AstrMessageEvent):
        """DeepSeek-R1助手，支持异步请求"""
        msg = message.message_str.replace("deepR1", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：deepR1 <提问内容>\n\n示例：deepR1 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/deepseek.php"
        params = {
            "question": question
        }
        
        try:
            # 根据文档，该API响应速度较慢，设置较长超时时间
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求DeepSeek-R1助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到DeepSeek-R1助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求DeepSeek-R1助手时发生错误：{e}")
            return CommandResult().error(f"请求DeepSeek-R1助手时发生错误：{str(e)}")

    @filter.command("智谱")
    async def glm46(self, message: AstrMessageEvent):
        """智谱GLM4.6助手，支持异步请求"""
        msg = message.message_str.replace("智谱", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：智谱 <提问内容>\n\n示例：智谱 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/glm4.6.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求智谱GLM4.6助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到智谱GLM4.6助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求智谱GLM4.6助手时发生错误：{e}")
            return CommandResult().error(f"请求智谱GLM4.6助手时发生错误：{str(e)}")
    
    @filter.command("夸克")
    async def kuaike_ai(self, message: AstrMessageEvent):
        """夸克AI助手，支持异步请求"""
        msg = message.message_str.replace("夸克", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：夸克 <提问内容>\n\n示例：夸克 1+1")
        
        content = msg.strip()
        
        api_url = "https://api.jkyai.top/API/kkaimx.php"
        params = {
            "content": content
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求夸克AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到夸克AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求夸克AI助手时发生错误：{e}")
            return CommandResult().error(f"请求夸克AI助手时发生错误：{str(e)}")

    async def terminate(self):
        """插件卸载/重载时调用"""
        pass
