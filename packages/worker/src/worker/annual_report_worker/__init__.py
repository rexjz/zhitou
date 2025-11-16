from ragflow_sdk import RAGFlow
from worker.config import WorkerConfigLoader, WorkerConfig


def main() -> None:
  loader: WorkerConfigLoader = WorkerConfigLoader()
  config: WorkerConfig = loader.load()
  print(config)
  print("Hello from worker!")

  rag_object = RAGFlow(api_key=config.ragflow.apikey, base_url=config.ragflow.url)