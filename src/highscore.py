import json


def save_highscore(name: str, score: int) -> None:
    """saves the player's score in the top 10 highscores"""
    filename = "highscore.json"
    try:
        with open(filename, "r") as file:
            highscores = json.load(file)
        if not isinstance(highscores, list):
            highscores = []
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = []
    if name == "":
        name = "unknown"
    highscores.append({
        "name": name,
        "score": score
    })
    highscores.sort(
        key=lambda player: player["score"],
        reverse=True
    )
    highscores = highscores[:10]
    with open(filename, "w") as file:
        json.dump(highscores, file, indent=4)
