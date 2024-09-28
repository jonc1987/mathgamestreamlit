import random

class QuestionCache:
    def __init__(self, cache_size=20):
        self.cache = {}
        self.cache_size = cache_size

    def add_question(self, topic, difficulty, question):
        if (topic, difficulty) not in self.cache:
            self.cache[(topic, difficulty)] = []
        if len(self.cache[(topic, difficulty)]) < self.cache_size:
            self.cache[(topic, difficulty)].append(question)

    def get_questions(self, topic, difficulty, num_questions):
        if (topic, difficulty) not in self.cache or len(self.cache[(topic, difficulty)]) < num_questions:
            return None
        return random.sample(self.cache[(topic, difficulty)], num_questions)

    def clear_cache(self):
        self.cache = {}
