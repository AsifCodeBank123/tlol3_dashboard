# constants.py/fixtures_modules

TEAM_CODE_MAP = {
    "Gully Gang": "GG",
    "Badshah Blasters": "BB",
    "Rockstar Rebels": "RR",
    "Dabangg Dynamos": "DD"
}


# ✅ Tournament structure per sport
TOURNAMENT_STRUCTURE = {
    "Super 32": {"next": "Super 16", "size": 16},
    "Super 16": {"next": "Quarter Final", "size": 8},
    "Quarter Final": {"next": "Semi Final", "size": 4},
    "Semi Final": {"next": "Final", "size": 2},
    "Final": {"next": None, "size": 1}
}


# ✅ Match number column name for each round
ROUND_MATCH_COLS = {
    "Super 32": "super_32_match_no",
    "Super 16": "super_16_match_no",
    "Quarter Final": "quarter_match_no",
    "Semi Final": "semi_match_no",
    "Final": "final_match_no"
}

# ✅ Match result column name for each round
ROUND_RESULT_COLS = {
    "Group Stage": "group_result",
    "Super 32": "super_32_result",
    "Super 16": "super_16_result",
    "Quarter Final": "quarter_result",
    "Semi Final": "semi_result",
    "Final": "final_result"
}

# ✅ Emoji tags for display (optional)
WINNER_EMOJI = " 🏆"
LOSER_EMOJI = " 🦆"

# ✅ Sheet ID (can be overridden from env or passed)
SPREADSHEET_ID = "1854rtEWHjp1-akVlSIzjdR_PxUW1hdKxnU2hOp5KPTw"

SPREADSHEET_ID2 = "1em-up1n6pmsw-oYfuGs5NSZP_xQi2iEHxpeEMolkFw4"


# ✅ Round size config
ROUND_SIZE = {
    "Super 32": 16,
    "Super 16": 8,
    "Quarter Final": 4,
    "Semi Final": 2,
    "Final": 1
}

SPORT_LOGOS = {
    "Carrom": "assets/carrom.jpg",
    "Chess": "assets/chess.jpg",
    "Badminton": "assets/badminton.jpg",
    "Table tennis": "assets/tt.jpg",
    "Cricket": "assets/cricket.jpg",
    "Foosball": "assets/foosball.jpg",
    # add all other sports you have
}

