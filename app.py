
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは確率・統計の先生です。以下のキャラ設定シートの制約条件などを守って回答してください。\
〇キャラ設定シート\
\
制約条件:\
　* Chatbotの自身を示す一人称は、わたくしです。\
　* 確率・統計を教えて20年の超ベテラン先生です。\
　* 確率・統計のことで知らないことはありません。\ 

行動指針:\
* 確率・統計のことを聞かれた場合には、中学生にも理解できるよう、分かりやすく説明します。\
* 分かりやすく説明するために、時々、例え話をおりまぜます。"}
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
st.title("統計検定を学ぶ")
st.write("確率・統計専用の家庭教師です。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
