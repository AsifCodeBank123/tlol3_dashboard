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
            {"match": "Match 2", "winner": "Esakki", "team": "Rockstar Rebels"},
            {"match": "Match 19", "winner": "Bhagyashree", "team": "Gully Gang"},
            {"match": "Match 8", "winner": "Suraj", "team": "Rockstar Rebels"},
            {"match": "Match 10", "winner": "Pooja", "team": "Badshah Blasters"},
            {"match": "Match 15", "winner": "Vishal S", "team": "Badshah Blasters"},
            {"match": "Match 18", "winner": "Wilfred", "team": "Badshah Blasters"},
            
            # add more...
        ],
        "Super 32 Winners": [
            {"match": "Match 1", "winner": "Blessen", "team": "Rockstar Rebels"},
            {"match": "Match 2", "winner": "Adnan", "team": "Dabangg Dynamos"},
            {"match": "Match 3", "winner": "Sanket Patil", "team": "Rockstar Rebels"},
            {"match": "Match 4", "winner": "Sanskar", "team": "Dabangg Dynamos"},
            {"match": "Match 5", "winner": "Lalit", "team": "Dabangg Dynamos"},
            {"match": "Match 6", "winner": "Rachita", "team": "Dabangg Dynamos"},
            {"match": "Match 7", "winner": "Irshad", "team": "Rockstar Rebels"},
            {"match": "Match 8", "winner": "Arijit", "team": "Dabangg Dynamos"},
            {"match": "Match 9", "winner": "Pooja", "team": "Badshah Blasters"},
            {"match": "Match 10", "winner": "Arvind", "team": "Rockstar Rebels"},
            {"match": "Match 11", "winner": "Saurabh", "team": "Badshah Blasters"},
            {"match": "Match 12", "winner": "Somansh", "team": "Badshah Blasters"},
            {"match": "Match 13", "winner": "Vishal", "team": "Badshah Blasters"},
            {"match": "Match 14", "winner": "Nilesh S", "team": "Dabangg Dynamos"},
            {"match": "Match 16", "winner": "Wilfred", "team": "Badshah Blasters"},
            {"match": "Match 16", "winner": "Pritesh", "team": "Badshah Blasters"},

        ],
        "Super 16 Winners": [
            {"match": "Match 1", "winner": "TBD", "team": "TBD"},
            {"match": "Match 2", "winner": "TBD", "team": "TBD"},
            {"match": "Match 3", "winner": "TBD", "team": "TBD"},
            {"match": "Match 4", "winner": "TBD", "team": "TBD"},
            {"match": "Match 5", "winner": "TBD", "team": "TBD"},
            {"match": "Match 6", "winner": "TBD", "team": "TBD"},
            {"match": "Match 7", "winner": "TBD", "team": "TBD"},
            {"match": "Match 8", "winner": "TBD", "team": "TBD"},

        ],
        "Quarter Final Winners": [
            {"match": "Match 1", "winner": "TBD", "team": "TBD"},
            {"match": "Match 2", "winner": "TBD", "team": "TBD"},
            {"match": "Match 3", "winner": "TBD", "team": "TBD"},
            {"match": "Match 4", "winner": "TBD", "team": "TBD"},
            ],
        "Semi Final Winners": [
            {"match": "Match 1", "winner": "TBD", "team": "TBD"},
            {"match": "Match 2", "winner": "TBD", "team": "TBD"},
        ],
       
        "Champion": [
             {"match": "Match 1", "winner": "TBD", "team": "TBD"},
        ]
    },
    "Carrom": {
        "Group Stage Winners": [ 
            {"match": "Match 1", "winner": "Amit & Arijit", "team": "Dabangg Dynamos"},
            {"match": "Match 2", "winner": "Bijal & Rachita", "team": "Dabangg Dynamos"},
            {"match": "Match 3", "winner": "Ankit & Esakki", "team": "Rockstar Rebels"},
            {"match": "Match 4", "winner": "Vishal S & Kiran", "team": "Badshah Blasters"},
            {"match": "Match 5", "winner": "Somansh & Gayatri", "team": "Badshah Blasters"},
            {"match": "Match 6", "winner": "Samiksha & Pooja", "team": "Badshah Blasters"},
            {"match": "Match 7", "winner": "Nilesh M & Lalit", "team": "Dabangg Dynamos"},
            {"match": "Match 8", "winner": "Kishan & Suraj", "team": "Rockstar Rebels"},
            ],
        "Super 16 Winners": [
            {"match": "Match 1", "winner": "Adnan & Nilesh S", "team": "Dabangg Dynamos"},
            {"match": "Match 2", "winner": "Asif & Vibhuti", "team": "Rockstar Rebels"},
            {"match": "Match 3", "winner": "Rahul A & Pramod", "team": "Gully Gang"},
            {"match": "Match 4", "winner": "Wilfred & Pritesh", "team": "Badshah Blasters"},
            {"match": "Match 5", "winner": "Jay & Umesh", "team": "Gully Gang"},
            {"match": "Match 6", "winner": "Samiksha & Pooja", "team": "Badshah Blasters"},
            {"match": "Match 7", "winner": "Mayur & Sanskar", "team": "Dabangg Dynamos"},
            {"match": "Match 8", "winner": "Johnson & Jincy", "team": "Rockstar Rebels"},

        ],
        "Quarter Final Winners": [
            {"match": "Match 1", "winner": "Adnan & Nilesh S", "team": "Dabangg Dynamos"},
            {"match": "Match 2", "winner": "Wilfred & Pritesh", "team": "Badshah Blasters"},
            {"match": "Match 3", "winner": "Jay & Umesh", "team": "Gully Gang"},
            {"match": "Match 4", "winner": "Johnson & Jincy", "team": "Rockstar Rebels"},
            ],
        "Semi Final Winners": [
            {"match": "Match 1", "winner": "TBD", "team": "TBD"},
            {"match": "Match 2", "winner": "TBD", "team": "TBD"},
        ],
       
        "Champion": [
             {"match": "Match 1", "winner": "TBD", "team": "TBD"},
        ]
    },
    "Badminton": {
        "Group Stage Winners": [ 
            {"match": "Match 1", "winner": "Suraj & Asif", "team": "Rockstar Rebels"},
            {"match": "Match 2", "winner": "Pooja & Samiksha", "team": "Badshah Blasters"},
            {"match": "Match 3", "winner": "Cancelled", "team": "NA"},
            {"match": "Match 4", "winner": "Bhagyashree & Pramod", "team": "Gully Gang"},
            {"match": "Match 5", "winner": "Cancelled", "team": "NA"},
            {"match": "Match 6", "winner": "Cancelled", "team": "NA"},
            ],
        "Super 16 Winners": [
            {"match": "Match 1", "winner": "Jay & Umesh", "team": "Gully Gang"},
            {"match": "Match 2", "winner": "Lalit & Sanskar", "team": "Dabangg Dynamos"},
            {"match": "Match 3", "winner": "Wilfred & Hitesh", "team": "Badshah Blasters"},
            {"match": "Match 4", "winner": "Cancelled", "team": "NA"},
            {"match": "Match 5", "winner": "Adnan & Mayur", "team": "Dabangg Dynamos"},
            {"match": "Match 6", "winner": "Saurabh & Pritesh", "team": "Badshah Blasters"},
            {"match": "Match 7", "winner": "Arvind & Blessen", "team": "Rockstar Rebels"},
            {"match": "Match 8", "winner": "Somansh & Vishal S", "team": "Badshah Blasters"},
            ],
        "Quarter Final Winners": [
            {"match": "Match 1", "winner": "Jay & Umesh", "team": "Gully Gang"},
            {"match": "Match 2", "winner": "Wilfred & Hitesh", "team": "Badshah Blasters"},
            {"match": "Match 3", "winner": "Saurabh & Pritesh", "team": "Badshah Blasters"},
            {"match": "Match 4", "winner": "Somansh & Vishal S", "team": "Badshah Blasters"},
            ],
        "Semi Final Winners": [
            {"match": "Match 1", "winner": "Jay & Umesh", "team": "Gully Gang"},
            {"match": "Match 2", "winner": "Saurabh & Pritesh", "team": "Badshah Blasters"},
        ],
       
        "Champion": [
             {"match": "Match 1", "winner": "Saurabh & Pritesh", "team": "Badshah Blasters"},
        ]
   
    },
    "Foosball": {
        "Group Stage Winners": [ 
            {"match": "Match 1", "winner": "Umesh T & Rahul A", "team": "Gully Gang"},
            {"match": "Match 6", "winner": "Pritesh & Umesh G", "team": "Badshah Blasters"},
            {"match": "Match 7", "winner": "Irshad & Suraj", "team": "Rockstar Rebels"},
            {"match": "Match 8", "winner": "Vibhuti & Jincy", "team": "Rockstar Rebels"},
            {"match": "Match 2", "winner": "Amit & Ravi", "team": "Dabangg Dynamos"},
            {"match": "Match 3", "winner": "Wilfred & Hitesh", "team": "Badshah Blasters"},
            {"match": "Match 4", "winner": "Saurabh & Kiran", "team": "Badshah Blasters"},
            {"match": "Match 5", "winner": "Ankit & Johnson", "team": "Rockstar Rebels"},
            ],
        "Super 16 Winners": [
            {"match": "Match 1", "winner": "Pramod & Bhagyashree", "team": "Gully Gang"},
            {"match": "Match 2", "winner": "Vijay C & Somansh", "team": "Badshah Blasters"},
            {"match": "Match 3", "winner": "Lalit & Mayur", "team": "Dabangg Dynamos"},
            {"match": "Match 4", "winner": "Blessen & Asif", "team": "Rockstar Rebels"},
            {"match": "Match 5", "winner": "Adnan & Arijit", "team": "Dabangg Dynamos"},
            {"match": "Match 6", "winner": "Arvind & Kishan", "team": "Rockstar Rebels"},
            {"match": "Match 7", "winner": "Komal & Avinash G", "team": "Gully Gang"},
            {"match": "Match 8", "winner": "Gayatri & Pooja", "team": "Badshah Blasters"},
            ],
        "Quarter Final Winners": [
            {"match": "Match 1", "winner": "Vijay C & Somansh", "team": "Badshah Blasters"},
            {"match": "Match 2", "winner": "Blessen & Asif", "team": "Rockstar Rebels"},
            {"match": "Match 3", "winner": "Arvind & Kishan", "team": "Rockstar Rebels"},
            {"match": "Match 4", "winner": "Komal & Avinash G", "team": "Gully Gang"},
            ],
        "Semi Final Winners": [
            {"match": "Match 1", "winner": "TBD", "team": "TBD"},
            {"match": "Match 2", "winner": "TBD", "team": "TBD"},
        ],
       
        "Champion": [
             {"match": "Match 1", "winner": "TBD", "team": "TBD"},
        ]
    },
    "Table Tennis": {
        "Group Stage Winners": [ 
            {"match": "Group A1",  "winner": "Wilfred & Pritesh", "team": "Badshah Blasters"},
            {"match": "Group A2",  "winner": "Suraj & Blessen", "team": "Rockstar Rebels"},
            {"match": "Group B1",  "winner": "Nilesh M & Lalit", "team": "Dabangg Dynamos"},
            {"match": "Group B2",  "winner": "Somansh & Saurabh", "team": "Badshah Blasters"},
            {"match": "Group C1",  "winner": "Nilesh S & Adnan", "team": "Dabangg Dynamos"},
            {"match": "Group C2",  "winner": "Vibhuti & Ravi C", "team": "Rockstar Rebels"},
            {"match": "Group D1",  "winner": "Johnson & Kishan", "team": "Rockstar Rebels"},
            {"match": "Group D2",  "winner": "Hitesh & Umesh G", "team": "Badshah Blasters"},
            ],
       
        "Quarter Final Winners": [
            {"match": "Match QF1",  "winner": "TBD", "team": "TBD"},
            {"match": "Match QF2",  "winner": "TBD", "team": "TBD"},
            {"match": "Match QF3", "winner": "TBD", "team": "TBD"},
            {"match": "Match QF4",  "winner": "TBD", "team": "TBD"},
            ],
        "Semi Final Winners": [
            {"match": "Match SF1", "winner": "TBD", "team": "TBD"},
            {"match": "Match SF2", "winner": "TBD", "team": "TBD"},
        ],
       
        "Champion": [
             {"match": "Final Match", "winner": "TBD", "team": "TBD"},
        ]
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
        "image": "assets/badminton_champion.png",
        "winner": "Pritesh & Saurabh",
        "team": "Badshah Blasters"
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
        {"name": "Amit", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Esakki", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Bishal", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Rahul P", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Vibhuti", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Jincy", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Bhaskar", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Kishansingh", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Lalit", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Johnson", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Kiran", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Asif", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Rachita", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Suraj", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Vijay S", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Irshad", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Mayur", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Avinash C", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Pooja", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Arvind", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Ravi K", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Avinash G", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Bijal", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Ankit Y", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Saurabh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Vijay C", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Nilesh M", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Vishal S", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Amitabh", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Pratap", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Nilesh S", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Rahul A", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Hitesh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Jay", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Wilfred", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Samiksha", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Bhagyashree", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Umesh G", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Somansh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Gayatri", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Pritesh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Adnan", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Sanket Patil", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Sanskar", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Arijit", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Pramod", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Umesh T", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Komal", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Blessen", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Ravi C", "team": "Rockstar Rebels", "status": "eliminated"},
       
    ],
    "Foosball": [
        {"name": "Bishal & Sanskar", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Umesh T & Rahul A", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Amit & Ravi", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Dhananjay & Sanket", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Rahul P & Jay", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Wilfred & Hitesh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Saurabh & Kiran", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Esakki & Ravi Chavan", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Bijal & Rachita", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Ankit & Johnson", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Nilesh M & Nilesh S", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Pritesh & Umesh G", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Irshad & Suraj", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Vijay S & Bhaskar P", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Vishal S & Samiksha", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Vibhuti & Jincy", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Pramod & Bhagyashree", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Vijay C & Somansh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Lalit & Mayur", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Blessen & Asif", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Adnan & Arijit", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Arvind & Kishan", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Komal & Avinash G", "team": "Gully Gang", "status": "alive"},
        {"name": "Gayatri & Pooja", "team": "Badshah Blasters", "status": "eliminated"},
       
    ],
    "Carrom": [
        {"name": "Blessen & Arvind", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Amit & Arijit", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Rahul P & Vijay S", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Bijal & Rachita", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Vijay C & Umesh G", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Ankit & Esakki", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Vishal S & Kiran", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Ravi C & Irshad", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Somansh & Gayatri", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Avinash G & Bhaskar", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Samiksha & Pooja", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Bhagyashree & Komal", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Nilesh M & Lalit", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Dhananjay & Sanket", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Kishan & Suraj", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Bishal & Ravi", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Rahul A & Pramod", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Jay & Umesh", "team": "Gully Gang", "status": "alive"},
        {"name": "Adnan & Nilesh", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Vibhuti & Asif", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Wilfred & Pritesh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Hitesh & Saurabh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Mayur & Sanskar", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Johnson & Jincy", "team": "Rockstar Rebels", "status": "alive"},
        
       
    ],
    "Badminton": [
        {"name": "Vijay C & Umesh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Suraj & Asif", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Pooja & Samiksha", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Esakki & Irshad", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Arijit & Bijal", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Komal & Rahul P", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Amit & Bishal", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Bhagyashree & Pramod", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Kiran & Gayatri", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Sanket & Dhananjay", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Johnson & Ravi C", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Vijay S & Bhaskar P", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Jay & Umesh", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Lalit & Sanskar", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Wilfred & Hitesh", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Jincy & Vibhuti", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Ankit & Kishan", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Adnan & Mayur", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Saurabh & Pritesh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Rahul A & Avinash G", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Arvind & Blessen", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Somansh & Vishal S", "team": "Badshah Blasters", "status": "eliminated"},
        
       
    ],
    "Table Tennis": [
        {"name": "Rahul & Umesh T", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Wilfred & Pritesh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Bijal & Rachita", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Esakki & Asif", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Suraj & Blessen", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Saurabh & Somansh", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Nilesh M & Lalit", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Bhagyashree & Jay", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Samiksha & Gayatri", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Ankit & Dhananjay", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Avinash G & Komal", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Kiran & Vishal S", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Mayur & Sanskar", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Irshad & Arvind", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Ravi C & Vibhuti", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Johnson & Kishan", "team": "Rockstar Rebels", "status": "alive"},
        {"name": "Adnan & Nilesh S", "team": "Dabangg Dynamos", "status": "alive"},
        {"name": "Hitesh & Umesh G ", "team": "Badshah Blasters", "status": "alive"},
        {"name": "Rahul P & Pramod", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Vijay S & Bhaskar", "team": "Gully Gang", "status": "eliminated"},
        {"name": "Pooja & Vijay C", "team": "Badshah Blasters", "status": "eliminated"},
        {"name": "Amit & Ravi K", "team": "Dabangg Dynamos", "status": "eliminated"},
        {"name": "Sanket & Jincy", "team": "Rockstar Rebels", "status": "eliminated"},
        {"name": "Bishal & Arijit", "team": "Dabangg Dynamos", "status": "eliminated"},
        
       
    ],
    "Cricket": [
      
    ],
}


# constants.py

player_avatars = {
    "Wilfred Dsilva": "https://cdn.pixabay.com/photo/2024/03/21/10/09/ai-generated-8647321_1280.jpg",
    "Vishal Shinde": "https://cdn.pixabay.com/photo/2024/04/23/18/01/ai-generated-8715804_1280.jpg",
    "Saurabh Mahadik": "https://cdn.pixabay.com/photo/2024/04/23/18/01/ai-generated-8715800_1280.jpg",
    "Pritesh Menon": "https://cdn.pixabay.com/photo/2023/02/14/16/16/ai-generated-7789977_1280.jpg",
    "Samiksha Prabhu": "https://cdn.pixabay.com/photo/2023/10/18/10/36/parrot-8323739_1280.jpg",
    "Umesh Gawade": "https://cdn.pixabay.com/photo/2023/10/18/10/30/line-8323668_1280.jpg",
    "N Pratap Kumar": "https://cdn.pixabay.com/photo/2024/09/02/05/57/cocker-spaniel-9015668_1280.jpg",
    "Vijay Chinkate": "https://cdn.pixabay.com/photo/2024/03/11/12/13/ai-generated-8626488_1280.jpg",
    "Pooja Nandoskar": "https://cdn.pixabay.com/photo/2024/02/09/17/30/ai-generated-8563502_1280.jpg",
    "Gayatri Zuting": "https://cdn.pixabay.com/photo/2024/04/20/12/33/ai-generated-8708497_1280.png",
    "Hitesh Ghadigaonkar": "https://cdn.pixabay.com/photo/2023/07/03/05/09/ai-generated-8103366_1280.jpg",
    "Somansh Datta": "https://cdn.pixabay.com/photo/2023/12/22/22/21/ai-generated-8464524_1280.jpg",
    "Kiran Padwal": "https://cdn.pixabay.com/photo/2023/03/14/17/49/ai-generated-7852855_1280.jpg",
    "Adnan Shaikh": "https://cdn.pixabay.com/photo/2024/04/06/14/02/ai-generated-8679363_1280.jpg",
    "Nilesh Sansare": "https://cdn.pixabay.com/photo/2023/12/29/11/31/ai-generated-8476023_1280.png",
    "Rachita Harit": "https://cdn.pixabay.com/photo/2024/05/17/06/54/ai-generated-8767503_1280.jpg",
    "Nilesh Mulik": "https://cdn.pixabay.com/photo/2024/03/29/21/23/ai-generated-8663666_1280.jpg",
    "Mayur Pawar": "https://cdn.pixabay.com/photo/2023/08/23/11/04/ai-generated-8208262_1280.jpg",
    "Bijal Gala": "https://cdn.pixabay.com/photo/2024/02/04/13/05/ai-generated-8552159_1280.jpg",
    "Sanskar Bagwe": "https://cdn.pixabay.com/photo/2023/04/16/19/06/dog-7930973_1280.jpg",
    "Lalit Chavan": "https://cdn.pixabay.com/photo/2024/02/25/04/11/ai-generated-8595188_1280.jpg",
    "Ravi Khanra": "https://cdn.pixabay.com/photo/2024/01/10/22/34/ai-generated-8500481_1280.jpg",
    "Bishal Pandit": "https://cdn.pixabay.com/photo/2023/07/09/12/34/dog-8116056_1280.jpg",
    "Arijit Ghosh": "https://cdn.pixabay.com/photo/2024/08/20/04/06/ai-generated-8981976_1280.jpg",
    "Amit Singh": "https://cdn.pixabay.com/photo/2024/03/22/16/31/ai-generated-8650076_1280.jpg",
    "Amitabh Singh": "https://cdn.pixabay.com/photo/2024/08/11/03/06/ai-generated-8960518_1280.jpg",
    "Umesh Tank": "https://cdn.pixabay.com/photo/2024/07/27/15/45/ai-generated-8925819_1280.jpg",
    "Bhaskar Patil": "https://cdn.pixabay.com/photo/2024/12/16/17/21/rhinoceros-9271262_1280.jpg",
    "Rahul Arjun": "https://cdn.pixabay.com/photo/2023/10/17/13/56/ai-generated-8321330_1280.jpg",
    "Avinash Gowda": "https://cdn.pixabay.com/photo/2023/03/13/20/16/ai-generated-7850729_1280.jpg",
    "Rahul Pokharkar": "https://cdn.pixabay.com/photo/2024/04/15/01/47/ai-generated-8696587_1280.png",
    "Avin Chorage": "https://cdn.pixabay.com/photo/2024/05/20/22/10/ai-generated-8776428_1280.jpg",
    "Vijay Sangale": "https://cdn.pixabay.com/photo/2024/09/02/05/58/golden-retriever-9015671_1280.jpg",
    "Jay Jagad": "https://cdn.pixabay.com/photo/2024/04/21/09/32/ai-generated-8710190_1280.jpg",
    "Bhagyashree Dhotre": "https://cdn.pixabay.com/photo/2023/12/22/10/45/ai-generated-8463567_1280.png",
    "Pramod Patel": "https://cdn.pixabay.com/photo/2024/02/28/07/05/ai-generated-8601418_1280.png",
    "Komal Panjwani": "https://cdn.pixabay.com/photo/2024/05/09/20/20/ai-generated-8751751_1280.jpg",
    "Pritam Paparkar": "https://cdn.pixabay.com/photo/2019/09/22/05/06/tiger-4495107_1280.png",
    "Dhananjay Kulkarni": "https://cdn.pixabay.com/photo/2024/04/21/09/13/ai-generated-8710159_1280.jpg",
    "Suraj Kamerkar": "https://cdn.pixabay.com/photo/2024/03/11/15/48/ai-generated-8627010_1280.jpg",
    "Kishansingh Devda": "https://cdn.pixabay.com/photo/2024/01/25/21/36/ai-generated-8532716_1280.png",
    "Vibhuti S Dabholkar": "https://cdn.pixabay.com/photo/2024/12/14/15/21/bird-9267497_1280.png",
    "Jincy Geevarghese": "https://cdn.pixabay.com/photo/2024/01/29/10/29/ai-generated-8539463_1280.png",
    "Arvind Arumuga Nainar": "https://cdn.pixabay.com/photo/2024/01/28/17/23/ai-generated-8537971_1280.jpg",
    "Johnson Thomas": "https://cdn.pixabay.com/photo/2024/05/17/12/33/ai-generated-8768250_1280.jpg",
    "Ankit Yadav": "https://cdn.pixabay.com/photo/2024/04/28/16/40/wolf-8725855_1280.jpg",
    "Irshad Darji": "https://cdn.pixabay.com/photo/2023/10/18/10/33/ai-generated-8323701_1280.jpg",
    "Ravi Chavan": "https://cdn.pixabay.com/photo/2023/06/05/21/48/dragon-8043440_1280.jpg",
    "Sanket Patil": "https://cdn.pixabay.com/photo/2023/04/14/15/54/ai-generated-7925440_1280.jpg",
    "Asif Khan": "https://cdn.pixabay.com/photo/2023/10/12/16/53/ai-generated-8311259_1280.jpg",
    "Esakki Shummugavel": "https://cdn.pixabay.com/photo/2024/02/03/20/30/ai-generated-8550982_1280.jpg",
    "Blessen Thomas": "https://cdn.pixabay.com/photo/2024/10/18/04/54/ai-generated-9129381_1280.jpg",
}

player_stats = {
    "Wilfred Dsilva": {"final": 0, "sf": 2, "qf": 1},
    "Vishal Shinde": {"final": 0, "sf": 1, "qf": 0},
    "Saurabh Mahadik": {"final": 1, "sf": 0, "qf": 1},
    "Pritesh Menon": {"final": 1, "sf": 1, "qf": 1},
    "Samiksha Prabhu": {"final": 0, "sf": 0, "qf": 1},
    "Umesh Gawade": {"final": 0, "sf": 0, "qf": 1},
    "N Pratap Kumar": {"final": 0, "sf": 0, "qf": 0},
    "Vijay Chinkate": {"final": 0, "sf": 1, "qf": 0},
    "Pooja Nandoskar":{"final": 0, "sf": 0, "qf": 2},
    "Gayatri Zuting": {"final": 0, "sf": 0, "qf": 1},
    "Hitesh Ghadigaonkar": {"final": 0, "sf": 1, "qf": 1},
    "Somansh Datta": {"final": 0, "sf": 2, "qf": 1},
    "Kiran Padwal": {"final": 0, "sf": 0, "qf": 0},
    "Adnan Shaikh": {"final": 0, "sf": 1, "qf": 3},
    "Nilesh Sansare": {"final": 0, "sf": 1, "qf": 1},
    "Rachita Harit": {"final": 0, "sf": 0, "qf": 0},
    "Nilesh Mulik": {"final": 0, "sf": 0, "qf": 1},
    "Mayur Pawar": {"final": 0, "sf": 0, "qf": 3},
    "Bijal Gala":{"final": 0, "sf": 0, "qf": 0},
    "Sanskar Bagwe": {"final": 0, "sf": 0, "qf": 2},
    "Lalit Chavan": {"final": 0, "sf": 0, "qf": 3},
    "Ravi Khanra": {"final": 0, "sf": 0, "qf": 0},
    "Bishal Pandit": {"final": 0, "sf": 0, "qf": 0},
    "Arijit Ghosh": {"final": 0, "sf": 0, "qf": 1},
    "Amit Singh": {"final": 0, "sf": 0, "qf": 0},
    "Amitabh Singh": {"final": 0, "sf": 0, "qf": 0},
    "Umesh Tank": {"final": 1, "sf": 1, "qf": 0},
    "Bhaskar Patil": {"final": 0, "sf": 0, "qf": 0},
    "Rahul Arjun": {"final": 0, "sf": 0, "qf": 1},
    "Avinash Gowda": {"final": 0, "sf": 0, "qf": 0},
    "Rahul Pokharkar": {"final": 0, "sf": 0, "qf": 0},
    "Avin Chorage": {"final": 0, "sf": 0, "qf": 0},
    "Vijay Sangale": {"final": 0, "sf": 0, "qf": 0},
    "Jay Jagad": {"final": 1, "sf": 1, "qf": 0},
    "Bhagyashree Dhotre": {"final": 0, "sf": 0, "qf": 1},
    "Pramod Patel": {"final": 0, "sf": 0, "qf": 2},
    "Komal Panjwani": {"final": 0, "sf": 0, "qf": 0},
    "Pritam Paparkar": {"final": 0, "sf": 0, "qf": 0},
    "Dhananjay Kulkarni": {"final": 0, "sf": 0, "qf": 0},
    "Suraj Kamerkar": {"final": 0, "sf": 0, "qf": 1},
    "Kishansingh Devda": {"final": 0, "sf": 1, "qf": 1},
    "Vibhuti S Dabholkar": {"final": 0, "sf": 0, "qf": 2},
    "Jincy Geevarghese": {"final": 0, "sf": 1, "qf": 0},
    "Arvind Arumuga Nainar": {"final": 0, "sf": 1, "qf": 1},
    "Johnson Thomas": {"final": 0, "sf": 1, "qf": 1},
    "Ankit Yadav": {"final": 0, "sf": 0, "qf": 0},
    "Irshad Darji": {"final": 0, "sf": 0, "qf": 0},
    "Ravi Chavan": {"final": 0, "sf": 0, "qf": 1},
    "Sanket Patil": {"final": 0, "sf": 0, "qf": 0},
    "Asif Khan": {"final": 0, "sf": 1, "qf": 1},
    "Esakki Shummugavel": {"final": 0, "sf": 0, "qf": 0},
    "Blessen Thomas": {"final": 0, "sf": 1, "qf": 2},
}


