scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = 'White Yellow Orange Green Blue Brown Black Paneled Red'.split()
BELTS = dict(zip(scores, ranks))


class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        belt = None
        # Find all the belts with a score less then 
        # or equal to the new_score
        lower_belts = [b for b in BELTS.items() if b[0] <= new_score]
        # Check if there are any (eg. if new_score is 5 then this will be empty
        # and max() throws a ValueError when passed an empty sequence)
        if lower_belts:
            # Since lower_belts is a list of tuples (score, colour) 
            # we just pull off the colour since that's all we need
            belt = max(lower_belts)[1]
        # Will be None or the belt Colour for new_score
        return belt

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        # Valid the new value is an int 
        # bigger then our current score
        if not type(new_score) == int:
            raise ValueError('Can only set score to an int')
        if new_score <= self._score:
            raise ValueError('Can only increase score')
        
        # Save the new score
        self._score = new_score

        # Check if belt has changed.
        # If so, print out the congrats message
        # otherwise just print out the new score.
        new_belt = self._get_belt(new_score)
        if (new_belt != self._last_earned_belt):
            self._last_earned_belt = new_belt
            print(f'Congrats, you earned {self._score} points obtaining the PyBites Ninja {self._last_earned_belt} Belt')
        else:
            print(f'Set new score to {self._score}')

    score = property(_get_score, _set_score)