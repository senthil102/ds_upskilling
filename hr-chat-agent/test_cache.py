from semantic_cache import SemanticCache


cache = SemanticCache()


question = "What is the annual leave policy?"

cached = cache.get_cached_response(question)

if cached:
    print("CACHE HIT")
    print(cached)

else:
    print("CACHE MISS")

    answer = (
        "Employees are entitled to 18 annual leave days per year."
    )

    cache.save_response(
        question,
        answer
    )

    print("Response saved to cache.")