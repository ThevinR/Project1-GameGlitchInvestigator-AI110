# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude (Claude Code) as my AI teammate for this project, working in an agentic chat mode where it could read and edit the repo directly.

**Correct suggestion.** When I asked it to move `check_guess` and `update_score` into `logic_utils.py` and fix the two bugs I had marked with `# FIXME`, it suggested swapping the hint text so "Too High" pairs with "Go LOWER!" and "Too Low" pairs with "Go HIGHER!" (previously inverted), and removing the `attempt_number % 2 == 0` special case in `update_score` that gave +5 points instead of a penalty on even attempts. This was correct: the original code was telling the player to move further away from the secret instead of closer, and the scoring bonus had no gameplay justification — it was just alternating between a penalty and a reward for the same "Too High" outcome depending on attempt parity. I verified it by writing regression tests (`test_too_high_hint_says_go_lower`, `test_too_low_hint_says_go_higher`, `test_too_high_score_penalty_on_even_attempt`, `test_too_high_score_penalty_on_odd_attempt`) and running `pytest`, which passed 7/7, and by spot-checking `check_guess(60, 50)` and `update_score(0, "Too High", 2)` directly in a Python shell to confirm the returned message and score matched expectations.

**Suggestion I changed.** While fixing `check_guess`, the original function had a `try/except TypeError` fallback block that stringified the guess if comparing an int to a secret raised a `TypeError` (a symptom of a separate bug where `app.py` converted `secret` to a string on every other attempt). I had Claude fix that root cause too — removing the `secret = str(...)` conversion in `app.py` so `check_guess` always receives an int. Once that was done, the `try/except TypeError` fallback in `check_guess` became permanently dead code, since `secret` could never be a non-int anymore. Rather than leaving that unreachable branch in place "just in case," I had it rewrite `check_guess` without the fallback at all, keeping only the simple `if/else` comparison. I rejected keeping the defensive branch because it was now unreachable complexity that made the function harder to read for no benefit — not because the original suggestion was factually wrong. I confirmed this was safe by re-running the full test suite after the simplification (still 7/7 passing) and manually driving the Streamlit app in the browser across several guesses to confirm the hints and win condition still behaved correctly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I considered a bug really fixed only once I had a test that failed against the old behavior and passed against the new one, plus a manual check in the running app. For the hint-inversion bug, I ran `pytest tests/test_game_logic.py -v` after adding `test_too_high_hint_says_go_lower` and `test_too_low_hint_says_go_higher`, which asserted `"LOWER" in message` for a too-high guess and `"HIGHER" in message` for a too-low guess — these would have failed against the original (inverted) code and passed cleanly against the fix (7 passed in 0.03s). I also ran the three pre-existing tests (`test_winning_guess`, `test_guess_too_high`, `test_guess_too_low`) and discovered they were failing for an unrelated reason: they compared the full `(outcome, message)` tuple returned by `check_guess` directly against a bare string like `"Win"`, which can never be equal. I fixed those by unpacking the tuple (`outcome, _ = check_guess(...)`) before asserting on `outcome`.

I also hit a real environment bug while testing: running plain `pytest` from the project root raised `ModuleNotFoundError: No module named 'logic_utils'`, even though the same tests passed under `python -m pytest`. Claude explained that bare `pytest` inserts the `tests/` folder onto `sys.path` (since there's no `tests/__init__.py`), not the project root where `logic_utils.py` lives, while `python -m pytest` adds the current working directory automatically — which is why it worked for one invocation and not the other. The fix was adding a `pytest.ini` with `pythonpath = .` so the project root is always importable, which I verified by running bare `pytest` afterward and seeing all 7 tests collected and passed.

Yes — AI helped me design these tests. I described the bug in plain language ("the hint says to go higher when the guess was already too high") and it translated that into concrete assertions on the tuple returned by `check_guess`, and similarly for the `update_score` even/odd attempt bug. It also explained *why* the original three tests were broken (tuple vs. string comparison) rather than just rewriting them silently, which helped me actually understand the mistake instead of just copying a fix.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every click reruns the whole script from top to bottom, so any plain variable resets each time. `st.session_state` is a dict that survives reruns, which is why `secret`, `score`, and `attempts` are stored there instead of as normal variables.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to keep writing a regression test for each bug before trusting that a fix actually worked, instead of just eyeballing the diff. Next time I'd ask the AI to run the tests itself right after each fix instead of waiting until the end, so broken tests (like the tuple-vs-string ones) surface immediately. This project made me more skeptical of AI-generated code by default — it runs and looks reasonable, but subtle logic bugs (inverted hints, parity-based scoring) only showed up once I actually played the game and wrote tests.


### Reason why I did not accept the suggetions as written 

 While fixing check_guess, the original function had a try/except TypeError fallback block that stringified the guess if comparing an int to a secret raised a TypeError (a symptom of a separate bug where app.py converted secret to a string on every other attempt). I had Claude fix that root cause too — removing the secret = str(...) conversion in app.py so check_guess always receives an int. Once that was done, the try/except TypeError fallback in check_guess became permanently dead code, since secret could never be a non-int anymore. Rather than leaving that unreachable branch in place "just in case," I had it rewrite check_guess without the fallback at all, keeping only the simple if/else comparison. I rejected keeping the defensive branch because it was now unreachable complexity that made the function harder to read for no benefit — not because the original suggestion was factually wrong. I confirmed this was safe by re-running the full test suite after the simplification (still 7/7 passing) and manually driving the Streamlit app in the browser across several guesses to confirm the hints and win condition still behaved correctly.