SPORT_RULES = {
    "Chess": {
        "Prerequisites": [
            "Stable Internet Connection",
            "Website: www.lichess.org",
            "WebEx for live moderation"
        ],
        "Rules": [
            "White/Black Side: Randomly assigned by lichess.org.",
            "Moderator must be present before starting; one player creates the game and shares the link.",
            "It is forbidden to have cell phones or electronic communication devices during the game.",
            "Good sportsmanship is expected at all times.",
            "No distracting or annoying the opponent (e.g., constant talking or repeatedly offering a draw)."
        ],
        "Match Settings": {
            "Qualifying Round": {"Type": "Standard", "Timer": "5 Minutes Per Side"},
            "Quarter Finals": {"Type": "Standard", "Timer": "8 Minutes Per Side"},
            "Semi Finals": {"Type": "Standard", "Timer": "10 Minutes Per Side"},
            "Finals": {"Type": "Standard", "Timer": "20 Minutes Per Side"}
        },
        "Elimination Rules": [
            "Using any other tab/window during the game will result in elimination.",
            "Using any chess-related application will result in a direct knockout.",
            "If timer ends, the site determines the winner.",
            "Disconnection or abandoning the game results in a loss unless rejoined within the time limit.",
            "Game must not start without a moderator watching."
        ],
        "Tournament Rules": {
            "Won Games": [
                "By checkmate.",
                "If the opponent resigns.",
                "If the opponent runs out of time."
            ],
            "Drawn Games": [
                "By stalemate.",
                "By agreement during the game.",
                "By three-fold repetition.",
                "By fifty-move rule."
            ],
            "Three-Fold Repetition": [
                "Claimable if an identical position appears three times.",
                "Tournament official may declare a draw if position repeats at least five times.",
                "Incorrect claims carry no penalty."
            ],
            "Fifty-Move Rule": [
                "Claimable if 50 moves occur without a pawn move or capture.",
                "Official may declare a draw if 75 moves occur without pawn move or capture."
            ]
        },
        "Tournament Progression": [
            "Winner advances to the next round.",
            "If drawn, another game is played until there is a winner.",
            "Later stages may be held offline if both players are in-office.",
            "Remote players in Quarterfinals or later must have their camera on."
        ],
        "Bonus Rule": [
            "Teams get a 30-minute time budget to add 1-2 minutes per game across multiple rounds."
        ]
    },

    "Foosball": {
        "Format": [
            "Match will be played with 2 on 2 players.",
            "All rounds will be played in best of 3 format.",
            "Single match is up to 10 points — whoever scores 10 first wins."
        ],
        "Serving Rules": [
            "Team who wins the toss decides the side of the table.",
            "First serve will be done by the referee.",
            "After every goal, the team who lost the point will serve.",
            "Before serving, tap the ball on the server side to signal play is starting and wait until all players are ready.",
            "Once the ball is in play, the server cannot have any part of either hand in the playing area."
        ],
        "Ball Rules": [
            "If the ball is dead between two opposing rods, it will be re-served by the referee.",
            "If the ball goes out of play, it must be re-served by the referee.",
            "Two-touch will be considered as a goal.",
            "A ball entering the goal but bouncing back will still be counted as a goal."
        ],
        "Prohibited Actions": [
            "360° rod rotations are not allowed. On the 3rd warning, the opponent gets to start from the center."
        ],
        "Player Movement": [
            "Once the game has started, you may only switch positions once."
        ]
    },

    "Table tennis": {
        "Format": [
            "Doubles matches will be played.",
            "Each set is up to 7 points in doubles format.",
            "A match consists of 3 sets — winner decided by winning 2 out of 3 sets.",
            "Semi-Finals and Finals will be best of 5 sets — winner decided by winning 3 out of 5 sets.",
            "Referee’s decision will be final.",
            "Players may bring their own bats and balls.",
            "Time-wasting is strictly prohibited and will result in point loss.",
            "The game format (direct knockout or group stage) will depend on the number of participants."
        ],
        "Service Rules": [
            "Teams decide the first serve using Rock-Paper-Scissors.",
            "It is compulsory to toss the ball in the air while serving; failure results in a fault.",
            "In doubles, the serve alternates between the two teams every two points.",
            "Serving players must alternate — after one serves twice, their partner serves the next two points.",
            "The receiving team must also alternate receivers.",
            "The serve must be diagonal from the server’s right-hand side to the receiver’s right-hand side."
        ],
        "Service & Return Order": [
            "After the initial two points, the partner of the server becomes the next server, and the partner of the receiver becomes the next receiver.",
            "In the deciding game, the team that first served in the match serves first, but the internal order of service within the team can be changed."
        ],
        "Changing Ends": [
            "Teams change ends after each game.",
            "In the deciding game, teams switch ends when one team reaches 3 points."
        ],
        "Final Game Rules": [
            "In the deciding game, teams switch ends at 5 points.",
            "The order of receiving must be maintained."
        ],
        "Playing Sequence": [
            "After the serve, the partner of the receiver plays next, followed by the partner of the server — this strict pattern continues throughout the rally.",
            "Bat touching the table is allowed and not considered a foul.",
            "Only one position switch is allowed after the game starts."
        ]
    },

    "Carrom": {
        "Format": [
            "Matches will be played in doubles.",
            "League games: Best of 3 boards — team with 2 wins qualifies.",
            "Final: Best of 5 boards — team with 3 wins is the winner.",
            "Referee’s decision will be final."
        ],
        "Queen Rules": [
            "Queen can be pocketed only after at least one coin is pocketed.",
            "If the queen is pocketed before any coin, the queen is returned to the board and the turn is lost.",
            "If the queen and cover coin are pocketed in the same turn, the queen is considered covered regardless of order."
        ],
        "Fouls & Penalties": [
            "Single Due: Striker goes into pocket without pocketing a coin — one coin returned to board.",
            "Double Due: Striker goes into pocket with a coin — two coins returned to board.",
            "If striker goes into pocket with queen — queen and one coin returned to board.",
            "If striker goes into pocket while covering queen — two coins returned to board and queen still needs to be covered.",
            "If striker pockets last coin of self and opponent in same shot — team that covered queen wins."
        ],
        "Placement Rules": [
            "Due coins are placed by opponent within the circle without touching any coin.",
            "Coins going out of board are placed in the center by referee.",
            "Once placed, a coin cannot be moved."
        ],
        "Conduct Rules": [
            "Play cut-line is warned once, then penalized by placing player's coin back on board.",
            "Elbow must not cross marked line or touch board.",
            "Do not touch coins while passing striker.",
            "Seat must not be moved while playing (repositioning without standing is allowed).",
            "No feet on the carrom table.",
            "No hand on board during opponent’s turn.",
            "Partners cannot assist while playing.",
            "Only valid finger flicks allowed — no 'ghasti' shots."
        ],
        "Equipment": [
            "Players may bring their own striker."
        ],
        "Scoring": [
            "Queen = 3 points.",
            "All other coins = 1 point."
        ],
        "Availability": [
            "Players must be present during match — no-show results in opponent being declared winner."
        ]
    },

    "Badminton": {
        "rules": [
            "A game starts with a coin toss. Whoever wins the toss chooses to serve, receive, or select court side. The losing side gets the remaining choice.",
            "Players must not touch the net with their racquet or body at any time.",
            "The shuttlecock must not be carried on or come to rest on the racquet.",
            "Players are not allowed to reach over the net to hit the shuttlecock.",
            "A serve must be delivered cross court (diagonally) to be valid.",
            "During serve, the server must not touch any court lines until the shuttlecock is struck.",
            "The shuttlecock must be struck from below the waist during serve.",
            "A point is awarded to a player whenever they win a rally.",
            "A rally is won when the shuttlecock touches the opponent’s court floor or when the opponent commits a fault (e.g., hitting outside boundaries, into the net, or failing to return).",
            "Each side can only strike the shuttlecock once before it crosses the net.",
            "Players cannot strike the shuttlecock twice in the same rally.",
            "If the shuttlecock hits the ceiling, it is considered a fault."
        ],
        "scoring_system": [
            "Matches are played as best of 3 sets.",
            "Quarter-finals and earlier: each set is played to 7 points.",
            "Semi-finals and finals: each set is played to 11 points.",
            "The side winning a rally adds a point to its score.",
            "At 7-all, the side that gains a 2-point lead first wins the set.",
            "At 16-all, the side scoring the 17th point wins the set.",
            "The side winning a set serves first in the next set."
        ]
    }


}

