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
            {"match": "Match 6", "winner": "Johnson", "team": "Rockstar Rebels"},
            {"match": "Match 13", "winner": "Saurabh", "team": "Badshah Blasters"},
            {"match": "Match 3", "winner": "Rahul P", "team": "Gully Gang"},
            {"match": "Match 11", "winner": "Arvind", "team": "Rockstar Rebels"},
            {"match": "Match 17", "winner": "Rahul A", "team": "Gully Gang"},
            {"match": "Match 9", "winner": "Irshad", "team": "Rockstar Rebels"},
            {"match": "Match 14", "winner": "Nilesh M", "team": "Dabangg Dynamos"},
            {"match": "Match 16", "winner": "Nilesh S", "team": "Dabangg Dynamos"},
            
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


# players_by_sport: list of players (for pairs, use combined names)
# status: "alive" or "eliminated"
# For chess we expect 46 entries (fill as needed). Example entries below.

players_by_sport = {
    "Chess": [
        {"name": "Dhananjay", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Amit", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Esakki", "team": "Rockstar Rebels", "status": "not_played"},
        {"name": "Bishal", "team": "Dabangg Dynamos", "status": "not_played"},
        {"name": "Rahul P", "team": "Gully Gang", "status": "alive"},
        {"name": "Vibhuti", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Jincy", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Bhaskar", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Kishansingh", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Lalit", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Johnson", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Kiran", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Asif", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Rachita", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Suraj", "team": "Rockstar Rebels", "status": "not_played"},
        {"name": "Vijay S", "team": "Gully Gang", "status": "not_played"},
        {"name": "Irshad", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Mayur", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Avinash C", "team": "Gully Gang", "status": "not_played"},
        {"name": "Pooja", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Arvind", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Ravi K", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Avinash G", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Bijal", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Ankit Y", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Saurabh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Vijay C", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Nilesh M", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Vishal S", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Amitabh", "team": "Dabangg Dynamos", "status": "not_played"},
        {"name": "Pratap", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Nilesh S", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Rahul A", "team": "Gully Gang", "status": "alive"},
        {"name": "Hitesh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Jay", "team": "Gully Gang", "status": "not_played"},
        {"name": "Wilfred", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Samiksha", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Bhagyashree", "team": "Gully Gang", "status": "not_played"},
        {"name": "Umesh G", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Somansh", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Gayatri", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Pritesh", "team": "Badshah Blasters", "status": "not_played"},
        {"name": "Adnan", "team": "Dabangg Dynamos", "status": "not_played"},
        {"name": "Sanket Patil", "team": "Dabangg Dynamos", "status": "not_played"},
        {"name": "Sanskar", "team": "Gully Gang", "status": "not_played"},
        {"name": "Arijit", "team": "Gully Gang", "status": "not_played"},
        {"name": "Pramod", "team": "Gully Gang", "status": "not_played"},
        {"name": "Umesh T", "team": "Gully Gang", "status": "not_played"},
        {"name": "Komal", "team": "Gully Gang", "status": "not_played"},
        {"name": "Blessen", "team": "Rockstar Rebels", "status": "not_played"},
        {"name": "Ravi C", "team": "Rockstar Rebels", "status": "not_played"},
    ],
    "Carrom": [
        {"name": "Amit", "team": "Gully Gang", "status": "alive"},
        {"name": "Pooja", "team": "Rockstar Rebels", "status": "eliminated"},
        # pairs -> combine names such as "Amit & Rohit"
    ],
    "Foosball": [
        {"name": "Team Alpha (Rohit & Sam)", "team": "Gully Gang", "status": "alive"},
        {"name": "Team Bravo (Nisha & Tara)", "team": "Badshah Blasters", "status": "eliminated"},
    ],
    "Badminton": [
        {"name": "Rahul", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Sana", "team": "Rockstar Rebels", "status": "alive"},
    ],
    "Table Tennis": [
        {"name": "Vikram", "team": "Gully Gang", "status": "alive"},
        {"name": "Nina", "team": "Badshah Blasters", "status": "eliminated"},
    ],
    "Cricket": [
        # show team names for Cricket winners scenario; but here players/pairs format kept same
        {"name": "Gully Gang", "team": "Gully Gang", "status": "alive"},
        {"name": "Rockstar Rebels", "team": "Rockstar Rebels", "status": "eliminated"},
    ],
}

