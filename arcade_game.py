import streamlit as st
import random

def run_arcade_game():
    st.subheader("🏓 Two Player Pong Game")

    # Initialize game state
    if "ball_x" not in st.session_state:
        reset_ball()
        st.session_state.paddle1_y = 100
        st.session_state.paddle2_y = 100
        st.session_state.score1 = 0
        st.session_state.score2 = 0

    # Auto refresh every 500ms
    st_autorefresh = st.experimental_rerun  # fallback if old Streamlit version
    st_autorefresh = getattr(st, "autorefresh", None)
    if st_autorefresh:
        st_autorefresh(interval=300, key="pong_refresh")

    # Paddle Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬆️ P1 Up"):
            st.session_state.paddle1_y = max(0, st.session_state.paddle1_y - 20)
        if st.button("⬇️ P1 Down"):
            st.session_state.paddle1_y = min(240, st.session_state.paddle1_y + 20)

    with col2:
        if st.button("⬆️ P2 Up"):
            st.session_state.paddle2_y = max(0, st.session_state.paddle2_y - 20)
        if st.button("⬇️ P2 Down"):
            st.session_state.paddle2_y = min(240, st.session_state.paddle2_y + 20)

    # Move ball
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    # Bounce on top/bottom walls
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= 300:
        st.session_state.ball_dy *= -1

    # Bounce on paddles
    if (st.session_state.ball_x <= 20 and 
        st.session_state.paddle1_y <= st.session_state.ball_y <= st.session_state.paddle1_y + 60):
        st.session_state.ball_dx *= -1
    if (st.session_state.ball_x >= 470 and 
        st.session_state.paddle2_y <= st.session_state.ball_y <= st.session_state.paddle2_y + 60):
        st.session_state.ball_dx *= -1

    # Scoring
    if st.session_state.ball_x < 0:
        st.session_state.score2 += 1
        reset_ball()
    if st.session_state.ball_x > 500:
        st.session_state.score1 += 1
        reset_ball()

    # Show scores
    st.write(f"**Score:** Player 1 - {st.session_state.score1} | Player 2 - {st.session_state.score2}")

    # Draw game
    st.markdown(
        f"""
        <svg width="500" height="300" style="border:2px solid black; background:#f0f0f0">
            <!-- Paddles -->
            <rect x="10" y="{st.session_state.paddle1_y}" width="10" height="60" fill="blue"/>
            <rect x="480" y="{st.session_state.paddle2_y}" width="10" height="60" fill="red"/>
            
            <!-- Ball -->
            <circle cx="{st.session_state.ball_x}" cy="{st.session_state.ball_y}" r="8" fill="green"/>
        </svg>
        """,
        unsafe_allow_html=True
    )

def reset_ball():
    st.session_state.ball_x = 250
    st.session_state.ball_y = 150
    st.session_state.ball_dx = random.choice([-3, 3])
    st.session_state.ball_dy = random.choice([-3, 3])
