import streamlit as st
import streamlit.components.v1 as components
import html
import os
from pathlib import Path

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path, encoding="utf-8") as f:  # 👈 force UTF-8
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_global_styles()


DEFAULT_CSS = """
/* Scoped to the pipeline root so it doesn't leak if you change approach */


"""

def render_olympics_fixtures():
    st.title("🏅 Olympics — Events Sequence")
    st.caption("Follow the sequence — each card shows Event, Task, and Next action.")

    events = [
        {"name": "Dilwale Lunges Le Jayenge",
         "task": "Player performs 15 lunges (each leg) while holding a rose and reciting a Bollywood dialogue at the last lunge (e.g., “Bade bade deshon mein…”). Lunges must be dramatic, with arms outstretched like Shah Rukh Khan.",
         "next": "Tags the next player by passing the rose."},
        {"name": "Hum Saath Saath Hain Race",
         "task": "Player pairs with a teammate, ties their legs together with a rakhi-style bracelet (Gym band), and races a set distance.",
         "next": "Tags the next player by tying a handkerchief on their wrist, saying “Hum saath saath hain!”"},
        {"name": "Sholay Ka Sikka",
         "task": "Player uses the provided coin and does 20 flips while catching the coin. For every head, 3 seconds will be reduced from your time (max reduction: 60 seconds).",
         "next": "Tags the next player with a gunfinger salute, saying “Arre o Sambha!”"},
        {"name": "Goalmaal",
         "task": "Player kicks 3 footballs at targets with Golmaal characters with multipliers (1x = 1 second, 2x = 5 seconds, 3x = 10 seconds). Each hit reduces the team’s time (max 30 seconds).",
         "next": "Tags the next player by providing the hockey stick and saying “Dhan Dhana Dhan Goal”"},
        {"name": "Chake De TCoE",
         "task": "Player shoots 3 tennis balls with a hockey stick such that the ball reaches the multipliers (1s, 5s, 10s). Each hit reduces the team’s time (max 30 seconds).",
         "next": "Tags the next player saying “Chak De TCOE!”"},
        {"name": "Ae Cup Hai Mushkil",
         "task": "There are 5 cups lined up. Player picks each cup one by one and nests them (put one inside the other). After bringing each cup the player says a movie name with the team's mascot hero.",
         "next": "Tags the next player by handing over the cup with a heroic pose."},
        {"name": "Kaho Na Tennis Hai",
         "task": "Player is given a tennis racquet and ball; they must bounce it 50 times while saying a tongue twister single-handedly.",
         "next": "Tags the next player by saying the tongue twister one last time."},
        {"name": "Baahubali Ring Toss",
         "task": "Player tosses 5 rings onto poles marked with multipliers (2s, 4s, 6s). Each hit reduces the team’s time (max 30s).",
         "next": "Player finishes with a regal “Jai Mahishmati!” salute."},
    ]

    def position_for_index(i):
        r = i % 4
        return "right" if r == 0 or r == 3 else "left"

    # Try to read your project's assets/style.css (works if app root contains assets/style.css)
    css_text = ""
    try:
        project_root = Path(__file__).resolve().parent.parent
        css_path = project_root / "assets" / "style.css"
        if css_path.exists():
            css_text = css_path.read_text(encoding="utf-8")
        else:
            css_text = DEFAULT_CSS
    except Exception:
        css_text = DEFAULT_CSS

    # Build HTML
    html_parts = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        "<style>",
        css_text,
        "</style>",
        "</head><body>",
        '<div class="olympics-pipeline-root">',
        '<div class="pipeline" role="list">'
    ]

    for idx, ev in enumerate(events):
        pos = position_for_index(idx)
        title = html.escape(ev["name"])
        task = html.escape(ev["task"])
        nxt = html.escape(ev["next"])

        card_html = f"""
        <div class="stage {pos}" role="listitem">
            <div class="card">
                <div class="card-head">
                    <span class="stage-num">Event {idx+1}</span>
                    <h3 class="card-title">{title}</h3>
                </div>
                <div class="card-body">
                    <div class="card-sep" aria-hidden="true"></div>
                    <p class="task"><strong>Task:</strong> {task}</p>

                    <div class="card-sep" aria-hidden="true"></div>
                    <p class="next"><strong>Next:</strong> {nxt}</p>
                </div>
            </div>
            
        </div>
        """

        html_parts.append(card_html)

    html_parts.append("</div></div></body></html>")
    full_html = "\n".join(html_parts)

    # Heuristic height: 150px per stage but clamp to reasonable range
    height = min(max(400, 150 * len(events)), 2400)

    # Render inside an iframe (components.html) with the embedded CSS
    components.html(full_html, height=height, scrolling=True)