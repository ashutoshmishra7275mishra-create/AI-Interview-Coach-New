def evaluate_answer(answer):

    answer = answer.strip().lower()

    if not answer:
        return 0

    score = 0

    if len(answer) > 20:
        score += 3

    if len(answer) > 50:
        score += 2

    if "example" in answer:
        score += 2

    if "because" in answer:
        score += 1

    if "therefore" in answer:
        score += 2

    return min(score, 10)