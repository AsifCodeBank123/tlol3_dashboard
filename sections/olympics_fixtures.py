# sections/olympics_fixtures.py
"""
Render the Olympics events pipeline as an HTML blob inside an iframe (components.html).
Features:
 - Renders a vertical pipeline of event cards (alternating left/right positions).
 - Shows Event name, Task, Next, decorative separators.
 - Loads images for each event:
     * If EVENTS_IMAGES (from utils.constants) is present it will be used.
     * If a local file is found under your project 'assets' folder it will be embedded as a data URI
       (this avoids Streamlit static serving quirks and MediaFileStorageError).
     * If the mapping contains an http(s) URL, it will be used directly.
 - CSS is embedded into the HTML so styles apply inside the iframe.
"""

import streamlit as st
import streamlit.components.v1 as components
import html
from pathlib import Path
import mimetypes
import base64
import re
from urllib.parse import quote

# Optional: import user-defined EVENTS_IMAGES mapping if present
try:
    from utils.constants import EVENTS_IMAGES as USER_EVENTS_IMAGES  # noqa: F401
except Exception:
    USER_EVENTS_IMAGES = {}

# Fallback hard-coded image map (relative to assets/)
EVENTS_IMAGES = dict(USER_EVENTS_IMAGES) if isinstance(USER_EVENTS_IMAGES, dict) else {}
EVENTS_IMAGES.setdefault("Event 1", "olympics/lunges.png")
# you can expand these defaults or replace EVENTS_IMAGES with your own mapping in utils/constants.py

