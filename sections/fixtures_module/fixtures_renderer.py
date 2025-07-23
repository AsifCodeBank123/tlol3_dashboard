import streamlit as st
import base64
import os
from sections.fixtures_module.state_manager import generate_fixtures_globally
from sections.ui_data import display_card
from sections.fixtures_module.utils import ROUND_EMOJIS

def render_sport_fixtures(sport):
    if f"fixtures_{sport}_matches" not in st.session_state:
        matches, knockouts = generate_fixtures_globally(sport)
        st.session_state[f"fixtures_{sport}_matches"] = matches
        st.session_state[f"fixtures_{sport}_knockouts"] = knockouts

    matches = st.session_state[f"fixtures_{sport}_matches"]
    knockouts = st.session_state[f"fixtures_{sport}_knockouts"]

    # Sport-specific background image
    image_filename = f"assets/{sport.lower()}.jpg"
    if os.path.exists(image_filename):
        with open(image_filename, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
                <div style='background-image: url("data:image/jpeg;base64,{encoded}"); background-size: cover; background-position: center; padding: 40px 20px;'>
            """, unsafe_allow_html=True)

    # Group Stage
    with st.expander("🟡 Group Stage", expanded=True):
        if not matches:
            st.info("No group stage matches generated for this sport yet.")
        for i in range(0, len(matches), 3):
            cols = st.columns(3)
            for j, match in enumerate(matches[i:i + 3]):
                index = i + j  # unique card index
                with cols[j]:
                    match_id = f"{sport.lower()}_group_stage_match_{index}"
                    display_card(
                        title=f"Match {index + 1}",
                        team1=match["team 1"],
                        players1=match["players 1"],
                        team2=match["team 2"],
                        players2=match["players 2"],
                        match_id=match_id,
                        round_name="Group Stage",
                        card_index=index
                    )

    # Knockout Rounds
    for round_name, round_matches in knockouts.items():
        emoji = ROUND_EMOJIS.get(round_name, "")
        with st.expander(f"{emoji} {round_name}", expanded=True):
            if not round_matches:
                st.info(f"No {round_name} matches generated for this sport yet.")
                continue

            for i in range(0, len(round_matches), 2):
                cols = st.columns(2)
                for j, match in enumerate(round_matches[i:i + 2]):
                    match_index = i + j
                    match_num = match_index + 1
                    with cols[j]:
                        match_id = f"{sport.lower()}_{round_name.lower().replace(' ', '_')}_match_{match_num}"
                        match_title = f"Match {match_num}"

                        team1, team2 = "TBD", "TBD"
                        players1, players2 = ("TBD",), ("TBD",)
                        team1_result = team2_result = ""

                        if isinstance(match, dict):
                            team1 = match.get('team 1', 'TBD')
                            players1 = match.get('players 1', ('TBD',))
                            team2 = match.get('team 2', 'TBD')
                            players2 = match.get('players 2', ('TBD',))
                            team1_result = str(match.get('p1_dict', {}).get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()
                            team2_result = str(match.get('p2_dict', {}).get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()

                        elif isinstance(match, tuple):
                            mid, t1_data, t2_data = match
                            match_title = f"Match {mid}"

                            def parse_team(side):
                                if isinstance(side, dict):
                                    name = side.get("team name", "TBD")
                                    result = str(side.get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()
                                    if "player" in side:
                                        players = (side["player"],)
                                    else:
                                        players = (
                                            side.get("player 1", ""),
                                            side.get("player 2", "")
                                        )
                                elif isinstance(side, str):
                                    parts = side.split("\n")
                                    name = parts[0].split("(")[0].strip() if parts else "TBD"
                                    players = tuple(parts[1].strip("()").split(" & ")) if len(parts) > 1 else ("TBD",)
                                    result = ""
                                else:
                                    name, players, result = "TBD", ("TBD",), ""
                                return name, players, result

                            team1, players1, team1_result = parse_team(t1_data)
                            team2, players2, team2_result = parse_team(t2_data)

                        # Cleanup missing players
                        players1 = tuple(p for p in players1 if p) or ("TBD",)
                        players2 = tuple(p for p in players2 if p) or ("TBD",)

                        # Mark winners/eliminated
                        if team1_result == "w":
                            team1 += " 🏆"
                            team2 += " 🦆"
                        elif team2_result == "w":
                            team2 += " 🏆"
                            team1 += " 🦆"

                        # Display card
                        display_card(
                            title=match_title,
                            team1=team1,
                            players1=players1,
                            team2=team2,
                            players2=players2,
                            match_id=match_id,
                            round_name=round_name,
                            card_index=match_index
                        )

            # ▶ Add a "Regenerate" button for updating fixtures
            if round_name != "Final":
                regen_key = f"regen_{sport}_{round_name}"
                if st.button(f"🔄 Regenerate {round_name} for {sport}", key=regen_key):
                    st.session_state.pop(f"fixtures_{sport}_matches", None)
                    st.session_state.pop(f"fixtures_{sport}_knockouts", None)
                    st.rerun()

    # if os.path.exists(image_filename):
    #     st.markdown("</div>", unsafe_allow_html=True)

