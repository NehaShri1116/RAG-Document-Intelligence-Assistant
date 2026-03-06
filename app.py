import streamlit as st
import uuid
from src.ingest import process_pdf
from src.vector_store import create_store
from src.rag_chain import build_chain

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Neha's RAG Assistant",
    layout="wide"
)

# ------------------------------
# Dark Theme
# ------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0f172a;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

button {
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Session State Setup
# ------------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.sessions[chat_id] = {
        "messages": [],
        "chain": None,
        "name": "New Chat"
    }

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:

    st.image("puppy.svg", width=36)

    if st.button("New Chat", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.sessions[chat_id] = {
            "messages": [],
            "chain": None,
            "name": "New Chat"
        }
        st.rerun()

    st.divider()

    for chat_id, chat_data in list(st.session_state.sessions.items()):

        col_main, col_edit, col_delete = st.columns([7,1,1])

        # Select Chat
        with col_main:
            if st.button(
                chat_data["name"],
                key=f"select_{chat_id}",
                use_container_width=True
            ):
                st.session_state.current_chat = chat_id
                st.rerun()

        # Rename
        with col_edit:
            if st.button("✎", key=f"rename_{chat_id}"):
                st.session_state["rename_target"] = chat_id

        # Delete
        with col_delete:
            if st.button("🗑", key=f"delete_{chat_id}"):
                del st.session_state.sessions[chat_id]

                if chat_id == st.session_state.current_chat:
                    if st.session_state.sessions:
                        st.session_state.current_chat = list(st.session_state.sessions.keys())[0]
                    else:
                        new_id = str(uuid.uuid4())
                        st.session_state.current_chat = new_id
                        st.session_state.sessions[new_id] = {
                            "messages": [],
                            "chain": None,
                            "name": "New Chat"
                        }

                st.rerun()

    # Rename Input
    if "rename_target" in st.session_state:
        target = st.session_state["rename_target"]
        new_name = st.text_input(
            "Rename chat",
            value=st.session_state.sessions[target]["name"]
        )
        if st.button("Save"):
            st.session_state.sessions[target]["name"] = new_name
            del st.session_state["rename_target"]
            st.rerun()

# ------------------------------
# Header
# ------------------------------
col_icon, col_title = st.columns([1, 12])

with col_icon:
    st.image("puppy.svg", width=45)

with col_title:
    st.markdown("## Neha's Production RAG Assistant")

current = st.session_state.sessions[st.session_state.current_chat]

# ------------------------------
# Chat Messages (ABOVE)
# ------------------------------
chat_container = st.container()

with chat_container:
    for msg in current["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ------------------------------
# Bottom Input Area
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)

input_col, upload_col = st.columns([6,1])

with input_col:
    prompt = st.chat_input("Ask about the document...")

with upload_col:
    uploaded_file = st.file_uploader(
        "",
        type="pdf",
        label_visibility="collapsed"
    )

# ------------------------------
# Handle Upload
# ------------------------------
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    docs = process_pdf("temp.pdf")
    create_store(docs)
    current["chain"] = build_chain()

    st.success("Document uploaded & chat initialized.")

# ------------------------------
# Handle Prompt
# ------------------------------
if prompt:
    current["messages"].append({
        "role": "user",
        "content": prompt
    })

    if current["name"] == "New Chat":
        current["name"] = prompt[:25]

    with st.chat_message("assistant"):
        if current["chain"] is None:
            st.warning("Upload a document first.")
        else:
            with st.spinner("Thinking..."):
                answer = current["chain"].invoke(prompt)
                st.write(answer)

            current["messages"].append({
                "role": "assistant",
                "content": answer
            })

    st.rerun()