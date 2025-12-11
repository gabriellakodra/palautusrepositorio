from flask import Flask, render_template, request, session, redirect, url_for
from kps_tehdas_web import KPSTehdas
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store games in memory (in production, use a database)
games = {}


@app.route("/")
def index():
    """Main page - select game mode"""
    return render_template("index.html")


@app.route("/new_game", methods=["POST"])
def new_game():
    """Start a new game"""
    game_type = request.form.get("game_type")

    # Create a new game
    game = KPSTehdas.luo_peli_web(game_type)

    if game is None:
        return redirect(url_for("index"))

    # Generate a session ID
    if "game_id" not in session:
        session["game_id"] = secrets.token_hex(16)

    game_id = session["game_id"]
    games[game_id] = {"game": game, "type": game_type}

    return redirect(url_for("play"))


@app.route("/play")
def play():
    """Game page"""
    game_id = session.get("game_id")

    if game_id not in games:
        return redirect(url_for("index"))

    game_data = games[game_id]
    game_type = game_data["type"]

    # Determine game mode name
    mode_names = {
        "a": "Pelaaja vs Pelaaja",
        "b": "Pelaaja vs Tekoäly",
        "c": "Pelaaja vs Parannettu Tekoäly",
    }

    return render_template(
        "play.html", game_type=game_type, mode_name=mode_names.get(game_type, "Unknown")
    )


@app.route("/make_move", methods=["POST"])
def make_move():
    """Handle a move"""
    game_id = session.get("game_id")

    if game_id not in games:
        return {"error": "No active game"}, 400

    game_data = games[game_id]
    game = game_data["game"]
    game_type = game_data["type"]

    pelaaja1_siirto = request.json.get("pelaaja1_siirto")
    pelaaja2_siirto = request.json.get("pelaaja2_siirto")

    # Make the move
    result = game.make_move(pelaaja1_siirto, pelaaja2_siirto)

    return result


@app.route("/end_game", methods=["POST"])
def end_game():
    """End the current game"""
    game_id = session.get("game_id")

    if game_id not in games:
        return {"error": "No active game"}, 400

    game_data = games[game_id]
    game = game_data["game"]

    result = game.end_game()

    # Clean up
    del games[game_id]
    session.pop("game_id", None)

    return result


@app.route("/reset")
def reset():
    """Reset and go back to main page"""
    game_id = session.get("game_id")

    if game_id in games:
        del games[game_id]

    session.pop("game_id", None)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
