import random
import time
from datetime import datetime

class BadmintonMatch:
    def __init__(self, player1, player2, best_of=3):
        self.players = [player1, player2]
        self.best_of = best_of
        self.current_game = 1
        self.scores = [0, 0]       # points in current game
        self.games = [0, 0]        # games won
        self.set_scores = []       # list of tuples like [(21, 12), (21, 10), (1, 21)]
        self.log = []

        # Match timing
        self.start_time = datetime.now()
        self.end_time = None   # Time when Game ends
        self.sleep_per_rally = 0  # default = no delay

    def set_match_duration(self, target_seconds, estimated_rallies=150):
        """
        Set pacing so that the match approximately lasts target_seconds.
        estimated_rallies = expected number of rallies in a match (default ~150).
        """
        self.sleep_per_rally = target_seconds / estimated_rallies
        print(f"Match pacing set: ~{self.sleep_per_rally:.2f}s per rally")

    def rally(self):
        """Simulate a rally where one of the players scores a point."""
        if self.match_over():
            return f"Match already won by {self.winner()}"

        scorer = random.choice([0, 1])
        self.scores[scorer] += 1
        msg = f"Rally: {self.players[scorer]} scores → {self.scores_display()}"
        self.log.append(msg)
        print(msg)  # emit rally immediately
        self._check_game_end()

        if self.sleep_per_rally > 0:
            time.sleep(self.sleep_per_rally)

        return msg
    # Internal method to check if the game has ended
    def _check_game_end(self):
        """Check if the current game has ended and update match state."""
        for i in (0, 1):
            if (self.scores[i] >= 21 and (self.scores[i] - self.scores[1 - i]) >= 2) or self.scores[i] == 30:
                # Save set score
                self.set_scores.append((self.scores[0], self.scores[1]))
                set_score_str = f"{self.scores[0]}-{self.scores[1]}"

                # Update games won
                self.games[i] += 1
                msg = f"Result: {self.players[i]} wins Game {self.current_game} ({set_score_str})! Games score: {self.games_display()}"
                self.log.append(msg)
                print(msg)  # emit game result immediately
                self.current_game += 1
               
                # If match is over, freeze end time
                if self.match_over():
                    self.end_time = datetime.now()
                else:
                    self.scores = [0, 0]
                break
            

    def scores_display(self):
        return f"{self.players[0]} {self.scores[0]} - {self.players[1]} {self.scores[1]}"

    def games_display(self):
        return f"{self.players[0]} {self.games[0]} - {self.players[1]} {self.games[1]}"

    def match_over(self):
        return any(g > self.best_of // 2 for g in self.games)

    def winner(self):
        if not self.match_over():
            return None
        return self.players[0] if self.games[0] > self.games[1] else self.players[1]

    def final_summary(self):
        """Return formatted match summary with timestamp and duration."""
        end_time =  self.end_time if self.end_time else datetime.now()
        duration = end_time - self.start_time
        duration_str = str(duration).split(".")[0]  # trim microseconds

        set_scores_str = ", ".join([f"{a}-{b}" for a, b in self.set_scores])
        # Format: ddmmyyyy|hh:mm:ss
        start_str = self.start_time.strftime("%d%m%Y|%H:%M:%S")
        end_str = end_time.strftime("%d%m%Y|%H:%M:%S")

        return (
            f'StartTime:"{start_str}"\n'
            f'EndTime:"{end_str}"\n'
            f'Match Winner: {self.winner()}\n'
            f'Game Score: {self.games_display()} | Set Scores: [{set_scores_str}]\n'
            f'Duration: {duration_str}'
        )

