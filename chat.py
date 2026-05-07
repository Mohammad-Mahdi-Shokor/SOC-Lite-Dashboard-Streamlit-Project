import streamlit as st
from yourHelper import getDeepseekResponse, load_policy_text

def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0


def render_policy():
    policy = load_policy_text()
    with st.expander("AI Response Policy (click to view)"):
        st.markdown(policy)


def render_chat():
    st.title("Chat with the Assistant")
    # render_policy()

    for msg in st.session_state.messages:
        role, text = msg[0], msg[1]
        # `st.chat_message` requires a `name` argument (e.g. 'user' or 'assistant')
        with st.chat_message(name=role):
            # show text; optionally add simple prefixes for clarity
            if role == "user":
                st.markdown(f"**You:** {text}")
            else:
                st.markdown(f"**Assistant:** {text}")

    # Use a dynamic key for the text input so we can 'clear' it by
    # incrementing `input_key` after sending. This avoids calling
    # `st.experimental_rerun()` which may be unavailable in some Streamlit versions.
    input_key = f"user_input_{st.session_state.input_key}"
    # Use Streamlit's chat-style input widget. It returns a string when the
    # user presses Enter. We handle the returned value immediately.
    user_input = st.chat_input(placeholder="Type your message and press Enter", key=input_key)

    if user_input:
        user_msg = user_input.strip()
        if user_msg:
            st.session_state.messages.append(("user", user_msg))
            with st.spinner("Assistant is typing..."):
                resp = getDeepseekResponse(user_msg)
            st.session_state.messages.append(("assistant", resp))
            # increment the input key so next render shows an empty field
            st.session_state.input_key += 1

    # Clear button to reset the conversation
    if st.button("Clear"):
        st.session_state.messages = []
        st.session_state.input_key += 1


if __name__ == "__main__":
    init_chat_state()
    render_chat()
