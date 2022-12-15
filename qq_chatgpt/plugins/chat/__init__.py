from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment
from nonebot import on_keyword, get_driver, logger
from .config import default_config, OpenAIConfig
import openai
import pickle
import ast

try:
    # print(Config.parse_obj(get_driver().config))
    openai_config = OpenAIConfig.parse_obj(get_driver().config)
    openai.api_key = openai_config.openai_api_key
    openai.organization = openai_config.openai_organization
except Exception as e:
    import sys
    logger.opt(colors=True).critical(f'<r>OPENAI API KEY获取失败</r>, 错误信息:\n{e}')
    sys.exit()

# TODO:edit paragraph
# TODO:replace on_keyword with on_command
catch_ask_str = on_keyword(keywords={".ask", "/问一下", "/问问"})
catch_chat_str = on_keyword(keywords={".chat", "/聊天"})
catch_help_str = on_keyword(keywords={".help", "/帮助"})
catch_edit_str = on_keyword(keywords={".edit", "/编辑"})
catch_clear_str = on_keyword(keywords={".clear", "/清除"})
catch_image_str = on_keyword(keywords={".image", "/图片"})
catch_test_str = on_keyword(keywords={".test", "/测试"})
catch_backup_str = on_keyword(keywords={".backup", "/备份"})
catch_load_str = on_keyword(keywords={".load", "/恢复"})

group_sessions = {}
private_sessions = {}


@catch_ask_str.handle()
async def group_ask_msg(bot: Bot, event: Event, gm: GroupMessageEvent):
    group_id, msg_id = gm.group_id, gm.message_id
    # determine if group_sessions has key "f"group_{group_id}""
    key = f"group_{group_id}"
    if not group_sessions.get(key):
        group_sessions[key] = default_config.copy()
    local_config = group_sessions[key]
    questions = event.get_plaintext().replace(".ask", "")
    local_config["text_completion"]["prompt"] = f"Q:{questions}\nA: "
    response = openai.Completion.create(**local_config["text_completion"])
    response_text = response["choices"][0]["text"].strip()
    msg = Message(f"[CQ:reply,id={msg_id}]{response_text}")
    await catch_ask_str.finish(msg)


@catch_ask_str.handle()
async def private_ask_msg(bot: Bot, event: Event, pm: PrivateMessageEvent):
    user_id = pm.user_id  # or event.get_user_id()
    # determine if group_sessions has key "f"private_{user_id}""
    key = f"private_{user_id}"
    if not private_sessions.get(key):
        private_sessions[key] = default_config.copy()
    local_config = private_sessions[key]
    questions = event.get_plaintext().replace(".ask", "")
    local_config["text_completion"]["prompt"] = f"Q:{questions}\nA: "
    response = openai.Completion.create(**local_config["text_completion"])
    # delelte the "\n" in resopnse_text
    response_text = response["choices"][0]["text"].strip()
    msg = Message(response_text)
    await catch_ask_str.finish(msg)


@catch_chat_str.handle()
async def group_chat_msg(bot: Bot, event: Event, gm: GroupMessageEvent):
    group_id, msg_id = gm.group_id, gm.message_id
    # determine if group_sessions has key "f"group_{group_id}""
    key = f"group_{group_id}"
    if not group_sessions.get(key):
        group_sessions[key] = default_config.copy()
    local_config = group_sessions[key]
    questions = event.get_plaintext().replace(".chat", "")
    local_config["context"] += f"Q:{questions}\nA: "
    local_config["text_completion"]["prompt"] = local_config["context"]
    response = openai.Completion.create(**local_config["text_completion"])
    response_text = response["choices"][0]["text"].strip()
    local_config["context"] += f"{response_text}\n\n"
    msg = Message(f"[CQ:reply,id={msg_id}]{response_text}")
    await catch_chat_str.finish(msg)


