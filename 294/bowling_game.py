import string


def is_strike(ball):
    return ball == "X"


def is_spare(frame):
    return frame[1] == "/"


def ball_score(ball):
    score = 0
    if is_strike(ball):
        score = 10
    elif ball in string.digits:
        score = int(ball)
    return score


def frame_score(frame, next_two_balls):
    score = 0
    if is_strike(frame[0]):
        score = 10
        # Check for special case where spare was thrown next
        if len(next_two_balls) > 1 and next_two_balls[1] == "/":
            score += 10
        else:
            for ball in next_two_balls[:2]:
                score += ball_score(ball)
    elif is_spare(frame):
        score = 10
        for ball in next_two_balls[:1]:
            score += ball_score(ball)
    else:
        score = ball_score(frame[0]) + ball_score(frame[1])
    return score


def get_frame(frames, frame_number):
    # Each frame is two entries
    offset = (frame_number - 1) * 2
    frame = frames[offset : offset + 2]

    # To compute score of strike need the nex two balls
    # thrown, so grab everything after the frame and get
    # ride of all the non-throws (i.e., blanks)
    next_balls = frames[offset + 2 :].replace(" ", "")
    next_balls = next_balls[:2]

    # Return the current frame + the next two balls
    return (frame, next_balls)


def calculate_score(frames: str) -> int:
    """Calculates a total 10-pin bowling score from a string of frame data."""
    total_score = 0
    for i in range(1, 10):
        v = get_frame(frames, i)
        score = frame_score(v[0], v[1])
        #        print(f"{i:2d}: {v[0]} {v[1]} -> {score}")
        total_score += score
    # Last frame is special - just add up the total across all 3 balls
    last_frame = frames[18:]
    # If only 2 were thrown just pad it with an empty throw
    if len(last_frame) < 3:
        last_frame += " "
    # If first two were a spare then it's 10 + last ball
    if is_spare(last_frame):
        score = 10 + ball_score(last_frame[2])
    # If we threw a strike then a spare the score is 20
    elif is_strike(last_frame[0]) and last_frame[2] == "/":
        score = 20
    else:
        # Otherwise it's just the total of all three balls
        score = (
            ball_score(last_frame[0])
            + ball_score(last_frame[1])
            + ball_score(last_frame[2])
        )

    #    print(f"10: {last_frame} -> {score}")
    total_score += score
    #    print(f"{frames} -> {total_score}")
    return total_score