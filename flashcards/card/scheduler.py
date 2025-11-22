from fsrs import Scheduler as FSRS_Scheduler, Rating

def map_rating_to_fsrs(performance_rating: int) -> Rating:
    if performance_rating == 1:
        return Rating.Again
    elif performance_rating == 2:
        return Rating.Hard
    elif performance_rating == 3:
        return Rating.Good
    elif performance_rating == 4:
        return Rating.Easy
    else:
        return Rating.Again

class Scheduler:
    def __init__(self):
        self.sc = FSRS_Scheduler()

    def change_desired_retention(self, retention = 0.9):
        self.sc.desired_retention = retention

    def change_max_interval(self, max_interval):
        self.sc.max_interval = max_interval

    def change_learning_steps(self, steps):
        self.sc.learning_steps = steps

    def change_relearning_steps(self, steps):
        self.sc.relearning_steps = steps

    def review_card(self, card, rating):
        mapped_rating = map_rating_to_fsrs(rating)
        return self.sc.review_card(card, mapped_rating)