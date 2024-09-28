import pandas as pd

class ScoreTracker:
    def __init__(self):
        self.scores = {}

    def add_score(self, topic: str, correct: int):
        if topic not in self.scores:
            self.scores[topic] = {"correct": 0, "total": 0}
        
        self.scores[topic]["total"] += 5  # Total questions per quiz
        self.scores[topic]["correct"] += correct

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

    def reset_scores(self):
        self.scores = {}

    def get_leaderboard(self, top_n: int = 5) -> pd.DataFrame:
        data = []
        for topic, score in self.scores.items():
            correct = score["correct"]
            total = score["total"]
            percentage = (correct / total) * 100 if total > 0 else 0
            data.append({
                "Topic": topic,
                "Score": correct,
                "Total": total,
                "Percentage": percentage
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values("Percentage", ascending=False).head(top_n)
            df["Percentage"] = df["Percentage"].apply(lambda x: f"{x:.2f}%")
        return df
