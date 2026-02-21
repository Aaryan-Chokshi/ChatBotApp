import streamlit as st
import time

# =================================================================
# BACKEND LOGIC TEMPLATE
# Replace this function with your actual AI model integration
# =================================================================

def get_bot_response(history, user_message, model):
    """
    This function contains the logic to generate a response.
    Currently, it uses simple rule-based logic.
    """
    try:
        from ollama import chat
        response = ""

        stream = chat(
            model=model,
            messages=[*history, {'role': 'user', 'content': f'{user_message}'}],
            stream=True
        )

        for chunk in stream:
            response += chunk.message.content

        return response
    except Exception as e:
        return f"Error: {e}"

# --- Page Configuration ---
st.set_page_config(
    page_title="Basic AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --- Initialize Session State ---
# This ensures chat history persists across user interactions
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar for Backend Logic Configuration ---
with st.sidebar:
    import ollama, json
    st.header("⚙️ Model selection")
    st.write("Select a model to initiate a conversation.")

    raw_model_data = json.loads(ollama.list().model_dump_json())
    raw_model_list = raw_model_data['models']

    cloud_models_list = []

    for model_data in raw_model_list:
        if model_data['model'].__contains__('cloud'):
            cloud_models_list.append(model_data['model'])
    
    # Simple logic switcher for the demo
    selected_model = st.radio(
        "Available cloud models (no self-hosted capacity right now, my M1 will kill me lol)",
        cloud_models_list,
        index=0
    )
    
    st.divider()
    st.subheader("About")
    st.write("A quick and dirty chatbot UI")
    st.write("Currently runs Ollama's cloud models. I'm a little tight on money :)")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Chat Interface ---
st.title("💬 ChatBot Interface")
st.write("Start a conversation below.")

# 1. Display Chat History
# We iterate through the stored messages to show the conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Accept User Input
prompt = st.chat_input("Type your message here...")

if prompt:
    # --- A. Add User Message to History ---
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display User Message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- B. Generate Backend Response (The Logic Section) ---
    # In a real app, you would send 'prompt' and 'st.session_state.messages' 
    # to your API (OpenAI, HuggingFace, etc.) here.
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Creates a placeholder for streaming
        full_response = ""

        # Simulate typing effect for visual feedback
        # NOTE: Replace the logic inside this block with your actual Model call
        bot_reply = get_bot_response(st.session_state.messages, prompt, selected_model)
        
        # Simulate streaming text
        # for chunk in bot_reply:
        #     full_response += chunk.message.content + " "
        #     # time.sleep(0.05) # Slow down for effect
        #     message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(bot_reply)

    # --- C. Save Assistant Response to History ---
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})


