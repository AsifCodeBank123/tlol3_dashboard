def extract_pair(label):
    try:
        return label.split('\n')[1].strip("() ")
    except (IndexError, AttributeError):
        return ''
    
ROUND_EMOJIS = {
    "Super 32": "🔶",
    "Super 16": "🔵",
    "Quarter Finals": "🏐",
    "Semi Finals": "🥈",
    "Final": "🏆"
}