@catch_chat_str.handle()
async def private_chat_msg(bot: Bot, event: Event, pm: PrivateMessageEvent):
    user_id = pm.user_id  # or event.get_user_id()
    # determine if group_sessions has key "f"private_{user_id}""
    key = f"private_{user_id}"
    if not private_sessions.get(key):
        private_sessions[key] = default_config.copy()
    local_config = private_sessions[key]
    questions = event.get_plaintext().replace(".chat", "")
    local_config["context"] += f"Q:{questions}\nA: "
    local_config["text_completion"]["prompt"] = local_config["context"]
    response = openai.Completion.create(**local_config["text_completion"])
    response_text = response["choices"][0]["text"].strip()
    local_config["context"] += f"{response_text}\n\n"
    msg = Message(response_text)
    await catch_chat_str.finish(msg)


@catch_image_str.handle()
async def send_image_msg(bot: Bot, event: Event):
    prompt = event.get_plaintext().replace(".image", "")
    await catch_image_str.send(Message("Image generating... Please wait."))
    for size in ["256x256", "512x512", "1024x1024"]:
        if size in prompt:
            default_config["generate_image"]["size"] = size
            prompt = prompt.replace(size, "")
    default_config["generate_image"]["prompt"] = prompt
    response = openai.Image.create(**default_config["generate_image"])
    image_url = response["data"][0]["url"]
    msg = Message(MessageSegment.image(image_url))
    await catch_image_str.finish(msg)


@catch_clear_str.handle()
async def send_clear_msg(bot: Bot, event: Event):
    default_config["context"] = ""
    msg = Message("cleared all contexts! 已清除所有上下文！")
    await catch_clear_str.finish(msg)


@catch_backup_str.handle()
async def backup(bot: Bot, event: Event):
    # back up all sessions to pickles
    with open("./qq_chatgpt/pkl/group_sessions.pkl", "wb") as f:
        pickle.dump(group_sessions, f)
    with open("./qq_chatgpt/pkl/private_sessions.pkl", "wb") as f:
        pickle.dump(private_sessions, f)
    msg = Message("已备份所有数据！")
    await catch_clear_str.finish(msg)


@catch_load_str.handle()
async def load(bot: Bot, event: Event):
    # load all sessions from pickles
    with open("./qq_chatgpt/pkl/group_sessions.pkl", "rb") as f:
        group_sessions = pickle.load(f)
    with open("./qq_chatgpt/pkl/private_sessions.pkl", "rb") as f:
        private_sessions = pickle.load(f)
    print(group_sessions)
    print(private_sessions)
    msg = Message("已加载所有数据！")
    await catch_clear_str.finish(msg)


async def send_help_msg(bot: Bot, event: Event):
    msg = Message("""
欢迎使用chatbot QQ机器人！
基于NoneBot2.0，使用ChatGPT API实现的聊天机器人。
.ask 问AI问题，不产生上下文
.chat 与AI聊天，产生上下文
.clear 清除上下文
.image 生成图片，需输入图片描述
.help 查看帮助
[作者：@nanguagua]
        """.strip())
    await catch_help_str.finish(msg)


@catch_test_str.handle()
async def send_test_msg(bot: Bot, event: Event, pm: PrivateMessageEvent):
    # userid = int(event.get_user_id())
    # group_id = group_event.group_id
    # print(group_id)
    data = await bot.call_api("get_group_info", group_id=980698737)
    # 对json进行转义
    data = ast.literal_eval(str(data))
    print(data)
    # await bot.send_group_msg(group_id=980698737, message="test ok!")
    # msg = MessageSegment.location(latitude=39.90469, longitude=116.40717)
    # seq = bot.call_api("get_msg", message_id=ME.message_id)
    # print("the_seq_is:", str(seq.cr_code))
    msg = Message(f"[CQ:reply,id={pm.message_id}]123")
    await catch_test_str.send(msg)
    msg = Message([
        MessageSegment.text(f"群号：{data['group_id']}\n"),
        MessageSegment.text(f"群名称：{data['group_name']}\n"),
        # MessageSegment.image("https://cdn.luogu.com.cn/fe/logo.png"),
        MessageSegment.text(f"成员数：{data['member_count']}\n"),
    ])
    await catch_test_str.send(msg)
    # await catch_test_str.send(
    #     MessageSegment.image(
    #         file="https://cdn.luogu.com.cn/fe/logo.png", type_="flash"
    #     )
    # )
    await catch_test_str.finish()
