import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestFlaskApp:
    def test_index_page(self, client):
        """Test that index page loads"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Kivi-Paperi-Sakset" in response.data

    def test_new_game_pelaaja_vs_pelaaja(self, client):
        """Test starting a player vs player game"""
        response = client.post(
            "/new_game", data={"game_type": "a"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Pelaaja vs Pelaaja" in response.data

    def test_new_game_tekoaly(self, client):
        """Test starting a player vs AI game"""
        response = client.post(
            "/new_game", data={"game_type": "b"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Tekoäly".encode("utf-8") in response.data

    def test_new_game_parempi_tekoaly(self, client):
        """Test starting a player vs improved AI game"""
        response = client.post(
            "/new_game", data={"game_type": "c"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert (
            "Parannettu".encode("utf-8") in response.data
            or "Tekoäly".encode("utf-8") in response.data
        )

    def test_new_game_invalid_type(self, client):
        """Test that invalid game type redirects to index"""
        response = client.post(
            "/new_game", data={"game_type": "x"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_play_without_game(self, client):
        """Test accessing play page without starting a game"""
        response = client.get("/play", follow_redirects=True)
        assert response.status_code == 200

    def test_make_move_player_vs_player(self, client):
        """Test making a move in player vs player mode"""
        # Start a game
        client.post("/new_game", data={"game_type": "a"})

        # Make a move
        response = client.post(
            "/make_move",
            json={"pelaaja1_siirto": "k", "pelaaja2_siirto": "s"},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "pelaaja1_siirto" in data
        assert "pelaaja2_siirto" in data
        assert "game_over" in data

    def test_make_move_vs_ai(self, client):
        """Test making a move against AI"""
        # Start a game
        client.post("/new_game", data={"game_type": "b"})

        # Make a move
        response = client.post(
            "/make_move", json={"pelaaja1_siirto": "k"}, content_type="application/json"
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["pelaaja1_siirto"] == "k"
        assert data["pelaaja2_siirto"] in ["k", "p", "s"]

    def test_make_move_invalid_move(self, client):
        """Test making an invalid move"""
        # Start a game
        client.post("/new_game", data={"game_type": "a"})

        # Make an invalid move
        response = client.post(
            "/make_move",
            json={"pelaaja1_siirto": "x", "pelaaja2_siirto": "k"},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["game_over"] == True
        assert "error" in data

    def test_end_game(self, client):
        """Test ending a game"""
        # Start a game
        client.post("/new_game", data={"game_type": "a"})

        # Make a move
        client.post(
            "/make_move",
            json={"pelaaja1_siirto": "k", "pelaaja2_siirto": "s"},
            content_type="application/json",
        )

        # End the game
        response = client.post("/end_game")

        assert response.status_code == 200
        data = response.get_json()
        assert data["game_over"] == True

    def test_reset(self, client):
        """Test reset functionality"""
        # Start a game
        client.post("/new_game", data={"game_type": "a"})

        # Reset
        response = client.get("/reset", follow_redirects=True)
        assert response.status_code == 200
        assert b"Kivi-Paperi-Sakset" in response.data

    def test_full_game_flow(self, client):
        """Test a complete game flow"""
        # Start a game
        response = client.post(
            "/new_game", data={"game_type": "a"}, follow_redirects=True
        )
        assert response.status_code == 200

        # Play 2 rounds (not reaching 3 wins yet)
        for _ in range(2):
            response = client.post(
                "/make_move",
                json={"pelaaja1_siirto": "k", "pelaaja2_siirto": "p"},
                content_type="application/json",
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["game_over"] == False

        # End the game
        response = client.post("/end_game")
        assert response.status_code == 200
        data = response.get_json()
        assert data["game_over"] == True
        assert data["tokan_pisteet"] == 2  # Player 2 won 2 rounds

    def test_game_ends_at_3_wins(self, client):
        """Test that game automatically ends when a player wins 5 times"""
        # Start a game
        client.post("/new_game", data={"game_type": "a"})

        # Play 3 rounds where player 1 always wins
        for i in range(3):
            response = client.post(
                "/make_move",
                json={"pelaaja1_siirto": "k", "pelaaja2_siirto": "s"},
                content_type="application/json",
            )
            assert response.status_code == 200
            data = response.get_json()

            if i < 2:
                assert data["game_over"] == False
                assert data["ekan_pisteet"] == i + 1
            else:
                # On 5th win, game should end
                assert data["game_over"] == True
                assert data["ekan_pisteet"] == 3
                assert "winner" in data
                assert data["winner"] == "Pelaaja 1"
