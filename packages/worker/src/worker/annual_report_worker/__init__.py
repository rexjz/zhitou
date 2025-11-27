from worker.config import WorkerConfigLoader, WorkerConfig
from core.integration.ragflow.client import RAGFlowClient
from core.integration.ragflow.errors import RAGFlowHealthCheckError
import requests


def main() -> None:
  loader: WorkerConfigLoader = WorkerConfigLoader()
  config: WorkerConfig = loader.load()
  print("Hello from worker!")

  # Initialize RAGFlowClient
  rag_client = RAGFlowClient(api_key=config.ragflow.apikey, base_url=config.ragflow.url)

  # Perform health check
  try:
    health_data = rag_client.health_check()
    print("RAGFlow health check passed:")
    print(health_data)
  except RAGFlowHealthCheckError as e:
    print(f"RAGFlow health check failed: {e}")
  except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
  