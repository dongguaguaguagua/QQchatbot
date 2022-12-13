from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
import openai
import os

from openai.api_resources import image

openai.organization = 'org-WvMRPik8NGGoWxdJf9QPwpkh'
openai.api_key = os.getenv('OPENAI_API_KEY')

catch_ask_str = on_keyword({'.ask'})
catch_chat_str = on_keyword({'.chat'})
catch_help_str = on_keyword({'.help'})
catch_edit_str = on_keyword({'.edit'})
catch_clear_str = on_keyword({'.clear'})
catch_image_str = on_keyword({'.image'})

default_config = {
    'api_key': '',
    'enable_context': True,
    'context': '',
    # Creates a completion for the provided prompt and parameters
    'completion': {
        # ID of the model to use.
        # You can use the List models API to see all of your available models,
        # or see our Model overview for descriptions of them.
        'model': 'text-davinci-003',
        # The prompt(s) to generate completions for, encoded as a string,
        # array of strings, array of tokens, or array of token arrays.
        'prompt': '',
        # What sampling temperature to use.
        # Higher values means the model will take more risks.
        # Try 0.9 for more creative applications,
        # and 0 (argmax sampling) for ones with a well-defined answer.
        # We generally recommend altering this or top_p but not both.
        'temperature': 0.9,
        # max_tokens is a parameter in the ChatGPT API that indicates the \
        # maximum number of tokens (words) that should be generated \
        # in the response. Increasing this number can make the response \
        # longer and more detailed, but it can also make the model slower.
        # The maximum number of tokens to generate in the completion.
        'max_tokens': 1024,
        # # An alternative to sampling with temperature, called nucleus sampling,
        # # where the model considers the results of the tokens with top_p probability mass.
        # # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        # # We generally recommend altering this or temperature but not both.
        # 'top_p': 1,
        # How many completions to generate for each prompt.
        'n': 1,
        # Whether to stream back partial progress.
        # If set, tokens will be sent as data-only server-sent events as they b
        # ecome available, with the stream terminated by a data: [DONE] message
        'stream': False,
        # Echo back the prompt in addition to the completion
        'echo': False,
        # The suffix that comes after a completion of inserted text.
        'suffix': None,
        # Up to 4 sequences where the API will stop generating further tokens.
        # The returned text will not contain the stop sequence.
        'stop': None,
    },
    # Given a prompt and an instruction,
    # the model will return an edited version of the prompt.
    'edit': {
        # ID of the model to use.
        # You can use the List models API to see all of your available models,
        # or see our Model overview for descriptions of them.
        'model': 'text-davinci-edit-001',
        # The input text to use as a starting point for the edit.
        'input': '',
        # The instruction that tells the model how to edit the prompt.
        'instruction': '',
        # How many edits to generate for the input and instruction.
        'n': 1,
        # Defaults to 1, What sampling temperature to use.
        # Higher values means the model will take more risks.
        # Try 0.9 for more creative applications,
        # and 0 (argmax sampling) for ones with a well-defined answer.
        'temperature': 0.9,
        # An alternative to sampling with temperature, called nucleus sampling,
        # where the model considers the results of the tokens with top_p
        # probability mass. So 0.1 means only the tokens comprising the top 10%
        # probability mass are considered.
        # # 'top_p' = 1,
    },
    'image': {
        # A text descr/iption of the desired image(s).
        # The maximum length is 1000 characters.
        'prompt': '',
        # The number of images to generate. Must be between 1 and 10.
        'n': 1,
        # The size of the generated images.
        # Must be one of 256x256, 512x512, or 1024x1024.
        'size': '256x256',
        # The format in which the generated images are returned.
        # Must be one of url or b64_json.
        'response_format': 'url',
    }
}


@catch_ask_str.handle()
async def send_ask_msg(bot: Bot, event: Event, state: T_State):
    # id = event.get_user_id()
    questions = str(event.get_message()).replace('.ask', '')
    default_config['completion']['prompt'] = f'Q:{questions}\nA: '
    response = openai.Completion.create(**default_config['completion'])
    response_text = response['choices'][0]['text'].strip()
    # msg = '[CQ:at,qq={}]'.format(id) + response_text
    msg = response_text
    await catch_ask_str.finish(Message(msg))


@catch_chat_str.handle()
async def send_chat_msg(bot: Bot, event: Event, state: T_State):
    # id = event.get_user_id()
    questions = str(event.get_message()).replace('.chat', '')
    default_config['context'] += f'Q:{questions}\nA: '
    default_config['completion']['prompt'] = default_config['context']
    response = openai.Completion.create(**default_config['completion'])
    response_text = response['choices'][0]['text'].strip()
    # msg = '[CQ:at,qq={}]'.format(id) + response_text
    default_config['context'] += f'{response_text}\n\n'
    print(default_config['context'])
    msg = response_text
    await catch_chat_str.finish(Message(msg))


@catch_image_str.handle()
async def send_image_msg(bot: Bot, event: Event, state: T_State):
    # id = event.get_user_id()
    prompt = str(event.get_message()).replace('.image', '')
    default_config['image']['prompt'] = prompt
    response = openai.Image.create(**default_config['image'])
    image_url = response['data'][0]['url']
    # msg = '[CQ:at,qq={}]'.format(id) + response_text
    msg = MessageSegment.image(image_url)
    await catch_image_str.finish(Message(msg))


@catch_clear_str.handle()
async def send_clear_msg(bot: Bot, event: Event, state: T_State):
    # id = event.get_user_id()
    default_config['context'] = ''
    msg = 'cleared all contexts! 已清除所有上下文！'
    await catch_clear_str.finish(Message(msg))


@catch_help_str.handle()
async def send_help_msg(bot: Bot, event: Event, state: T_State):
    msg = """
欢迎使用chatbot QQ机器人！
基于NoneBot2.0，使用ChatGPT API实现的聊天机器人。
.ask 问AI问题，不产生上下文
.chat 与AI聊天，产生上下文
.clear 清除上下文
.image 生成图片
.help 查看帮助
[作者：@nanguagua]
    """.strip()
    await catch_help_str.finish(Message(msg))
