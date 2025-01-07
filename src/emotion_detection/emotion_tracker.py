from collections import deque


class EmotionTracker:
    def __init__(self, max_length=100):
        self.emotions = deque(maxlen=max_length)

    def add_emotion(self, emotion):
        self.emotions.append(emotion)

    def get_most_common_emotion(self):
        return max(set(self.emotions), key=self.emotions.count) if self.emotions else None