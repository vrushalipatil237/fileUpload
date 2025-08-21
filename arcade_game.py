import streamlit as st

def run_arcade_game():
    # Initialize state only once
    if "left_paddle" not in st.session_state:
        st.session_state.left_paddle = 120
    if "right_paddle" not in st.session_state:
        st.session_state.right_paddle = 120
    if "ball_x" not in st.session_state:
        st.session_state.ball_x = 250
    if "ball_y" not in st.session_state:
        st.session_state.ball_y = 150
    if "ball_dx" not in st.session_state:
        st.session_state.ball_dx = 3
    if "ball_dy" not in st.session_state:
        st.session_state.ball_dy = 3

    st.title("🏓 Two Player Pong Game")

    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬆️ Left Up"):
            st.session_state.left_paddle = max(0, st.session_state.left_paddle - 20)
        if st.button("⬇️ Left Down"):
            st.session_state.left_paddle = min(240, st.session_state.left_paddle + 20)

    with col2:
        if st.button("⬆️ Right Up"):
            st.session_state.right_paddle = max(0, st.session_state.right_paddle - 20)
        if st.button("⬇️ Right Down"):
            st.session_state.right_paddle = min(240, st.session_state.right_paddle + 20)

    # Move ball
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    # Bounce top/bottom
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= 300:
        st.session_state.ball_dy *= -1

    # Bounce left/right
    if st.session_state.ball_x <= 20 and st.session_state.left_paddle <= st.session_state.ball_y <= st.session_state.left_paddle + 60:
        st.session_state.ball_dx *= -1
    if st.session_state.ball_x >= 470 and st.session_state.right_paddle <= st.session_state.ball_y <= st.session_state.right_paddle + 60:
        st.session_state.ball_dx *= -1

    # Reset if out
    if st.session_state.ball_x < 0 or st.session_state.ball_x > 500:
        st.session_state.ball_x, st.session_state.ball_y = 250, 150

    # Render SVG
    st.markdown(f"""
    <svg width="500" height="300" style="background-color: lightblue; border: 2px solid black;">
        <!-- Left Paddle -->
        <rect x="10" y="{st.session_state.left_paddle}" width="10" height="60" fill="blue"/>
        
        <!-- Right Paddle -->
        <rect x="480" y="{st.session_state.right_paddle}" width="10" height="60" fill="red"/>
        
        <!-- Ball -->
        <circle cx="{st.session_state.ball_x}" cy="{st.session_state.ball_y}" r="8" fill="black"/>
    </svg>
    """, unsafe_allow_html=True)
