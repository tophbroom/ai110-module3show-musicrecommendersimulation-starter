from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by match score for a user."""

        scored: List[Tuple[float, Song, List[str]]] = []
        for song in self.songs:
            score, reasons = self._score_song_for_user(user, song)
            scored.append((score, song, reasons))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a particular song was recommended to a user."""

        _, reasons = self._score_song_for_user(user, song)
        return "; ".join(reasons) if reasons else "Matched your preferences."

    @staticmethod
    def _score_song_for_user(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_similarity = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        energy_points = 1.5 * energy_similarity
        score += energy_points
        reasons.append(f"energy close (+{energy_points:.2f})")

        # A small bonus based on acoustic preference.
        if user.likes_acoustic:
            acoustic_points = 0.7 * song.acousticness
            score += acoustic_points
            reasons.append(f"more acoustic (+{acoustic_points:.2f})")
        else:
            acoustic_points = 0.7 * (1.0 - song.acousticness)
            score += acoustic_points
            reasons.append(f"less acoustic (+{acoustic_points:.2f})")

        return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue

            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(float(row["tempo_bpm"])),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (score, reasons)."""

    def get_pref(*keys, default=None):
        for key in keys:
            if key in user_prefs and user_prefs[key] is not None:
                return user_prefs[key]
        return default

    favorite_genre = get_pref("favorite_genre", "genre")
    favorite_mood = get_pref("favorite_mood", "mood")

    target_energy = get_pref("target_energy", "energy")
    target_tempo = get_pref("target_tempo_bpm", "tempo_bpm")
    target_valence = get_pref("target_valence", "valence")
    target_danceability = get_pref("target_danceability", "danceability")
    target_acousticness = get_pref("target_acousticness", "acousticness")

    default_weights = {
        "genre": 2.0,
        "mood": 1.0,
        "energy": 1.5,
        "valence": 1.0,
        "danceability": 0.8,
        "acousticness": 0.7,
        "tempo": 0.8,
    }
    weights = dict(default_weights)
    weights.update(user_prefs.get("weights", {}) or {})

    score = 0.0
    reasons: List[str] = []

    if weights["genre"] and favorite_genre is not None and song.get("genre") == favorite_genre:
        score += float(weights["genre"])
        reasons.append(f"genre match (+{float(weights['genre']):.1f})")

    if weights["mood"] and favorite_mood is not None and song.get("mood") == favorite_mood:
        score += float(weights["mood"])
        reasons.append(f"mood match (+{float(weights['mood']):.1f})")

    # Similarity helpers
    def similarity_01(song_value: float, target_value: float) -> float:
        return max(0.0, 1.0 - abs(song_value - target_value))

    def tempo_similarity(song_value: float, target_value: float) -> float:
        return max(0.0, 1.0 - min(abs(song_value - target_value) / 60.0, 1.0))

    # Weighted numeric similarities (only if the target is provided)
    if target_energy is not None:
        sim = similarity_01(float(song["energy"]), float(target_energy))
        pts = float(weights["energy"]) * sim
        score += pts
        reasons.append(f"energy close (+{pts:.2f})")

    if target_valence is not None:
        sim = similarity_01(float(song["valence"]), float(target_valence))
        pts = float(weights["valence"]) * sim
        score += pts
        reasons.append(f"valence close (+{pts:.2f})")

    if target_danceability is not None:
        sim = similarity_01(float(song["danceability"]), float(target_danceability))
        pts = float(weights["danceability"]) * sim
        score += pts
        reasons.append(f"danceability close (+{pts:.2f})")

    if target_acousticness is not None:
        sim = similarity_01(float(song["acousticness"]), float(target_acousticness))
        pts = float(weights["acousticness"]) * sim
        score += pts
        reasons.append(f"acousticness close (+{pts:.2f})")

    if target_tempo is not None:
        sim = tempo_similarity(float(song["tempo_bpm"]), float(target_tempo))
        pts = float(weights["tempo"]) * sim
        score += pts
        reasons.append(f"tempo close (+{pts:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank the songs by score and return the top-k with explanations."""

    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "Matched your preferences."
        scored.append((song, float(score), explanation))

    top = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    return top
