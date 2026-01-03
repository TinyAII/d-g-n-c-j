import asyncio
import logging
import aiohttp
import urllib.parse
from astrbot.api.all import AstrMessageEvent, CommandResult, Context, Plain
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star

logger = logging.getLogger("astrbot")


@register("D-G-N-C-J", "Tinyxi", "腾讯元宝+DeepSeek-3.2+DeepSeek-3.1+GPT5-nano+Claude4.5-hiku+Qwen3-coder+DeepSeek-R1+智谱GLM4.6+夸克AI+蚂蚁AI+豆包AI+ChatGPT-oss+谷歌Gemini-2.5+阿里AI+讯飞AI", "1.0.0", "")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

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
                "timeout_ms": 30000
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
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, params=params) as resp:
                    if resp.status != 200:
                        yield CommandResult().error(f"解题助手请求失败，服务器返回错误状态码：{resp.status}")
                        return
                    
                    result = await resp.json()
                    
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
                        image_url = await self.text_to_image(formatted_content)
                        yield message.image_result(image_url)
                    except Exception as img_error:
                        logger.error(f"生成图片失败：{img_error}")
                        # 如果生成图片失败，返回文本格式
                        yield CommandResult().error(f"生成图片失败，请稍后重试\n\n{formatted_content}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"网络连接错误：{e}")
            yield CommandResult().error("无法连接到解题助手服务器，请稍后重试")
        except asyncio.TimeoutError:
            logger.error("请求超时")
            yield CommandResult().error("请求超时，请稍后重试")
        except Exception as e:
            logger.error(f"解题助手请求时发生错误：{e}")
            yield CommandResult().error(f"请求时发生错误：{str(e)}")
