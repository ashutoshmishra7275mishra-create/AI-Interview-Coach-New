from mock_interview import evaluate_answer

answer = input("Answer: ")

score = evaluate_answer(answer)

print(f"\nInterview Score: {score}/10")