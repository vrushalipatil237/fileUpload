# arcade_game.py
import random
import streamlit as st
import streamlit.components.v1 as components

W, H = 500, 300
PADDLE_W, PADDLE_H = 10, 60
BALL_R = 8

def _init_state():
    ss = st.session_state
    ss.setdefault("left_paddle", 120)
    ss.setdefault("right_paddle", 120)
    ss.setdefault("ball_x", W // 2)
    ss.setdefault("ball_y", H // 2)
    ss.setdefault("ball_dx", random.choice([-3, 3]))
    ss.setdefault("ball_dy", random.choice([-3, 3]))
    ss.setdefault("score1", 0)
    ss.setdefault("score2", 0)

def _clamp(v, lo, hi):
    return max(lo, min(hi, v))

def _reset_ball():
    st.session_state.ball_x = W // 2
    st.session_state.ball_y = H // 2
    st.session_state.ball_dx = random.choice([-3, 3])
    st.session_state.ball_dy = random.choice([-3, 3])

def _step_physics():
    ss = st.session_state
    ss.ball_x += ss.ball_dx
    ss.ball_y += ss.ball_dy

    if ss.ball_y - BALL_R <= 0 or ss.ball_y + BALL_R >= H:
        ss.ball_dy *= -1

    if (ss.ball_x - BALL_R <= 10 + PADDLE_W and
        ss.left_paddle <= ss.ball_y <= ss.left_paddle + PADDLE_H):
        ss.ball_dx *= -1
        ss.ball_x = 10 + PADDLE_W + BALL_R

    if (ss.ball_x + BALL_R >= 480 and
        ss.right_paddle <= ss.ball_y <= ss.right_paddle + PADDLE_H):
        ss.ball_dx *= -1
        ss.ball_x = 480 - BALL_R

    if ss.ball_x < -BALL_R:
        ss.score2 += 1
        _reset_ball()
    if ss.ball_x > W + BALL_R:
        ss.score1 += 1
        _reset_ball()

def _render_svg():
    ss = st.session_state
    svg = f"""
    <svg width="{W}" height="{H}" style="background:#f5f7ff; border:2px solid #000; border-radius:6px;">
        <!-- Midline -->
        <line x1="{W/2}" y1="0" x2="{W/2}" y2="{H}" stroke="#bbb" stroke-dasharray="6,6" />
        <!-- Left Paddle -->
        <rect x="10" y="{ss.left_paddle}" width="{PADDLE_W}" height="{PADDLE_H}" fill="#1976d2"/>
        <!-- Right Paddle -->
        <rect x="480" y="{ss.right_paddle}" width="{PADDLE_W}" height="{PADDLE_H}" fill="#d32f2f"/>
        <!-- Ball -->
        <circle cx="{ss.ball_x}" cy="{ss.ball_y}" r="{BALL_R}" fill="#111"/>
    </svg>
    """
    components.html(svg, height=H+50, scrolling=False)

def run_arcade_game():
    _init_state()

    st.title("🏓 Two Player Pong (Streamlit)")
    st.write(f"**Score** — Left: {st.session_state.score1} | Right: {st.session_state.score2}")

    colL, colR = st.columns(2)
    with colL:
        if st.button("⬆️ Left Up"):
            st.session_state.left_paddle = _clamp(st.session_state.left_paddle - 20, 0, H - PADDLE_H)
        if st.button("⬇️ Left Down"):
            st.session_state.left_paddle = _clamp(st.session_state.left_paddle + 20, 0, H - PADDLE_H)

    with colR:
        if st.button("⬆️ Right Up"):
            st.session_state.right_paddle = _clamp(st.session_state.right_paddle - 20, 0, H - PADDLE_H)
        if st.button("⬇️ Right Down"):
            st.session_state.right_paddle = _clamp(st.session_state.right_paddle + 20, 0, H - PADDLE_H)

    _step_physics()
    _render_svg()

    if st.button("▶ Next Frame"):
        _step_physics()
        _render_svg()

    if st.button("⬅ Back to Application"):
        st.session_state.page = "application"
