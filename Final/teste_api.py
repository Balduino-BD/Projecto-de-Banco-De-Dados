from openai import OpenAI

client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Olá!"}]
)

print(resp.choices[0].message["content"])