# ----- Helpers -----
def _slug(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    s = s.replace("’", "").replace("'", "").replace('"', "").replace("—", " ").replace("–", " ")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def file_to_data_uri(local_path: str):
    """
    Convert a local path (relative to project root 'assets' folder or absolute) to a data URI.
    Returns None if file not found.
    """
    if not local_path:
        return None

    p = Path(local_path)
    # If given a simple relative path like "olympics/lunges.png", assume assets/olympics/...
    if not p.is_absolute():
        candidate = Path.cwd() / "assets" / str(local_path).lstrip("/").lstrip("assets/").lstrip("/")
    else:
        candidate = p

    if not candidate.exists():
        # Try a second chance: sometimes constants include "TLOL_Dash/assets/..." style paths
        alt = Path(local_path.replace("\\", "/"))
        if not alt.is_absolute():
            alt = Path.cwd() / alt
        if alt.exists():
            candidate = alt
        else:
            return None

    mime, _ = mimetypes.guess_type(str(candidate))
    mime = mime or "application/octet-stream"
    data = candidate.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

def resolve_image_for_event(idx: int, ev_name: str):
    """
    Resolve image source for an event. Returns:
      - an http(s) URL (string), OR
      - a data: URI string (if local file found), OR
      - a server path '/assets/...' (last-resort), OR
      - None if nothing found.
    Order of attempts:
      1) EVENTS_IMAGES['Event N']
      2) EVENTS_IMAGES[full event name]
      3) EVENTS_IMAGES[slugified name]
      4) Try to embed local file into data URI if value looks local
    """
    key1 = f"Event {idx+1}"
    raw = EVENTS_IMAGES.get(key1) or EVENTS_IMAGES.get(ev_name) or EVENTS_IMAGES.get(_slug(ev_name))
    if not raw:
        return None
    raw_s = str(raw).strip()

    # If already http(s) or data:, return as-is
    if raw_s.startswith(("http://", "https://", "data:")):
        return raw_s

    # If already a leading slash path, return as-is (may work in some deployments)
    if raw_s.startswith("/"):
        return raw_s

    # Try to find local file and convert to data-uri (preferred for iframe)
    data_uri = file_to_data_uri(raw_s)
    if data_uri:
        return data_uri

    # Last-ditch: try to return a server-served assets path (may or may not work)
    s = raw_s.replace("\\", "/")
    if not s.startswith("assets/"):
        s = "assets/" + s.lstrip("/")
    return "/" + quote(s)

# ----- Embedded CSS (scoped under .olympics-pipeline-root) -----
DEFAULT_CSS = """
.olympics-pipeline-root .pipeline { position: relative; width: 100%; max-width: 1100px; margin: 16px auto 48px; padding: 24px 12px; }
.olympics-pipeline-root .pipeline::before { content: ""; position: absolute; left: 50%; transform: translateX(-50%); top: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, rgba(255,204,0,0.95), rgba(255,140,0,0.95)); border-radius: 4px; z-index: 1; box-shadow: 0 0 12px rgba(255,180,0,0.12); }
.olympics-pipeline-root .stage { position: relative; width: 50%; padding: 18px 24px; box-sizing: border-box; z-index: 2; display: flex; align-items: center; }
.olympics-pipeline-root .card { display: flex; flex-direction: column; align-items: stretch; gap: 12px; background: linear-gradient(180deg,#ffffff,#fffaf0); border-radius: 12px; padding: 14px 16px; box-shadow: 0 6px 18px rgba(16,24,40,0.08); border: 1px solid rgba(0,0,0,0.04); width: calc(100% - 40px); box-sizing: border-box; }
.olympics-pipeline-root .card-content { width: 100%; min-width: 0; }
.olympics-pipeline-root .stage.left .card-content { text-align: right; }
.olympics-pipeline-root .stage.right .card-content { text-align: left; }
.olympics-pipeline-root .card-head { display: flex; align-items: baseline; gap: 12px; }
.olympics-pipeline-root .stage-num { display:inline-block; background:#ffcc00; color:#222; padding:6px 10px; border-radius:999px; font-weight:700; font-size:0.82rem; box-shadow:0 2px 8px rgba(255,170,0,0.15); }
.olympics-pipeline-root .card-title { margin:0; font-size:1.05rem; line-height:1.1; color:#222; }
.olympics-pipeline-root .card-body { margin-top:8px; font-size:0.92rem; color:#333; }
.olympics-pipeline-root .card-body p { margin:6px 0; }
.olympics-pipeline-root .card-sep { height:6px; margin:10px 0; border-radius:6px; background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,204,0,0.95) 45%, rgba(255,140,0,0.95) 55%, rgba(255,255,255,0) 100%); box-shadow:0 2px 6px rgba(255,170,0,0.06); opacity:0.95; }

/* Image / media box centered under content */
.olympics-pipeline-root .card-media { width:300px; height:300px; border-radius:10px; padding:8px; overflow:hidden; margin:8px auto 0; background:linear-gradient(180deg,#f7f7f7,#ffffff); display:flex; align-items:center; justify-content:center; border:1px solid rgba(0,0,0,0.06); box-shadow:0 6px 18px rgba(16,24,40,0.06); transition:box-shadow .2s ease, transform .18s ease; }
.olympics-pipeline-root .card-media img { width:100%; height:100%; object-fit:cover; display:block; transform-origin:center center; transition:transform .25s ease; }
.olympics-pipeline-root .media-placeholder { width:60%; height:60%; border-radius:6px; background: repeating-linear-gradient(45deg, rgba(0,0,0,0.03) 0 4px, rgba(0,0,0,0.01) 4px 8px); box-shadow: inset 0 1px 0 rgba(255,255,255,0.6); }

.olympics-pipeline-root .connector { width:24px; height:24px; border-radius:50%; background:#ffcc00; box-shadow:0 3px 10px rgba(255,170,0,0.18); display:inline-block; }
.olympics-pipeline-root .stage.left { left:0; text-align:right; justify-content:flex-end; }
.olympics-pipeline-root .stage.left .card { margin-right:28px; }
.olympics-pipeline-root .stage.left .connector { margin-left:8px; transform:translateX(12px); }
.olympics-pipeline-root .stage.right { left:50%; text-align:left; justify-content:flex-start; }
.olympics-pipeline-root .stage.right .card { margin-left:28px; }
.olympics-pipeline-root .stage.right .connector { margin-right:8px; transform:translateX(-12px); }
.olympics-pipeline-root .stage { display:flex; align-items:center; min-height:110px; }
.olympics-pipeline-root .stage + .stage { margin-top:18px; }

@media (max-width:880px) {
  .olympics-pipeline-root .pipeline::before { left:6px; transform:none; width:3px; }
  .olympics-pipeline-root .stage { width:100%; padding-left:40px; }
  .olympics-pipeline-root .stage.left, .olympics-pipeline-root .stage.right { left:0; text-align:left; justify-content:flex-start; }
  .olympics-pipeline-root .stage.left .card, .olympics-pipeline-root .stage.right .card { margin:0 12px; width:calc(100% - 64px); }
  .olympics-pipeline-root .stage .connector { position:absolute; left:12px; transform:none; }
  .olympics-pipeline-root .card-media { width:76px; height:76px; margin-top:10px; }
}
"""

# ----- events list (same order/contents you provided) -----
EVENTS = [
    {
        "name": "Dilwale Lunges Le Jayenge",
        "task": (
            "Player performs 15 lunges (each leg) while holding a rose and reciting a Bollywood dialogue "
            "at the last lunge (e.g., “Bade bade deshon mein…”). Lunges must be dramatic, with arms "
            "outstretched like Shah Rukh Khan."
        ),
        "next": "Tags the next player by passing the rose."
    },
    {
        "name": "Hum Saath Saath Hain Race",
        "task": (
            "Player pairs with a teammate, ties their legs together with a rakhi-style bracelet (Gym band), "
            "and races a set distance."
        ),
        "next": "Tags the next player by tying a handkerchief on their wrist, saying “Hum saath saath hain!”"
    },
    {
        "name": "Sholay Ka Sikka",
        "task": (
            "Player uses the provided coin and does 20 flips while catching the coin. For every head, "
            "3 seconds will be reduced from your time (max reduction: 60 seconds)."
        ),
        "next": "Tags the next player with a gunfinger salute, saying “Arre o Sambha!”"
    },
    {
        "name": "Goalmaal",
        "task": (
            "Player kicks 3 footballs at targets with Golmaal characters with multipliers (1x = 1 second, 2x = 5 seconds, "
            "3x = 10 seconds). Each hit reduces the team’s time (max 30 seconds)."
        ),
        "next": "Tags the next player by providing the hockey stick and saying “Dhan Dhana Dhan Goal”"
    },
    {
        "name": "Chake De TCoE",
        "task": (
            "Player shoots 3 tennis balls with a hockey stick such that the ball reaches the multipliers (1s, 5s, 10s). "
            "Each hit reduces the team’s time (max 30 seconds)."
        ),
        "next": "Tags the next player saying “Chak De TCOE!”"
    },
    {
        "name": "Ae Cup Hai Mushkil",
        "task": (
            "There are 5 cups lined up. Player picks each cup one by one and nests them (put one inside the other). "
            "After bringing each cup the player says a movie name with the team's mascot hero."
        ),
        "next": "Tags the next player by handing over the cup with a heroic pose."
    },
    {
        "name": "Kaho Na Tennis Hai",
        "task": (
            "Player is given a tennis racquet and ball; they must bounce it 50 times while saying a tongue twister single-handedly."
        ),
        "next": "Tags the next player by saying the tongue twister one last time."
    },
    {
        "name": "Baahubali Ring Toss",
        "task": (
            "Player tosses 5 rings onto poles marked with multipliers (2s, 4s, 6s). Each hit reduces the team’s time (max 30s)."
        ),
        "next": "Player finishes with a regal “Jai Mahishmati!” salute."
    },
]

# ----- Main render function -----
def render_olympics_fixtures():
    st.title("🏅 Olympics — Events Sequence")
    st.caption("Follow the sequence — each card shows Event, Task, Next action and an image.")

    def position_for_index(i):
        r = i % 4
        return "right" if r == 0 or r == 3 else "left"

    # Build HTML
    html_parts = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        "<style>",
        DEFAULT_CSS,
        "</style>",
        "</head><body>",
        '<div class="olympics-pipeline-root">',
        '<div class="pipeline" role="list">'
    ]

    for idx, ev in enumerate(EVENTS):
        pos = position_for_index(idx)
        title = html.escape(ev["name"])
        task = html.escape(ev["task"])
        nxt = html.escape(ev["next"])

        # resolve image (may return data: URI or http(s) or /assets/..)
        resolved_src = resolve_image_for_event(idx, ev["name"])

        if resolved_src:
            safe_src = html.escape(resolved_src, quote=True)
            img_html = f'''
            <div class="card-media" aria-hidden="true">
                <img src="{safe_src}" alt="{title} image" />
            </div>
            '''
        else:
            img_html = '''
            <div class="card-media" aria-hidden="true">
                <div class="media-placeholder"></div>
            </div>
            '''

        card_html = f"""
        <div class="stage {pos}" role="listitem">
            <div class="card">
                <div class="card-content">
                    <div class="card-head">
                        <span class="stage-num">Event {idx+1}</span>
                        <h3 class="card-title">{title}</h3>
                    </div>

                    <div class="card-body">
                        <div class="card-sep" aria-hidden="true"></div>
                        <p class="task"><strong>Task:</strong> {task}</p>

                        <div class="card-sep" aria-hidden="true"></div>
                        <p class="next"><strong>Next:</strong> {nxt}</p>
                        <div class="card-sep" aria-hidden="true"></div>
                    </div>
                </div>

                {img_html}
            </div>

        </div>
        """
        html_parts.append(card_html)

    html_parts.append("</div></div></body></html>")
    full_html = "\n".join(html_parts)

    # Heuristic height: 150px per stage but clamp to reasonable range
    height = min(max(420, 150 * len(EVENTS)), 2600)

    # Render inside an iframe (components.html) with the embedded CSS
    components.html(full_html, height=height, scrolling=True)
