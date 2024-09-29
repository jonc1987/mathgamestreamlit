import pandas as pd

class ScoreTracker:
    def __init__(self):
        self.scores = {}

    def add_score(self, topic: str, correct: bool):
        if topic not in self.scores:
            self.scores[topic] = {"correct": 0, "total": 0}
        
        self.scores[topic]["total"] += 1
        if correct:
            self.scores[topic]["correct"] += 1

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