BONUS_CARDS = {
    "Badminton": [
        {
            "Sr": 1,
            "Event": "Badminton",
            "Card": "Tumse Na Ho Payega",
            "Description": "Replay Point – Force a replay of one point (must be called instantly).",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 2,
            "Event": "Badminton",
            "Card": "Phir Hera Pheri: Switch Server",
            "Description": "Force a server change even if the point wasn’t lost – use to unsettle rhythm.",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 3,
            "Event": "Badminton",
            "Card": "Dhinka Chika Serve",
            "Description": "Opponent must do a silly move or 5-second dance before every serve (for 3 rallies).",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        }
    ],

    "Table tennis": [
        {
            "Sr": 1,
            "Event": "Table Tennis",
            "Card": "Ek Doni Do",
            "Description": "Team using the card gets a chance to double the point.",
            "When it should be called": "During the match before the point",
            "When it cannot be active": "Cannot be used at game/match point",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 2,
            "Event": "Table Tennis",
            "Card": "Freeze Feet",
            "Description": "One Opponent can't move their feet during the next point (no stepping allowed).",
            "When it should be called": "During the match before the point",
            "When it cannot be active": "Cannot be used at game/match point",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 3,
            "Event": "Table Tennis",
            "Card": "Net Card",
            "Description": "Allows the player to use this card if a team loses the point on net.",
            "When it should be called": "During the match",
            "When it cannot be active": "Cannot be used at game/match point",
            "Team Restrictions": "Once in a Match"
        }
    ],

    "Carrom": [
        {
            "Sr": 1,
            "Event": "Carrom",
            "Card": "Ek Galti Maaf",
            "Description": "Dodge a foul (Due) penalty once in 3 sets (1 match).",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 2,
            "Event": "Carrom",
            "Card": "Mauka Naa Mila",
            "Description": "Opponent can ask the player to skip his chance to the other team player.",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        }
    ],

    "Foosball": [
        {
            "Sr": 1,
            "Event": "Foosball",
            "Card": "Khamoshhhhhh",
            "Description": "Players are not allowed to talk to each other for 30 seconds. Team loses a point.",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        },
        {
            "Sr": 2,
            "Event": "Foosball",
            "Card": "Yeh Haath Mujhe De De Thakur",
            "Description": "The opponent's goalkeeper cannot touch the rod for 10 seconds.",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in a Match"
        }
    ],

    "Chess": [
        {
            "Sr": 1,
            "Event": "Chess",
            "Card": "Piece Revival",
            "Description": "1 piece will be revived automatically if dead without touching the opponent's line.",
            "When it should be called": "During the match",
            "When it cannot be active": "",
            "Team Restrictions": "Once in Semis and Finals"
        }
    ]
}

