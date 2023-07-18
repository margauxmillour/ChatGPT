import openai
import subprocess


nb_itteration = 15

openai.api_key = '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'

def chat_with_gpt(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )

    # Extract the code portion from the response
    chat_result = response['choices'][0]['message']['content']
    code_start = chat_result.find("python")
    if code_start != -1:
        code_start += len("# CODE:")
        code_end = chat_result.find("```", code_start)
        code = chat_result[code_start:code_end].strip()
        return code

    return chat_result

def save_code(code,number):
    # Save the code to a file
    with open(f'code/code_{number}.py', 'w') as file:
        file.write(code)



prompt = "Create a Flappy Bird game using Pygame. The game should have the following features:\n"
prompt += "- The game window should be 288x512 pixels in size.\n"
prompt += "- The background, bird, base, pipe and highscore should be loaded from the assets folder and displayed on the screen.\n"
prompt += "- The bird should be able to flap when the spacebar is pressed.\n"
prompt += "- Pipes should spawn at regular intervals and move from right to left.\n"
prompt += "- The bird should be able to collide with the pipes, the top of the screen and the base.\n"
prompt += "- The score should increase when the bird successfully passes a pair of pipes.\n"
prompt += "- The game should end when the bird collides with an obstacle.\n"
prompt += "- The highest score achieved should be displayed on the screen, along with the option to restart the game.\n"
prompt += "Please provide the necessary code to implement the above features using the Pygame library."

print("starting process")
for i in range(0,nb_itteration):
    response = chat_with_gpt(prompt)
    save_code(response,i)
    print(f'{i+1}/{nb_itteration}')

print("end of process")
