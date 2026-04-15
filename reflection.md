# Reflection: Profile Comparisons

## Profiles Tested

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Edge case: Conflicting (High Energy + Sad)
- Edge case: Numbers only (no genre/mood)

## Comparisons

High-Energy Pop vs Chill Lofi:
- The Pop profile pushed upbeat pop songs to the top because it rewards matching genre and mood, plus higher energy and danceability.
- The Lofi profile pushed slower, more acoustic songs to the top because it targets lower energy, lower tempo, and higher acousticness.

High-Energy Pop vs Deep Intense Rock:
- Both profiles like high energy, so some intense tracks can appear in both lists.
- The Rock profile is more likely to rank rock or intense songs first because it rewards rock and intense matches, while the Pop profile rewards pop and happy matches.

Chill Lofi vs Deep Intense Rock:
- These two profiles produce very different results because they disagree on energy and tempo.
- Lofi recommends calmer, more acoustic tracks, while Rock recommends faster, louder, high-energy tracks.

## One Thing That Surprised Me

- A song can still rank high even if the genre does not match, as long as the numeric features are close and it matches mood.
- With a small catalog, the same songs show up often, so it is harder to get variety.

## Experiment Note

- When I increased the energy weight and lowered the genre weight, high-energy songs became even more dominant in the rankings.