# Full Sports Schedule Data with Details and Icons
sports_schedule = {
    "Foosball": [
        {
            "name": "Foosball",
            "type": "Indoor Game",
            "location": "Airoli",
            "format": "Doubles",
            "from": "Wednesday, August 20, 2025",
            "to": "Thursday, September 11, 2025",
            "event_head": "Bhagyashree Dhotre",
            "event_coord": "Bhagyashree Dhotre",
            "icon": "https://img.icons8.com/?size=100&id=LY7nh71PMOMY&format=png&color=000000"
        }
    ],
    "Carrom": [
        {
            "name": "Carrom",
            "type": "Indoor Game",
            "location": "Airoli",
            "format": "Doubles",
            "from": "Wednesday, August 20, 2025",
            "to": "Thursday, September 11, 2025",
            "event_head": "Umesh Tank",
            "event_coord": "Komal Panjwani",
            "icon": "https://img.icons8.com/?size=100&id=fg6EW7vMn9tC&format=png&color=000000"
        }
    ],
    "Chess": [
        {
            "name": "Chess",
            "type": "Online Game",
            "location": "Airoli",
            "format": "Singles",
            "from": "Wednesday, August 20, 2025",
            "to": "Thursday, September 11, 2025",
            "event_head": "Arijit Ghosh",
            "event_coord": "Pritam Paparkar",
            "icon": "https://img.icons8.com/?size=100&id=1uCVxPabLUk0&format=png&color=000000"
        }
    ],
    "Badminton": [
        {
            "name": "Badminton",
            "type": "Outdoor Game",
            "location": "Court",
            "format": "Doubles",
            "from": "Thursday, September 11, 2025",
            "to": "Thursday, September 11, 2025",
            "event_head": "Avinash Gowda",
            "event_coord": "Pritesh Menon",
            "icon": "https://img.icons8.com/?size=100&id=I8mGwYA8VF0W&format=png&color=000000"
        }
    ],
    "Table Tennis": [
        {
            "name": "Table Tennis",
            "type": "Indoor Game",
            "location": "Nesco",
            "format": "Doubles",
            "from": "Wednesday, September 17, 2025",
            "to": "Thursday, September 25, 2025",
            "event_head": "Rahul Arjun",
            "event_coord": "Rachita Harit",
            "icon": "https://img.icons8.com/?size=100&id=bbyXyG0mbZO2&format=png&color=000000"
        }
    ],
    "Cricket": [
        {
            "name": "Cricket",
            "type": "Outdoor Game",
            "location": "Airoli",
            "format": "Team",
            "from": "Friday, October 10, 2025",
            "to": "Friday, October 10, 2025",
            "event_head": "Wilfred Dsilva",
            "event_coord": "Vishal Dubey",
            "icon": "https://img.icons8.com/?size=100&id=Efof68tuPEwj&format=png&color=000000"
        }
    ],
    "Olympics": [
        {
            "name": "Olympics",
            "type": "Outdoor Game",
            "location": "Airoli",
            "format": "Team",
            "from": "Friday, October 10, 2025",
            "to": "Friday, October 10, 2025",
            "event_head": "Umesh Gawde",
            "event_coord": "Samiksha Prabhu",
            "icon": "https://img.icons8.com/?size=100&id=qQtUrFn64lSi&format=png&color=000000"
        }
    ]
}

