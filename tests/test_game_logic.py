from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Regression test: guessing above the secret used to return the
    # "Too High" outcome paired with a "Go HIGHER!" message, which told
    # the player to move further away from the secret instead of closer.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_hint_says_go_higher():
    # Regression test: guessing below the secret used to return the
    # "Too Low" outcome paired with a "Go LOWER!" message, inverted the
    # same way as the "Too High" case above.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_too_high_score_penalty_on_even_attempt():
    # Regression test: a "Too High" guess used to award +5 points instead
    # of a penalty whenever attempt_number was even.
    score = update_score(current_score=0, outcome="Too High", attempt_number=2)
    assert score == -5

def test_too_high_score_penalty_on_odd_attempt():
    # Confirms odd-attempt behavior still matches the even-attempt fix above.
    score = update_score(current_score=0, outcome="Too High", attempt_number=3)
    assert score == -5

# --- Edge cases ---

def test_check_guess_at_minimum_boundary():
    # Guessing the lowest possible value in a 1..N range should still win.
    outcome, message = check_guess(1, 1)
    assert outcome == "Win"
    assert "Correct" in message

def test_check_guess_with_negative_numbers():
    # Guess and secret can both be negative; comparison should still work.
    outcome, message = check_guess(-10, -5)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_check_guess_guess_below_zero_secret_above_zero():
    outcome, message = check_guess(-1, 5)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_update_score_win_points_floor_at_ten():
    # Winning on a very late attempt should never drop below the 10-point floor.
    score = update_score(current_score=0, outcome="Win", attempt_number=20)
    assert score == 10

def test_update_score_win_on_first_attempt():
    # attempt_number=0 (never incremented) should award the max 90 points.
    score = update_score(current_score=0, outcome="Win", attempt_number=0)
    assert score == 90

def test_update_score_too_low_penalizes_regardless_of_parity():
    even_attempt_score = update_score(current_score=0, outcome="Too Low", attempt_number=4)
    odd_attempt_score = update_score(current_score=0, outcome="Too Low", attempt_number=5)
    assert even_attempt_score == -5
    assert odd_attempt_score == -5

def test_update_score_unknown_outcome_leaves_score_unchanged():
    score = update_score(current_score=42, outcome="Something Else", attempt_number=3)
    assert score == 42

def test_update_score_can_go_negative_from_repeated_misses():
    score = 0
    for attempt_number in range(1, 6):
        score = update_score(current_score=score, outcome="Too High", attempt_number=attempt_number)
    assert score == -25
