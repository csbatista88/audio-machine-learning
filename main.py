# pip install -U openai gradio

import os, openai
import gradio as gr
# openai.api_key = 'sk-xxxxxx'



messages = [{"role": "system", "content": """Assistant is an expert candidate in
             technical IT job interviews. Currently, the interview is
             focused on a position for Platform Engineer. So, you have skills
             with Terraform, Kubernetes, Docker, Ansible, Python, AWS, and
             more. For technical code questions, use Python. Provide clear,
             short, and concise answers and code. 
             Answers should look human and avoid too much formality when replying.
             Always provide answers in English!"""}]

def transcribe(audio):
    global messages

    audio_filename_with_extension = audio + '.mp3'
    os.rename(audio, audio_filename_with_extension)

    audio_file = open(audio_filename_with_extension, "rb")
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language='en'
    )

    messages.append({"role": "user", "content": transcript})

    response = openai.chat.completions.create(model="gpt-4-1106-preview", messages=messages)

    message_role = response.choices[0].message.role
    message_content = response.choices[0].message.content
    messages.append({"role": message_role, "content": message_content})

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    return chat_transcript


ui = gr.Interface(fn=transcribe, inputs=gr.Audio(sources=["microphone"], type="filepath"), outputs="text").launch()
ui.launch()

