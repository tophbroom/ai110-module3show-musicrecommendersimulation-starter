# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

**VibeMatch 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

This recommender suggests the top 5 songs from a small CSV catalog based on a simple taste profile. It is meant for classroom exploration so the matching logic is simple, not for real users. It assumes a user’s taste can be represented with a few labels (genre, mood) and a few numbers (energy, tempo, etc.).

Non-intended use: This should not be used to make real product decisions, profile real people, or serve as a "best music" ranking for everyone.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

My model gives each song a score. It adds points when the song matches the user’s favorite genre and mood. Then it adds more points when the song’s “vibe numbers” are close to the user’s target values, like energy and tempo. After scoring every song, it sorts the list from highest score to lowest and recommends the top songs.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

The catalog has 18 songs in `data/songs.csv`. It includes a mix of genres and moods (like pop, lofi, rock, jazz, edm, folk, metal, r&b, classical, hip hop, and country). I expanded it from the starter 10 songs by adding 8 more. However the dataset is missing lots of real-world taste signals like lyrics, language, cultural context, and user listening history.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

This system works best when the user profile is specific and the catalog has songs that clearly match it. For example, the “Chill Lofi” profile ranked lofi + chill songs at the top, which felt reasonable. It is also easy to explain because every recommendation comes with clear reasons (genre match, mood match, energy close, etc.).

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

One limitation is that a strong genre or mood match can dominate the ranking, even if other features do not fit perfectly. For example, “Gym Hero” showed up for the “Deep Intense Rock” profile because it matched mood and had close energy and tempo, even though the genre was pop. Another limitation is that the catalog is small, so the same songs can appear often and it cannot represent many tastes. This can create a “filter bubble” effect where users keep seeing similar styles instead of discovering something different.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested three main profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. I also tested edge cases like “High Energy + Sad” and a profile with no genre/mood (numbers only) to see if the system still behaved sensibly. The results usually made sense when the profile lined up with songs in the dataset. One surprise was that high-energy songs often stayed near the top across different profiles, because energy is heavily rewarded and the dataset has several high-energy tracks.

I ran one small experiment by doubling the energy weight and cutting the genre weight in half. The same top songs mostly stayed at the top, but the gap between high-energy songs and the rest got bigger, showing that the system is sensitive to weight changes.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

- Add a “diversity” rule so the top 5 are not all the same style.
- Learn preferences from clicks/skips instead of only a manual profile.
- Add more songs so profiles have more variety to choose from.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

My biggest learning moment was seeing how a simple scoring rule can create results that feel “personal.” It was also surprising how much the weights matter. Small changes made the ranking change a lot.

AI tools helped me move faster when I was writing the first version of the functions and fixing errors. I still had to double-check the logic, especially the math for similarity scores and the data types from the CSV.

This project made me think more about why real recommendation apps can feel repetitive. If a model rewards one feature strongly, the same types of songs keep showing up. If I extended this project, I would add a rule that forces more variety and I would test with a bigger dataset.
