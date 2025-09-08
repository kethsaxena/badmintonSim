import tkinter as tk
from simEngine.badmintonDouble import BadmintonMatch
import threading

class BadmintonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badminton Match Simulator")

        # Initialize match
        self.match = BadmintonMatch("Player A", "Player B")

        # --- Scoreboard ---
        self.score_label = tk.Label(root, text="Scores will appear here", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.game_label = tk.Label(root, text="Games: 0-0", font=("Arial", 14))
        self.game_label.pack(pady=5)

        # --- Match Log ---
        self.log_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=10)

        # --- Duration Control ---
        duration_frame = tk.Frame(root)
        duration_frame.pack(pady=5)

        tk.Label(duration_frame, text="Set Match Duration:").pack(side=tk.LEFT, padx=5)
        self.duration_entry = tk.Entry(duration_frame, width=10)
        self.duration_entry.pack(side=tk.LEFT)
        tk.Button(duration_frame, text="Set Duration", command=self.set_duration).pack(side=tk.LEFT, padx=5)

        # --- Buttons ---
        self.match_button = tk.Button(root, text="Simulate Full Match", command=self.simulate_full_match, font=("Arial", 12))
        self.match_button.pack(pady=5)

        self.summary_button = tk.Button(root, text="Show Final Summary", command=self.show_summary, font=("Arial", 12))
        self.summary_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_match, font=("Arial", 12))
        self.reset_button.pack(pady=5)

    def parse_duration(self, input_str):
        """Convert user input like 60, 1m, 10m, 1h to seconds."""
        input_str = input_str.strip().lower()
        if input_str.endswith("m") and not input_str.endswith("min"):
            return int(input_str[:-1]) * 60
        elif input_str.endswith("h"):
            return int(input_str[:-1]) * 3600
        else:
            return int(input_str)  # assume seconds

    def set_duration(self):
        """Set pacing for the match."""
        try:
            seconds = self.parse_duration(self.duration_entry.get())
            self.match.set_match_duration(seconds)
            self.log_message(f"⏱ Match pacing set: ~{seconds} sec total")
        except ValueError:
            self.log_message("⚠️ Invalid input. Enter seconds, e.g., 60, 1m, or 1h")

    def simulate_full_match(self):
        """Run the entire match in a background thread so GUI doesn't freeze."""
        if self.match.match_over():
            self.log_message("🏆 Match already finished! Reset to start a new one.")
            return

        def run_match():
            while not self.match.match_over():
                msg = self.match.rally()
                self.log_message(msg)
                self.update_scoreboard()

            # Update scoreboard with final set scoreline
            scoreline_str = " | ".join([f"{a}-{b}" for a, b in self.match.set_scores])
            self.score_label.config(text=f"Scoreline: {scoreline_str}")

            # Log final summary
            self.log_message(self.match.final_summary())

        threading.Thread(target=run_match, daemon=True).start()

    def show_summary(self):
        """Show final match summary."""
        self.log_message(self.match.final_summary())

    def reset_match(self):
        """Reset the app for a new simulation."""
        # Create new match object
        self.match = BadmintonMatch("Player A", "Player B")

        # Clear log + reset labels
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "Ready for next Game\n")
        self.log_text.config(state=tk.DISABLED)

        self.score_label.config(text="Scores will appear here")
        self.game_label.config(text="Games: 0-0")

    def update_scoreboard(self):
        """Update scoreboard labels."""
        self.score_label.config(text=self.match.scores_display())
        self.game_label.config(text="Games: " + self.match.games_display())

    def log_message(self, msg):
        """Append a message to the match log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = BadmintonApp(root)
    root.mainloop()
