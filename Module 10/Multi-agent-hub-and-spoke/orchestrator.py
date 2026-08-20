from agents import researcher, planner, executor, writer, critic


task = "Explain photosynthesis to a 10-year-old."


print("\n1. Researcher")
research = researcher(task)
print(research)


print("\n2. Planner")
plan = planner(task, research)
print(plan)


print("\n3. Executor")
draft = executor(task, plan)
print(draft)


print("\n4. Writer")
answer = writer(task, draft)
print(answer)


print("\n5. Critic")
review = critic(task, answer)
print(review)


print("\n========== FINAL ANSWER ==========")
print(answer)