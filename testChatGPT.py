import openai

openai.organization = "org-WvMRPik8NGGoWxdJf9QPwpkh"
openai.api_key = "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"

default_config = {
    'preset': '',
    'api_key': '',
    'enable_context': True,
    'context': '',
    'openai': {
        'model': 'text-davinci-003',
        'temperature': 0.9,
        'max_tokens': 1024,
        'top_p': 1,
        'echo': False,
        'presence_penalty': 0,
        'frequency_penalty': 0,
    }
}

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=["Say this is a test.",
            "Please tell me how to create a new file in bash."],
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)['choices'][0]['text'].strip()

# response = openai.Completion.create(
#     **default_config["openai"], prompt="Say this is a test.")
print(response)
