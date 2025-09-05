TEAM_LOGOS = {
    "Gully Gang": "assets/gg_logo.png",
    "Badshah Blasters": "assets/bb_logo.png",
    "Dabangg Dynamos": "assets/dd_logo.png",
    "Rockstar Rebels": "assets/rr_logo.png"
}

TEAM_ABBR = {
    "Gully Gang": "GG",
    "Badshah Blasters": "BB",
    "Dabangg Dynamos": "DD",
    "Rockstar Rebels": "RR"
}

TEAM_COLORS = {
    "Gully Gang": "#FFF2DE",
    "Badshah Blasters": "#E3F2FD",
    "Dabangg Dynamos": "#E6F4EA",
    "Rockstar Rebels": "#F3E5F5"
}

# Compact ticker (as you set)
ticker_messages = [
    "♟️ Chess battles heating up – Raja ko checkmate karna easy nahi!",
    "🎯 Carrom striker shots flying – Queen pakadne ki race on!",
    "⚽ Foosball warriors in full attack – Ab leaderboard hilne wala hai!",
    "🏸 Badminton smashes everywhere – Rally abhi khatam nahi hui!",
    "🏓 Table Tennis spins & smashes – Khel mein asli tadka yahin hai!",
    "🏏 Cricket runs raining hard – Jeet ka maza tabhi jab fight ho josh mein!",
    "📊 Leaderboard shuffle nonstop – Kabhi tum upar, kabhi main neeche!",
    "💪 Winners never give up – Haar bhi ek nayi seekh hai!",
    "🏆 Celebrate every win with grace – Haar ko bhi izzat dena zaroori hai!"
]

# Winners by sport and stage
# Each entry: {"match": "Match 1", "winner": "Bijal", "team": "Rockstar Rebels"}
winners_by_sport_stage = {
    "Chess": {
        "Group Stage Winners": [
            {"match": "Match 12", "winner": "Bijal", "team": "Dabangg Dynamos"},
            {"match": "Match 4", "winner": "Jincy", "team": "Rockstar Rebels"},
            {"match": "Match 7", "winner": "Rachita", "team": "Dabangg Dynamos"},
            {"match": "Match 1", "winner": "Amit", "team": "Dabangg Dynamos"},
            {"match": "Match 5", "winner": "Lalit", "team": "Dabangg Dynamos"},
            
            # add more...
        ],
        "Quarterfinal Winners": [
            
        ],
        "Semifinals": [],
        "Final": []
    },
    "Carrom": {
        "Group Stages": [],
        "Quarterfinals": [],
        "Semifinals": [],
        "Final": []
    },
    "Badminton": {
        "Group Stages": [],
        "Quarterfinals": [],
        "Semifinals": [],
        "Final": []
   
    },
    "Foosball": {
        "Group Stages": [],
        "Quarterfinals": [],
        "Semifinals": [],
        "Final": []
    },
    "Table Tennis": {
        "Group Stages": [],
        "Quarterfinals": [],
        "Semifinals": [],
        "Final": []
    }
}

# Wall of Fame: per sport (final winners)
# For individual sports, use 'winner'. For Cricket, use 'team'.
wall_of_fame = {
    "Chess": {
        "title": "♟️ Chess Master",
        "image": "assets/chess.jpg",
        "winner": "",      # e.g., "Bijal"
        "team": ""  # optional
    },
    "Carrom": {
        "title": "🎯 Carrom Kings",
        "image": "assets/carrom.jpg",
        "winner": "",
        "team": ""
    },
    "Foosball": {
        "title": "⚽ Foosball Aces",
        "image": "assets/foosball.jpg",
        "winner": "",
        "team": ""
    },
    "Badminton": {
        "title": "🏸 Smash Legends",
        "image": "assets/badminton.jpg",
        "winner": "",
        "team": ""
    },
    "Table Tennis": {
        "title": "🏓 TT Maestros",
        "image": "assets/tt.jpg",
        "winner": "",
        "team": ""
    },
    "Cricket": {
        "title": "🏏 Cricket Champion",
        "image": "assets/cricket.jpg",
        "winner": "",
        "team": ""
    },
    
}
