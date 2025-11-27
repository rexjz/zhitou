from core.integration.ragflow.errors import RAGFlowHealthCheckError
from typing import Dict, Any
import requests
from ragflow_sdk import RAGFlow

class RAGFlowClient:
  def __init__(self, api_key: str, base_url: str):
    """
    Initialize RAGFlowClient with API credentials.

    Args:
      api_key: API key for authentication
      base_url: Base URL of the RAGFlow service
    """
    self.api_key = api_key
    self.base_url = base_url.rstrip("/")
    self.rag_flow = RAGFlow(api_key=api_key, base_url=base_url)

  def health_check(self) -> Dict[str, Any]:
    """
    Check the health status of the RAGFlow service.

    Returns:
      Dict containing the health check response with all services 'ok'

    Raises:
      requests.exceptions.HTTPError: If the request fails
      RAGFlowHealthCheckError: If any service is not healthy
    """
    url = f"{self.base_url}/v1/system/healthz"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    required_services = ["db", "redis", "doc_engine", "storage", "status"]

    missing_keys = [key for key in required_services if key not in data]
    if missing_keys:
      raise RAGFlowHealthCheckError(
        f"Missing required health check keys: {missing_keys}"
      )

    unhealthy_services = {
      key: data[key] for key in required_services if data[key] != "ok"
    }

    if unhealthy_services:
      error_details = data.get("_meta", {})
      raise RAGFlowHealthCheckError(
        f"Unhealthy services: {unhealthy_services}. Details: {error_details}"
      )

    return data

  def ensure_knowledge_base(self, kb_name: str):
    """
    Ensures a dataset (knowledge base) exists with the given name.
    If it doesn't exist, creates it. If it exists, does nothing.

    Args:
      kb_name: The name of the knowledge base (dataset)

    Returns:
      The DataSet object (either existing or newly created)

    Raises:
      Exception: If the operation fails
    """
    # Check if dataset already exists
    datasets = self.rag_flow.list_datasets(name=kb_name)

    if datasets and len(datasets) > 0:
      # Dataset exists, return the first one
      return datasets[0]
    else:
      # Dataset doesn't exist, create it
      return self.rag_flow.create_dataset(name=kb_name)
