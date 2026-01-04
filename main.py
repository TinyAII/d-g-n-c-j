import asyncio
import logging
import aiohttp
import urllib.parse
import json
import re
from astrbot.api.all import AstrMessageEvent, CommandResult, Context, Plain
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star
from astrbot.api.message_components import Image as MsgImage, Reply

logger = logging.getLogger("astrbot")


@register("D-G-N-C-J", "Tinyxi", "腾讯元宝+DeepSeek-3.2+DeepSeek-3.1+GPT5-nano+Claude4.5-hiku+Qwen3-coder+DeepSeek-R1+智谱GLM4.6+夸克AI+蚂蚁AI+豆包AI+ChatGPT-oss+谷歌Gemini-2.5+阿里AI+讯飞AI", "1.0.0", "")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.waiting_sessions = {}  # 存储等待图片的会话
        self.timeout_tasks = {}  # 存储超时任务

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
            return CommandResult().error("正确指令：gpt5 <记忆数> <提问内容>\n\n示例：gpt5 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：gpt5 <记忆数> <提问内容>\n\n示例：gpt5 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：gpt5 <记忆数> <提问内容>\n\n示例：gpt5 123456 你好")
        
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
            return CommandResult().error("正确指令：克劳德 <记忆数> <提问内容>\n\n示例：克劳德 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：克劳德 <记忆数> <提问内容>\n\n示例：克劳德 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：克劳德 <记忆数> <提问内容>\n\n示例：克劳德 123456 你好")
        
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
            return CommandResult().error("正确指令：通义千问 <记忆数> <提问内容>\n\n示例：通义千问 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：通义千问 <记忆数> <提问内容>\n\n示例：通义千问 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：通义千问 <记忆数> <提问内容>\n\n示例：通义千问 123456 你好")
        
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
    
    @filter.command("蚂蚁")
    async def ant_ling_ai(self, message: AstrMessageEvent):
        """蚂蚁Ling2.0-1tAI助手，支持异步请求"""
        msg = message.message_str.replace("蚂蚁", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：蚂蚁 <提问内容>\n\n示例：蚂蚁 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/ling-1t.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求蚂蚁AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到蚂蚁AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求蚂蚁AI助手时发生错误：{e}")
            return CommandResult().error(f"请求蚂蚁AI助手时发生错误：{str(e)}")
    
    @filter.command("豆包")
    async def doubao_ai(self, message: AstrMessageEvent):
        """字节跳动豆包AI助手，支持异步请求"""
        msg = message.message_str.replace("豆包", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：豆包 <提问内容>\n\n示例：豆包 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/doubao.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求豆包AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到豆包AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求豆包AI助手时发生错误：{e}")
            return CommandResult().error(f"请求豆包AI助手时发生错误：{str(e)}")
    
    @filter.command("gpt")
    async def chatgpt_oss(self, message: AstrMessageEvent):
        """ChatGPT-ossAI助手，支持记忆功能"""
        msg = message.message_str.replace("gpt", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：gpt <记忆数> <提问内容>\n\n示例：gpt 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：gpt <记忆数> <提问内容>\n\n示例：gpt 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：gpt <记忆数> <提问内容>\n\n示例：gpt 123456 你好")
        
        api_url = "https://api.jkyai.top/API/chatgpt-oss/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求ChatGPT-ossAI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到ChatGPT-ossAI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求ChatGPT-ossAI助手时发生错误：{e}")
            return CommandResult().error(f"请求ChatGPT-ossAI助手时发生错误：{str(e)}")
    
    @filter.command("谷歌")
    async def gemini_ai(self, message: AstrMessageEvent):
        """Gemini-2.5AI助手，支持记忆功能"""
        msg = message.message_str.replace("谷歌", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：谷歌 <记忆数> <提问内容>\n\n示例：谷歌 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：谷歌 <记忆数> <提问内容>\n\n示例：谷歌 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：谷歌 <记忆数> <提问内容>\n\n示例：谷歌 123456 你好")
        
        api_url = "https://api.jkyai.top/API/gemini2.5/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求谷歌Gemini-2.5AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到谷歌Gemini-2.5AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求谷歌Gemini-2.5AI助手时发生错误：{e}")
            return CommandResult().error(f"请求谷歌Gemini-2.5AI助手时发生错误：{str(e)}")
    
    @filter.command("阿里")
    async def qwen3_ai(self, message: AstrMessageEvent):
        """阿里云千问Qwen3-235bAI助手，支持异步请求"""
        msg = message.message_str.replace("阿里", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：阿里 <提问内容>\n\n示例：阿里 1+1")
        
        question = msg.strip()
        
        api_url = "https://api.jkyai.top/API/qwen3.php"
        params = {
            "question": question
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求阿里AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到阿里AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求阿里AI助手时发生错误：{e}")
            return CommandResult().error(f"请求阿里AI助手时发生错误：{str(e)}")
    
    @filter.command("讯飞")
    async def xfxhx1_ai(self, message: AstrMessageEvent):
        """讯飞星火X1AI助手，支持异步请求"""
        msg = message.message_str.replace("讯飞", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：讯飞 <提问内容>\n\n示例：讯飞 1+1")
        
        content = msg.strip()
        
        api_url = "https://api.jkyai.top/API/xfxhx1.php"
        params = {
            "content": content
        }
        
        try:
            # API文档显示响应耗时较长（6.70s），设置较长超时时间
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求讯飞AI助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到讯飞AI助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求讯飞AI助手时发生错误：{e}")
            return CommandResult().error(f"请求讯飞AI助手时发生错误：{str(e)}")
    
    @filter.command("小米")
    async def xiaomi_mimo(self, message: AstrMessageEvent):
        """小米MiMo-V2助手，支持记忆功能"""
        msg = message.message_str.replace("小米", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：小米 <记忆数> <提问内容>\n\n示例：小米 123456 你好")
        
        # 分割输入，提取记忆数和问题
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            return CommandResult().error("正确格式：小米 <记忆数> <提问内容>\n\n示例：小米 123456 你好")
        
        uid = parts[0].strip()
        question = parts[1].strip()
        
        # 验证记忆数是否为6位数字
        if not uid.isdigit() or len(uid) != 6:
            return CommandResult().error("记忆数必须是6位数字\n\n正确格式：小米 <记忆数> <提问内容>\n\n示例：小米 123456 你好")
        
        api_url = "https://api.jkyai.top/API/xiaomi/index.php"
        params = {
            "question": question,
            "uid": uid
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        return CommandResult().error(f"请求小米MiMo-V2助手失败，服务器返回错误状态码：{resp.status}")
                    
                    result = await resp.text()
                    
                    return CommandResult().message(result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("无法连接到小米MiMo-V2助手服务器，请稍后重试或检查网络连接")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"请求小米MiMo-V2助手时发生错误：{e}")
            return CommandResult().error(f"请求小米MiMo-V2助手时发生错误：{str(e)}")
    
    @filter.command("联网模式")
    async def lian_wang_mo_xing(self, message: AstrMessageEvent):
        """联网模式，结合搜索引擎和AI进行问答"""
        msg = message.message_str.replace("联网模式", "").strip()
        
        if not msg:
            return CommandResult().error("正确指令：联网模式 <提问内容>\n\n示例：联网模式 明日方舟最厉害的是谁")
        
        question = msg.strip()
        
        try:
            # 1. 调用搜索引擎API获取相关信息
            search_url = "https://uapis.cn/api/v1/search/aggregate"
            search_params = {
                "query": question,
                "timeout_ms": 30000,
                "sort": "date"  # 按日期排序
            }
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # 发送搜索引擎请求
                async with session.post(search_url, json=search_params) as search_resp:
                    if search_resp.status != 200:
                        return CommandResult().error(f"搜索引擎请求失败，服务器返回错误状态码：{search_resp.status}")
                    
                    search_result = await search_resp.json()
                    
                    # 2. 整理搜索结果，提取标题、片段和发布日期
                    search_info = []
                    for item in search_result.get("results", [])[:5]:  # 取前5条结果
                        title = item.get("title", "")
                        snippet = item.get("snippet", "")
                        publish_time = item.get("publish_time", "")
                        if title and snippet:
                            # 简化发布日期格式
                            if publish_time:
                                # 将ISO格式转换为YYYY-MM-DD格式
                                simple_time = publish_time.split("T")[0]
                            else:
                                simple_time = ""
                            search_info.append(f"标题：{title}\n片段：{snippet}\n发布日期：{simple_time}\n")
                    
                    # 3. 构建给DeepSeek-3.2的问题
                    combined_question = f"用户的问题是：{question}\n\n请结合以下搜索信息回答用户问题：\n{''.join(search_info)}\n\n注意：这是回答QQ平台的问题，请注意违禁词，回答要简洁明了，直接给出答案，不需要过多解释。"
                    
                    # 4. 调用DeepSeek-3.2API
                    deepseek_url = "https://api.jkyai.top/API/depsek3.2.php"
                    deepseek_params = {
                        "question": combined_question
                    }
                    
                    async with session.get(deepseek_url, params=deepseek_params) as deepseek_resp:
                        if deepseek_resp.status != 200:
                            return CommandResult().error(f"DeepSeek-3.2请求失败，服务器返回错误状态码：{deepseek_resp.status}")
                        
                        ai_result = await deepseek_resp.text()
                        
                        return CommandResult().message(ai_result)
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            return CommandResult().error("网络连接错误，请稍后重试")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            return CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"联网模型请求时发生错误：{e}")
            return CommandResult().error(f"请求时发生错误：{str(e)}")

    async def terminate(self):
        """插件卸载/重载时调用"""
        pass
        
    async def extract_image_from_event(self, event: AstrMessageEvent) -> str:
        """从事件中提取图片URL"""
        messages = event.get_messages()

        # 首先检查当前消息中的图片
        for msg in messages:
            # 标准图片组件
            if isinstance(msg, MsgImage):
                if hasattr(msg, "url") and msg.url:
                    return msg.url.strip()
                if hasattr(msg, "file") and msg.file:
                    # 从file字段提取URL - 处理微信格式
                    file_content = str(msg.file)
                    if "http" in file_content:
                        # 提取URL并移除反引号
                        urls = re.findall(r"https?://[^\s\`\']+", file_content)
                        if urls:
                            return urls[0].strip("`'")

            # QQ官方平台特殊处理
            if hasattr(msg, "type") and msg.type == "Plain":
                text = str(msg.text) if hasattr(msg, "text") else str(msg)
                if "attachmentType=" in text and "image" in text:
                    # 这是QQ官方的图片消息格式，需要后续消息处理
                    continue

        # 检查引用消息中的图片（Telegram等平台）
        try:
            # 查找Reply组件
            for msg in messages:
                if isinstance(msg, Reply):
                    # Reply组件包含原始消息的信息
                    if hasattr(msg, "chain") and msg.chain:
                        # 在引用消息的chain中查找图片
                        for reply_msg in msg.chain:
                            if isinstance(reply_msg, MsgImage):
                                if hasattr(reply_msg, "url") and reply_msg.url:
                                    return reply_msg.url.strip()
                                if hasattr(reply_msg, "file") and reply_msg.file:
                                    file_content = str(reply_msg.file)
                                    if "http" in file_content:
                                        urls = re.findall(r"https?://[^\s\`\']+", file_content)
                                        if urls:
                                            return urls[0].strip("`'")

        except Exception as e:
            logger.warning(f"检查引用消息图片时出错: {str(e)}")

        return None
        
    async def timeout_check(self, user_id: str, event: AstrMessageEvent):
        """检查用户发送图片是否超时"""
        try:
            await asyncio.sleep(30)  # 等待30秒
            if user_id in self.waiting_sessions:
                # 超时，发送消息
                await event.send(event.plain_result("⏰ 图片发送超时，请重新发送命令开始新的请求"))
                # 清理会话和超时任务
                del self.waiting_sessions[user_id]
                if user_id in self.timeout_tasks:
                    del self.timeout_tasks[user_id]
        except asyncio.CancelledError:
            # 任务被取消，说明用户已经发送了图片
            pass
        except Exception as e:
            logger.error(f"超时检查出错: {str(e)}")
            
    async def ocr_recognize(self, image_url: str) -> str:
        """调用OCR API识别图片中的文字"""
        try:
            ocr_url = "https://api.pearktrue.cn/api/ocr/"
            payload = {
                "file": image_url
            }
            
            logger.debug(f"OCR识别请求：图片URL = {image_url}")
            logger.debug(f"OCR API URL = {ocr_url}")
            logger.debug(f"请求参数 = {payload}")
            
            # 增加超时时间到120秒
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.post(ocr_url, json=payload) as resp:
                        logger.debug(f"OCR API响应状态码：{resp.status}")
                        logger.debug(f"响应头：{resp.headers}")
                        
                        if resp.status != 200:
                            resp_text = await resp.text()
                            logger.error(f"OCR API请求失败，状态码：{resp.status}，响应内容：{resp_text}")
                            raise Exception(f"OCR API请求失败，状态码：{resp.status}，响应：{resp_text[:100]}...")
                        
                        # 先读取响应文本，记录日志
                        resp_text = await resp.text()
                        logger.debug(f"OCR API响应内容：{resp_text}")
                        
                        try:
                            result = json.loads(resp_text)
                        except json.JSONDecodeError as json_error:
                            logger.error(f"OCR API返回JSON格式错误：{str(json_error)}，响应内容：{resp_text}")
                            raise Exception(f"OCR API返回JSON格式错误：{str(json_error)}")
                        
                        if result.get("code") != 200:
                            logger.error(f"OCR识别失败：{result.get('msg', '未知错误')}")
                            raise Exception(f"OCR识别失败：{result.get('msg', '未知错误')}")
                        
                        # 获取识别结果
                        parsed_text = result.get("data", {}).get("ParsedText", "")
                        if not parsed_text:
                            # 如果ParsedText为空，尝试从TextLine拼接
                            text_lines = result.get("data", {}).get("TextLine", [])
                            parsed_text = "\n".join(text_lines)
                        
                        logger.debug(f"OCR识别成功，识别结果：{parsed_text[:100]}...")
                        return parsed_text.strip()
                except asyncio.TimeoutError:
                    logger.error(f"OCR API请求超时，图片URL：{image_url}")
                    raise Exception("OCR识别超时，请稍后重试")
                except aiohttp.ClientError as client_error:
                    logger.error(f"OCR API网络请求错误：{str(client_error)}，图片URL：{image_url}")
                    raise Exception(f"OCR识别网络错误：{str(client_error)}")
        except Exception as e:
            logger.error(f"OCR识别出错: {str(e)}")
            logger.exception("OCR识别异常详情")
            raise
            
    async def process_image_question_solving(self, event: AstrMessageEvent, image_url: str):
        """处理图片解题的完整流程"""
        try:
            # 1. 调用OCR识别图片中的题目
            yield CommandResult().message("正在识别图片中的题目，请稍候...")
            try:
                question_text = await self.ocr_recognize(image_url)
            except asyncio.TimeoutError:
                yield CommandResult().error("OCR识别超时，服务器响应过慢\n\n建议：\n1. 检查网络连接\n2. 确保图片清晰可辨\n3. 稍后重试")
                return
            except Exception as ocr_error:
                yield CommandResult().error(f"OCR识别失败：{str(ocr_error)}\n\n建议：\n1. 检查网络连接\n2. 确保图片清晰可辨\n3. 稍后重试")
                return
            
            if not question_text:
                yield CommandResult().error("OCR识别失败，未能从图片中提取到题目内容")
                return
            
            # 2. 调用万能解题助手API
            yield CommandResult().message("正在解题，请稍候...")
            api_url = "https://api.jkyai.top/API/wnjtzs.php"
            params = {
                "question": question_text,
                "type": "json"  # 返回json格式，便于解析
            }
            
            timeout = aiohttp.ClientTimeout(total=120)  # 延长超时时间到120秒
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(api_url, params=params) as resp:
                        if resp.status != 200:
                            yield CommandResult().error(f"解题助手请求失败，服务器返回错误状态码：{resp.status}")
                            return
                        
                        # 检查响应头的Content-Type
                        content_type = resp.headers.get('Content-Type', '')
                        if 'application/json' not in content_type:
                            # 如果不是json，先尝试读取文本内容
                            text_content = await resp.text()
                            yield CommandResult().error(f"解题助手返回格式错误，预期JSON但得到：{text_content[:100]}...")
                            return
                        
                        try:
                            result = await resp.json()
                        except json.JSONDecodeError as e:
                            yield CommandResult().error(f"解题助手返回JSON格式错误：{str(e)}")
                            return
                        
                        # 3. 解析API返回结果
                        status = result.get("status", "")
                        if status != "success":
                            error_msg = result.get("answer", "解题助手请求失败")
                            yield CommandResult().error(f"解题助手请求失败：{error_msg}")
                            return
                        
                        # 获取data字段
                        data = result.get("data", {})
                        answer = data.get("answer", "")
                        
                        # 获取created_at
                        metadata = data.get("metadata", {})
                        created_at = metadata.get("created_at", "")
                        
                        # 4. 提取思考过程和答案
                        # 从answer中提取思考过程和答案
                        # answer格式：<Think>思考内容</Think>【解题答案：答案内容】
                        think_start = answer.find("<Think>")
                        think_end = answer.find("</Think>")
                        if think_start != -1 and think_end != -1:
                            thinking = answer[think_start+6:think_end].strip()
                            answer_content = answer[think_end+8:].strip()
                            # 移除可能的【解题答案：】前缀
                            if answer_content.startswith("【解题答案："):
                                answer_content = answer_content[7:].strip()
                                if answer_content.endswith("】"):
                                    answer_content = answer_content[:-1].strip()
                        else:
                            # 如果没有<Think>标签，直接使用answer作为答案
                            thinking = ""  # 没有思考过程
                            answer_content = answer.strip()
                        
                        # 5. 格式化内容
                        formatted_content = f"题目：\n{question_text}\n\n思考过程：\n{thinking}\n\n答案：\n{answer_content}\n\n时间：\n{created_at}"
                        
                        # 6. 生成图片
                        try:
                            # 返回处理中的提示
                            yield CommandResult().message("正在生成图片，请稍候...")
                            
                            image_url = await self.text_to_image_menu_style(formatted_content)
                            yield event.image_result(image_url)
                        except Exception as img_error:
                            logger.error(f"生成图片失败：{img_error}")
                            # 详细记录错误信息
                            logger.exception("生成图片时发生异常")
                            # 如果生成图片失败，直接返回文本格式
                            yield CommandResult().message(f"图片生成失败，以下是文本答案：\n\n{formatted_content}")
                except asyncio.TimeoutError:
                    yield CommandResult().error("解题助手请求超时，服务器响应过慢\n\n建议：\n1. 检查网络连接\n2. 稍后重试")
                    return
                except aiohttp.ClientError as client_error:
                    yield CommandResult().error(f"解题助手网络请求失败：{str(client_error)}\n\n建议：\n1. 检查网络连接\n2. 稍后重试")
                    return
                        
        except Exception as e:
            logger.error(f"图片解题失败：{str(e)}")
            logger.exception("图片解题异常详情")
            # 增加更友好的错误提示
            yield CommandResult().error(f"图片解题失败：{str(e)}\n\n可能的原因：\n1. 图片链接不可访问\n2. 图片中没有可识别的文字\n3. 网络连接问题\n4. 服务器暂时不可用\n\n请检查图片是否清晰可辨，或稍后重试")
    
    # 菜单样式的HTML模板
    MENU_TEMPLATE = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>解题助手</title>
        <style>
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .content {
                white-space: pre-wrap;
                font-size: 16px;
                color: #333;
                font-weight: normal;
                text-align: left;
            }
            .title {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">{{content}}</div>
        </div>
    </body>
    </html>
    '''
    
    async def text_to_image_menu_style(self, text: str) -> str:
        """使用菜单样式的HTML模板生成图片"""
        try:
            # 渲染HTML模板
            html_content = self.MENU_TEMPLATE.replace("{{content}}", text)
            
            # 使用html_render函数生成图片
            options = {
                "full_page": True,
                "type": "jpeg",
                "quality": 95,
            }
            
            image_url = await self.html_render(
                html_content,  # 渲染后的HTML内容
                {},  # 空数据字典
                True,  # 返回URL
                options  # 图片生成选项
            )
            
            return image_url
        except Exception as e:
            logger.error(f"菜单样式图片生成失败：{e}")
            # 回退到默认的text_to_image方法
            return await self.text_to_image(text)
    
    @filter.command("解题助手")
    async def jie_ti_zhu_shou(self, message: AstrMessageEvent):
        """解题助手，支持数学和物理方面的题目，返回图片格式的解题结果"""
        msg = message.message_str.replace("解题助手", "").strip()
        
        if not msg:
            yield CommandResult().error("正确指令：解题助手 <题目内容>\n\n示例：解题助手 1+1")
            return
        
        question = msg.strip()
        
        try:
            # 1. 调用万能解题助手API
            api_url = "https://api.jkyai.top/API/wnjtzs.php"
            params = {
                "question": question,
                "type": "json"  # 返回json格式，便于解析
            }
            
            timeout = aiohttp.ClientTimeout(total=120)  # 延长超时时间到120秒
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        yield CommandResult().error(f"解题助手请求失败，服务器返回错误状态码：{resp.status}")
                        return
                    
                    # 检查响应头的Content-Type
                    content_type = resp.headers.get('Content-Type', '')
                    if 'application/json' not in content_type:
                        # 如果不是json，先尝试读取文本内容
                        text_content = await resp.text()
                        yield CommandResult().error(f"解题助手返回格式错误，预期JSON但得到：{text_content[:100]}...")
                        return
                    
                    try:
                        result = await resp.json()
                    except json.JSONDecodeError as e:
                        yield CommandResult().error(f"解题助手返回JSON格式错误：{str(e)}")
                        return
                    
                    # 2. 解析API返回结果
                    status = result.get("status", "")
                    if status != "success":
                        error_msg = result.get("answer", "解题助手请求失败")
                        yield CommandResult().error(f"解题助手请求失败：{error_msg}")
                        return
                    
                    # 获取data字段
                    data = result.get("data", {})
                    answer = data.get("answer", "")
                    
                    # 获取created_at
                    metadata = data.get("metadata", {})
                    created_at = metadata.get("created_at", "")
                    
                    # 3. 提取思考过程和答案
                    # 从answer中提取思考过程和答案
                    # answer格式：<Think>思考内容</Think>【解题答案：答案内容】
                    think_start = answer.find("<Think>")
                    think_end = answer.find("</Think>")
                    if think_start != -1 and think_end != -1:
                        thinking = answer[think_start+6:think_end].strip()
                        answer_content = answer[think_end+8:].strip()
                        # 移除可能的【解题答案：】前缀
                        if answer_content.startswith("【解题答案："):
                            answer_content = answer_content[7:].strip()
                            if answer_content.endswith("】"):
                                answer_content = answer_content[:-1].strip()
                    else:
                        # 如果没有<Think>标签，直接使用answer作为答案
                        thinking = ""  # 没有思考过程
                        answer_content = answer.strip()
                    
                    # 4. 格式化内容
                    formatted_content = f"题目：\n{question}\n\n思考过程：\n{thinking}\n\n答案：\n{answer_content}\n\n时间：\n{created_at}"
                    
                    # 5. 生成图片
                    try:
                        # 先返回一个处理中的提示
                        yield CommandResult().message("正在生成图片，请稍候...")
                        
                        image_url = await self.text_to_image_menu_style(formatted_content)
                        yield message.image_result(image_url)
                    except Exception as img_error:
                        logger.error(f"生成图片失败：{img_error}")
                        # 详细记录错误信息
                        logger.exception("生成图片时发生异常")
                        # 如果生成图片失败，直接返回文本格式
                        yield CommandResult().message(f"图片生成失败，以下是文本答案：\n\n{formatted_content}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            yield CommandResult().error("无法连接到解题助手服务器，请稍后重试")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            yield CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"解题助手请求时发生错误：{e}")
            yield CommandResult().error(f"请求时发生错误：{str(e)}")
    
    @filter.command("图片解题助手")
    async def tu_pian_jie_ti_zhu_shou(self, message: AstrMessageEvent):
        """图片解题助手，支持识别图片中的题目并解题，返回图片格式的解题结果"""
        user_id = message.get_sender_id()
        
        # 检查当前消息是否包含图片
        image_url = await self.extract_image_from_event(message)
        if image_url:
            # 如果找到图片，直接进行处理
            async for result in self.process_image_question_solving(message, image_url):
                yield result
            return
        
        # 如果没有图片，设置等待状态
        self.waiting_sessions[user_id] = {
            "timestamp": asyncio.get_event_loop().time(),
            "event": message  # 保存事件对象用于后续处理
        }
        
        # 创建30秒超时任务
        if user_id in self.timeout_tasks:
            self.timeout_tasks[user_id].cancel()  # 取消之前的超时任务
        
        timeout_task = asyncio.create_task(self.timeout_check(user_id, message))
        self.timeout_tasks[user_id] = timeout_task
        
        yield CommandResult().message("📷 请发送要识别的图片（30秒内有效）")
    
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """监听所有消息，处理等待中的图片请求"""
        user_id = event.get_sender_id()
        
        # 检查用户是否在等待图片
        if user_id not in self.waiting_sessions:
            return
        
        # 提取图片URL
        image_url = await self.extract_image_from_event(event)
        if not image_url:
            return  # 不是图片消息，继续等待
        
        # 找到图片，开始处理
        original_event = self.waiting_sessions[user_id]["event"]
        
        # 清理会话和超时任务
        del self.waiting_sessions[user_id]
        if user_id in self.timeout_tasks:
            self.timeout_tasks[user_id].cancel()
            del self.timeout_tasks[user_id]
        
        # 处理图片解题
        async for result in self.process_image_question_solving(original_event, image_url):
            await original_event.send(result)
