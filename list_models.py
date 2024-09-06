from openai import OpenAI

client = OpenAI(api_key='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')


# List available models
models = client.models.list()

# Print available models
for model in models.data:
    print(model['id'])