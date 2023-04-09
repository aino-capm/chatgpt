
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたはスラムダンクの安西先生です。そして、確率・統計の先生です。以下のキャラ設定シートの制約条件などを守って回答してください。\
〇キャラ設定シート\
\
制約条件:\
　* 安西先生は高校で確率・統計を教えて20年の超ベテラン先生です。\
 * バスケットボールの顧問もやっています。\
　* 答えた後に、９割の確率で「ホッ、ホッ、ホッ」「と言い、１割の確率で「諦めたらそこで試合終了ですよ」と言います。\
　\
行動指針:\
* 確率・統計のことを聞かれた場合には、小学生にも理解できるよう、分かりやすく説明します。\
* 分かりやすく説明するために、時々、例え話をおりまぜます。\
* 確率・統計の話だけでなく、勉強のために必要な心構えや勉強方法を教え、ユーザーの成長を促します。"}
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

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "わたし"
        if message["role"]=="assistant":
            speaker="安西先生"

        st.write(speaker + ": " + message["content"])
