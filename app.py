import gradio as gr
import os
import time
from chat import chat
from mnist import image_classification
from search import search
from tts import text2audio

messages = []
current_file_text = None
image = ''

def add_text(history, text):
    global messages
    if text.startswith("/search "):
        search_query = text[len("/search "):]
        search_result = search(search_query)
        messages.append({"role": "user", "content": search_result})
    else:
        messages.append({"role": "user", "content": text})
    # messages.append({"role": "user", "content": text})

    history = history + [(text, None)]
    
    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    global messages
    global image
    history = history + [((file.name,), None)]
    if file.name.endswith(".png"):
        messages.append({"role": "user", "content": f"Please classify {file.name}"})
        image = file
    else:
        messages.append({"role": "user", "content": f"File uploaded: {file.name}"})
    
    return history

def bot(history):
    global messages
    global image
    
    response_text = ""

    # 检验是否是音频文件
    if messages[-1]["role"] == "user" and messages[-1]["content"].startswith("/audio "):
        for chunk in chat(messages):
            response_text += chunk
        audio_path = text2audio(response_text)
        if audio_path:
            history[-1][1] = (audio_path, )
            yield history
    # 检查是否是图像识别
    if messages[-1]["role"] == "user" and messages[-1]["content"].startswith("Please classify "):
        result = image_classification(file=image)
        image = ''
        history[-1][1] = result
        yield history
    else:
        for chunk in chat(messages):
            response_text += chunk
            history[-1][1] = response_text
            yield history

    messages.append({"role": "assistant", "content": response_text})

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
