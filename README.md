# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** Glitchy Guesser is a Streamlit number-guessing game: pick a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), guess the hidden secret number within a limited number of attempts, and get a "Too High"/"Too Low" hint after each guess. A score updates as you play, and the game ends when you guess correctly or run out of attempts.

- [x] **Detail which bugs you found.**
  1. **Inverted hints** - `check_guess` returned "Too High" paired with the message "Go HIGHER!", and "Too Low" paired with "Go LOWER!" - the exact opposite of what the player needed to do to find the secret.
  2. **Uneven scoring on "Too High"** - `update_score` gave +5 points instead of a -5 penalty for a "Too High" guess whenever the attempt number was even, so the same mistake was rewarded or punished depending on parity alone.
  3. **Int/str comparison bug** - `app.py` converted the secret to a string (`str(st.session_state.secret)`) on every other attempt before calling `check_guess`, so the guess (an int) and secret (a str) were compared inconsistently, which could produce wrong or inconsistent hints.
  4. *(Found but not yet fixed)* **"New Game" ignores difficulty** — clicking "New Game 🔁" always calls `random.randint(1, 100)` for the new secret, regardless of the selected difficulty, so an Easy (1–20) or Hard (1–50) round can start with a secret outside its displayed range.

- [x] **Explain what fixes you applied.** I fixed bugs 1–3: swapped the hint text in `check_guess` so it correctly tells the player which direction to guess next, removed the `attempt_number % 2 == 0` special case in `update_score` so "Too High" always applies the same -5 penalty, and removed the `str(secret)` conversion in `app.py` so `check_guess` always receives a plain int. I also moved `check_guess` and `update_score` out of `app.py` and into `logic_utils.py` (dropping a now-dead `try/except TypeError` fallback that existed only to work around the int/str bug), added regression tests for both fixes in `tests/test_game_logic.py`, fixed three pre-existing tests that compared a tuple to a bare string, and added a `pytest.ini` so `pytest` reliably finds `logic_utils` regardless of how it's invoked. Bug 4 (New Game ignoring difficulty) is documented but intentionally left unfixed for this pass.

## 📸 Demo Walkthrough

1. Select "Normal" difficulty in the sidebar. The secret number is hidden between 1 and 100, with 8 attempts allowed.
2. User enters a guess of 50. The game returns "Too Low 📈 Go HIGHER!" and the score drops by 5 points (score: -5).
3. User enters a guess of 75. The game returns "Too High 📉 Go LOWER!" and the score drops by another 5 points (score: -10).
4. User enters a guess of 60. The game returns "Too Low 📈 Go HIGHER!" (score: -15) — the hints now correctly point toward the secret instead of away from it.
5. User enters a guess of 65, which matches the secret. The game shows "🎉 Correct! You won! Final score: 25" along with a balloon animation, and the "Submit Guess" controls are disabled until a new game starts.
6. Clicking "New Game 🔁" resets the attempt counter and generates a new secret, so a fresh round can begin.

## 🧪 Test Results

Includes Challenge 1 (Advanced Edge-Case Testing): boundary values, negative numbers, the `Win` score floor, attempt-parity checks, an unknown outcome, and repeated misses driving the score negative.

```
$ pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\thevi\ai110-module1show-gameglitchinve-Project1stigator-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collecting ... collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 26%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 33%]
tests/test_game_logic.py::test_too_high_score_penalty_on_even_attempt PASSED [ 40%]
tests/test_game_logic.py::test_too_high_score_penalty_on_odd_attempt PASSED [ 46%]
tests/test_game_logic.py::test_check_guess_at_minimum_boundary PASSED    [ 53%]
tests/test_game_logic.py::test_check_guess_with_negative_numbers PASSED  [ 60%]
tests/test_game_logic.py::test_check_guess_guess_below_zero_secret_above_zero PASSED [ 66%]
tests/test_game_logic.py::test_update_score_win_points_floor_at_ten PASSED [ 73%]
tests/test_game_logic.py::test_update_score_win_on_first_attempt PASSED  [ 80%]
tests/test_game_logic.py::test_update_score_too_low_penalizes_regardless_of_parity PASSED [ 86%]
tests/test_game_logic.py::test_update_score_unknown_outcome_leaves_score_unchanged PASSED [ 93%]
tests/test_game_logic.py::test_update_score_can_go_negative_from_repeated_misses PASSED [100%]

============================== 15 passed in 0.04s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
