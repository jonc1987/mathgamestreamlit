import pandas as pd

class ScoreTracker:
    def __init__(self):
        self.scores = {}
        self.leaderboard = []

    def add_score(self, topic: str, score: int, name: str, time: float):
        if topic not in self.scores:
            self.scores[topic] = {"correct": 0, "total": 0}
        
        self.scores[topic]["total"] += 5
        self.scores[topic]["correct"] += score
        
        self.leaderboard.append((name, score, time))
        self.leaderboard.sort(key=lambda x: (-x[1], x[2]))  # Sort by score (descending) and time (ascending)
        self.leaderboard = self.leaderboard[:10]  # Keep only top 10

    def get_score_dataframe(self) -> pd.DataFrame:
        data = []
        for topic, score in self.scores.items():
            correct = score["correct"]
            total = score["total"]
            percentage = (correct / total) * 100 if total > 0 else 0
            data.append({
                "Topic": topic,
                "Correct": correct,
                "Total": total,
                "Percentage": f"{percentage:.2f}%"
            })
        
        return pd.DataFrame(data)

    def get_leaderboard_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.leaderboard, columns=["Name", "Score", "Time (s)"])

    def reset_scores(self):
        self.scores = {}
        self.leaderboard = []
