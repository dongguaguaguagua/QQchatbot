import os
import base64
# import openai

# openai.organization = "org-WvMRPik8NGGoWxdJf9QPwpkh"
# openai.api_key = os.getenv("OPENAI_API_KEY")

# default_config = {
#     'api_key': '',
#     'enable_context': True,
#     'context': '',
#     # Creates a completion for the provided prompt and parameters
#     'completion': {
#         # ID of the model to use.
#         # You can use the List models API to see all of your available models,
#         # or see our Model overview for descriptions of them.
#         'model': 'text-davinci-003',
#         # The prompt(s) to generate completions for, encoded as a string,
#         # array of strings, array of tokens, or array of token arrays.
#         'prompt': '',
#         # What sampling temperature to use.
#         # Higher values means the model will take more risks.
#         # Try 0.9 for more creative applications,
#         # and 0 (argmax sampling) for ones with a well-defined answer.
#         # We generally recommend altering this or top_p but not both.
#         'temperature': 0.9,
#         # max_tokens is a parameter in the ChatGPT API that indicates the \
#         # maximum number of tokens (words) that should be generated \
#         # in the response. Increasing this number can make the response \
#         # longer and more detailed, but it can also make the model slower.
#         # The maximum number of tokens to generate in the completion.
#         'max_tokens': 1024,
#         # # An alternative to sampling with temperature, called nucleus sampling,
#         # # where the model considers the results of the tokens with top_p probability mass.
#         # # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
#         # # We generally recommend altering this or temperature but not both.
#         # 'top_p': 1,
#         # How many completions to generate for each prompt.
#         'n': 1,
#         # Whether to stream back partial progress.
#         # If set, tokens will be sent as data-only server-sent events as they b
#         # ecome available, with the stream terminated by a data: [DONE] message
#         'stream': False,
#         # Echo back the prompt in addition to the completion
#         'echo': False,
#         # The suffix that comes after a completion of inserted text.
#         'suffix': None,
#         # Up to 4 sequences where the API will stop generating further tokens.
#         # The returned text will not contain the stop sequence.
#         'stop': None,
#     },
#     # Given a prompt and an instruction,
#     # the model will return an edited version of the prompt.
#     'edit': {
#         # ID of the model to use.
#         # You can use the List models API to see all of your available models,
#         # or see our Model overview for descriptions of them.
#         'model': 'text-davinci-edit-001',
#         # The input text to use as a starting point for the edit.
#         'input': '',
#         # The instruction that tells the model how to edit the prompt.
#         'instruction': '',
#         # How many edits to generate for the input and instruction.
#         'n': 1,
#         # Defaults to 1, What sampling temperature to use.
#         # Higher values means the model will take more risks.
#         # Try 0.9 for more creative applications,
#         # and 0 (argmax sampling) for ones with a well-defined answer.
#         'temperature': 0.9,
#         # An alternative to sampling with temperature, called nucleus sampling,
#         # where the model considers the results of the tokens with top_p
#         # probability mass. So 0.1 means only the tokens comprising the top 10%
#         # probability mass are considered.
#         # # 'top_p' = 1,
#     },
#     'image': {

#     }
# }

# response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=["Say this is a test.",
#             "Please tell me how to create a new file in bash."],
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )

# response = response['choices'][0]['text']
# print(response)


# response = openai.Moderation.create(input=input("type something: "))
# print(response)
# response_content = response['results'][0]['categories']
# def check(dict):
#     # for key and value in dict:
#     for (key, value) in dict.items():
#         print(value)
#         # if value:
#         #     print(key)
#     print("Done")


# check(response_content)

# response = openai.Image.create(
#     prompt="a white siamese cat",
#     n=1,
#     response_format="b64_json",
#     size="512x512",
# )

# image_url = response['data'][0]['url']
# print(image_url)
# image_b64 = response['data'][0]['b64_json']
