import streamlit as st
from pdf_extractor import run_pdf_extractor
from json_extractor import run_json_extractor
from arcade_game import run_arcade_game

st.set_page_config(page_title="ITR Tool & Arcade Game", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation
if st.session_state.page == "home":
    st.title("🎯 Multi-Tool App")
    st.subheader("Choose an option below:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 ITR Extraction Tool", use_container_width=True):
            st.session_state.page = "itr"
    with col2:
        if st.button("🎮 Two-Player Arcade Game", use_container_width=True):
            st.session_state.page = "game"

elif st.session_state.page == "itr":
    st.button("⬅ Back", on_click=lambda: st.session_state.update(page="home"))
    st.header("📄 ITR Extraction Tool")
    option = st.radio("Select File Type", ["PDF", "JSON"], horizontal=True)
    if option == "PDF":
        run_pdf_extractor()
    else:
        run_json_extractor()

elif st.session_state.page == "game":
    st.button("⬅ Back", on_click=lambda: st.session_state.update(page="home"))
        run_arcade_game()
