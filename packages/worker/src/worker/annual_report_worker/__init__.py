from worker.config import WorkerConfigLoader, WorkerConfig
from core.integration.ragflow.client import RAGFlowClient
from core.integration.ragflow.errors import RAGFlowHealthCheckError
import requests


def main() -> None:
  loader: WorkerConfigLoader = WorkerConfigLoader()
  config: WorkerConfig = loader.load()
  print("Hello from worker!")

  rag_client = RAGFlowClient(api_key=config.ragflow.apikey, base_url=config.ragflow.url)

  try:
    health_data = rag_client.health_check()
    print("RAGFlow health check passed:")
    print(health_data)
  except RAGFlowHealthCheckError as e:
    print(f"RAGFlow health check failed: {e}")
    return
  except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    return

  try:
    kb = rag_client.ensure_knowledge_base(config.ragflow.kb_name)
    print(f"Knowledge base '{config.ragflow.kb_name}' is ready (ID: {kb.id})")
  except Exception as e:
    print(f"Failed to ensure knowledge base: {e}")
    return
