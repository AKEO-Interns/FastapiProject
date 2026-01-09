import openai

# Set your OpenAI API key
openai.api_key = "YOUR_SECRET_KEY"  # replace with your actual key

#  Your input prompt
prompt = "What is Gen AI?"

#  Call the model (ChatCompletion API)
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,  # limit output length
    temperature=0.7  # creativity of output
)

#  Get the generated answer
output_text = response['choices'][0]['message']['content']

#  Print output
print("Input Prompt:", prompt)
print("Model Output:", output_text)
