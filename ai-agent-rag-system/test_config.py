from app.config import config

print("App Name:", config.APP_NAME)
print("Version:", config.APP_VERSION)
print("Host:", config.HOST)
print("Port:", config.PORT)
print("Embedding Model:", config.EMBEDDING_MODEL)
print("Vector DB:", config.VECTOR_DB)
print("LLM URL:", config.LLM_URL)
print("Max Iterations:", config.MAX_RESEARCH_ITERATIONS)