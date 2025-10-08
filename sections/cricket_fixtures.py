# sections/cricket_fixtures.py
"""
Cricket fixtures — round-robin matches shown as cards.
Each card contains a circular team logo that overlaps the top of the card,
plus a colored footer. Local images under assets/teams/ are embedded as data-URIs.
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import mimetypes
import base64
import html

# ----- Fixtures -----
FIXTURES = [
    ("Dabangg Dynamos", "Gully Gang"),
    ("Rockstar Rebels", "Badshah Blasters"),
    ("Badshah Blasters", "Dabangg Dynamos"),
    ("Gully Gang", "Rockstar Rebels"),
    ("Rockstar Rebels", "Dabangg Dynamos"),
    ("Gully Gang", "Badshah Blasters"),
]

# ----- Images (relative to assets/) -----
TEAM_IMAGES = {
    "Dabangg Dynamos": "teams/dd_logo.png",
    "Gully Gang": "teams/gg_logo.png",
    "Rockstar Rebels": "teams/rr_logo.png",
    "Badshah Blasters": "teams/bb_logo.png",
}

# ----- Team Colors (used for footer and ring) -----
TEAM_COLORS = {
    "Rockstar Rebels": ("#000000", "#333333"),     # black -> dark gray
    "Dabangg Dynamos": ("#6A0DAD", "#8B3DD9"),     # purple gradient
    "Gully Gang": ("#800000", "#B22222"),          # maroon gradient
    "Badshah Blasters": ("#0047AB", "#1E90FF"),    # blue gradient
}


# ----- Helpers: robust local-file -> data-uri (tries several candidate locations) -----
def try_paths_for(local_path: str):
    if not local_path:
        return
    s = str(local_path).replace("\\", "/").strip()
    p = Path(s)
    if p.is_absolute():
        yield p
    if s.startswith("assets/"):
        yield Path.cwd() / s.lstrip("/")
    else:
        yield Path.cwd() / "assets" / s.lstrip("/")
    yield Path.cwd() / s.lstrip("/")
    yield Path(s)


def file_to_data_uri_try(local_path: str):
    if not local_path:
        return None
    for candidate in try_paths_for(local_path):
        try:
            if candidate.exists() and candidate.is_file():
                mime, _ = mimetypes.guess_type(str(candidate))
                mime = mime or "image/png"
                data = candidate.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
                return f"data:{mime};base64,{b64}"
        except Exception:
            continue
    return None


def resolve_team_image(team_name: str):
    raw = TEAM_IMAGES.get(team_name) or TEAM_IMAGES.get(team_name.strip())
    if not raw:
        return None
    s = str(raw).strip()
    if s.startswith(("http://", "https://", "data:")):
        return s
    return file_to_data_uri_try(s)


# ----- CSS: compact cards + responsive VS -----------------------------------
CSS = """
.cricket-root { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 12px 10px 28px; color:#111; }
.cricket-container { max-width:1100px; margin: 6px auto; }
.cricket-title { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
.matches { display: grid; gap: 12px; }

/* match row: two compact cards with VS badge overlapping horizontally */
.match-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  align-items: start;
  position: relative;
  padding: 6px 0;
  justify-items: center; /* keep cards narrower and centered in their cells */
}

/* separator line between matches */
.match-separator {
  height: 2px;
  width: 85%;
  margin: 24px auto;
  border-radius: 2px;
  background: linear-gradient(
    90deg,
    rgba(255, 204, 0, 0.15) 0%,
    rgba(0, 0, 0, 0.05) 50%,
    rgba(255, 204, 0, 0.15) 100%
  );
  opacity: 1.0;
}

/* tighter spacing for small screens */
@media (max-width: 880px) {
  .match-separator {
    width: 90%;
    margin: 18px auto;
    opacity: 0.6;
  }
}


/* VS badge: absolute on desktop, static between stacked cards on mobile */
.vs-badge {
  position: absolute;
  left: 50%;
  top: 44%;
  transform: translate(-50%, -50%);
  z-index: 8;
  width: 60px;
  height: 60px;
  border-radius: 999px;
  display:flex; align-items:center; justify-content:center;
  font-weight:800; color:#fff;
  background: linear-gradient(135deg,#ff6b00,#ffcc00);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  border: 3px solid rgba(255,255,255,0.12);
  font-size: 0.9rem;
}

/* compact card container */
/* compact card container */
.team-card {
  position: relative;
  background: linear-gradient(
    180deg,
    #fffbea 0%,
    #fff8e1 40%,
    #fff4cc 100%
  ); /* soft goldish gradient */
  border-radius: 12px;
  box-shadow:
    0 10px 24px rgba(12, 20, 30, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  padding: 92px 14px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 420px;
  min-height: 170px;
  transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.25s ease;
}

.team-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 44px rgba(12, 20, 30, 0.12);
  background: linear-gradient(
    180deg,
    #fff7d6 0%,
    #fff2b8 50%,
    #ffeaa7 100%
  ); /* slightly richer gold hover */
}


/* circle logo badge (smaller) */
.team-img-circle {
  position: absolute;
  top: 10px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg, #fff, #f3f3f3);
  box-shadow: 0 10px 22px rgba(0,0,0,0.12);
  overflow: hidden;
  border: 5px solid rgba(255,255,255,0.95);
  transition: transform .2s ease, box-shadow .2s ease;
}
.team-img-circle img { width:72%; height:auto; object-fit:contain; display:block; }

/* colored inner ring using inset shadow */
.team-card.rockstar_rebels .team-img-circle { box-shadow: 0 10px 22px rgba(0,0,0,0.12), inset 0 0 0 5px rgba(17,17,17,0.88); }
.team-card.dabangg_dynamos .team-img-circle { box-shadow: 0 10px 22px rgba(0,0,0,0.12), inset 0 0 0 5px rgba(106,13,173,0.88); }
.team-card.gully_gang .team-img-circle { box-shadow: 0 10px 22px rgba(0,0,0,0.12), inset 0 0 0 5px rgba(128,0,0,0.88); }
.team-card.badshah_blasters .team-img-circle { box-shadow: 0 10px 22px rgba(0,0,0,0.12), inset 0 0 0 5px rgba(0,71,171,0.88); }

/* footer area */
.team-footer {
  margin-top: 140px;
  padding: 14px 16px;
  width: 400px;
  border-radius: 12px;
  color: #fff;
  font-weight: 800;
  text-align: center;
  font-size: 1.05rem;
  letter-spacing: 0.6px;
  box-shadow:
    inset 0 1px 3px rgba(255, 255, 255, 0.25),  /* soft inner shine */
    0 6px 18px rgba(0, 0, 0, 0.15);             /* outer depth */
  background-image:
    linear-gradient(145deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0) 40%), /* light streak */
    var(--team-gradient, linear-gradient(135deg, #222, #111)); /* fallback gradient */
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.25s ease;
}

.team-footer::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.15), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.team-card:hover .team-footer::before {
  opacity: 1; /* gentle light glow on hover */
}

.team-footer:hover {
  transform: translateY(-2px);
  box-shadow:
    0 10px 24px rgba(0, 0, 0, 0.25),
    inset 0 2px 4px rgba(255, 255, 255, 0.25);
}

.team-card.rockstar_rebels .team-footer { background: linear-gradient(135deg,#000,#2b2b2b); }
.team-card.dabangg_dynamos .team-footer { background: linear-gradient(135deg,#6A0DAD,#8B3DD9); }
.team-card.gully_gang .team-footer { background: linear-gradient(135deg,#800000,#B22222); }
.team-card.badshah_blasters .team-footer { background: linear-gradient(135deg,#0047AB,#1E90FF); }

/* small subtitle (optional) */
.team-sub { margin-top:6px; color: rgba(255,255,255,0.88); font-weight:600; font-size:0.85rem; }

/* responsive: stacked matches, VS badge static and centered between cards */
@media (max-width:880px) {
  .match-row { grid-template-columns: 1fr; gap: 12px; padding: 8px 0; }
  .vs-badge { position: static; transform: none; margin: 6px auto; width:58px; height:58px; }
  .team-card { padding: 80px 12px 10px; min-height: 150px; max-width: 640px; }
  .team-img-circle { width: 86px; height: 86px; top: 6px; border-width:4px; }
}

/* very small screens - scale down slightly */
@media (max-width:480px) {
  .team-card { padding: 72px 10px 10px; min-height: 140px; }
  .team-img-circle { width: 76px; height: 76px; top: 4px; }
  .vs-badge { width:52px; height:52px; font-size:0.85rem; }
}
"""


# ----- Render function -----
def render_cricket_fixtures():
    st.title("🏏 Round Robin Fixtures")
   

    # build HTML
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'/>",
        "<style>", CSS, "</style></head><body style='margin:0;padding:0;'>",
        "<div class='cricket-root'><div class='cricket-container'>",
        
        "<div class='matches'>"
    ]

    for idx, (team_a, team_b) in enumerate(FIXTURES, start=1):
        img_a = resolve_team_image(team_a)
        img_b = resolve_team_image(team_b)

        def make_card(team, img_src):
            cls = team.lower().replace(" ", "_")
            img_html = (
                f'<img src="{html.escape(img_src, quote=True)}" alt="{html.escape(team)}"/>'
                if img_src
                else '<div style="width:70%;height:70%;border-radius:50%;background:linear-gradient(180deg,#eee,#ddd)"></div>'
            )
            footer_text = html.escape(team)
            return f"""
            <div class="team-card {cls}">
              <div class="team-img-circle">{img_html}</div>
              <div class="team-plate">
                <div class="team-footer">{footer_text}</div>
              </div>
            </div>
            """

        parts.append(f"<div class='match-row' data-match='{idx}'>")
        parts.append(make_card(team_a, img_a))
        parts.append(make_card(team_b, img_b))
        parts.append('<div class="vs-badge" role="img" aria-label="versus">VS</div>')
        parts.append("</div>")

        # 🔹 Separator line after each match except last
        if idx < len(FIXTURES):
            parts.append('<div class="match-separator"></div>')


    parts.append("</div></div></div></body></html>")
    full_html = "\n".join(parts)

    approx_h = min(max(700, 400 * len(FIXTURES)), 3000)
    components.html(full_html, height=approx_h, scrolling=False)


# Optional: debug helper to show resolved paths (uncomment to use)
def debug_paths():
    st.write("cwd:", Path.cwd())
    for team, path in TEAM_IMAGES.items():
        st.write(team, "->", path)
        for cand in try_paths_for(path):
            st.write("   cand:", cand, "exists:", cand.exists())
