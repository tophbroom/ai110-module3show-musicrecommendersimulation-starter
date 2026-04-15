"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list[dict], k: int = 5) -> None:
    print("\n" + "=" * 60)
    print(f"Profile: {profile_name}")
    print(f"Prefs: {user_prefs}")
    print("-" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} — {song['artist']} (score: {score:.2f})")
        print(f"   Reasons: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Diverse profiles (for evaluation screenshots)
    profiles: dict[str, dict] = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "tempo_bpm": 130,
            "danceability": 0.85,
            "valence": 0.75,
            "acousticness": 0.15,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 75,
            "danceability": 0.55,
            "valence": 0.60,
            "acousticness": 0.85,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 155,
            "valence": 0.45,
            "danceability": 0.60,
            "acousticness": 0.10,
        },
    }

    # Edge-case profiles to see surprising behavior
    edge_profiles: dict[str, dict] = {
        "Conflicting: High Energy + Sad": {
            "mood": "sad",
            "energy": 0.95,
            "tempo_bpm": 140,
            "valence": 0.30,
            "danceability": 0.70,
            "acousticness": 0.20,
        },
        "No Genre/Mood (numbers only)": {
            "energy": 0.50,
            "tempo_bpm": 100,
            "valence": 0.60,
            "danceability": 0.60,
            "acousticness": 0.50,
        },
    }

    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs, k=5)

    for name, prefs in edge_profiles.items():
        print_recommendations(name, prefs, songs, k=5)

    # Small experiment: double energy importance, half genre importance
    baseline = profiles["High-Energy Pop"]
    print("\n" + "=" * 60)
    print("Experiment: weight shift (energy x2, genre x0.5)")
    print("=" * 60)

    print_recommendations("Baseline (default weights)", baseline, songs, k=5)
    shifted = {
        **baseline,
        "weights": {
            "genre": 1.0,
            "energy": 3.0,
        },
    }
    print_recommendations("Shifted Weights", shifted, songs, k=5)


if __name__ == "__main__":
    main()
