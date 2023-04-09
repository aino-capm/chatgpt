
import streamlit as st
import openai
import os
from PIL import Image

st.markdown("&nbsp;")

img = Image.open("img01.jpeg")
st.image(img,width=400)


# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは確率・統計の先生です。文末に、ホッ、ホッ、ホッ　とつけます。回答は、中学生にも理解できるぐらい分かりやすく行います。\
        回答の最後に、諦めたらそこで試合終了ですよとつけます。"}
        ] 

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("教えて！安西先生")
st.write("スラムダンクの安西先生が確率・統計のことを教えてくれます。")

user_input = st.text_input("質問をを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "わたし😊"
        if message["role"]=="assistant":
            speaker="安西先生🏀"

        st.write(speaker + ": " + message["content"])
