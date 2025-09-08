from simEngine.badmintonDouble import BadmintonMatch

# Example run
if __name__ == "__main__":
    match = BadmintonMatch("Player A", "Player B")
    match.set_match_duration(5)  # Target ~1 min match

    while not match.match_over():
        match.rally()

    print(match.final_summary())
