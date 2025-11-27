from worker.config import WorkerConfigLoader, WorkerConfig
from urllib.parse import urljoin
from ragflow_sdk import RAGFlow
import urllib.request
import urllib.error
import json


def main() -> None:
  loader: WorkerConfigLoader = WorkerConfigLoader()
  config: WorkerConfig = loader.load()
  print("Hello from worker!")

  rag_object = RAGFlow(api_key=config.ragflow.apikey, base_url=config.ragflow.url)
  # Make GET request to healthz endpoint using urllib
  url = urljoin(config.ragflow.url , "/v1/system/healthz")
  print(url)
  try:
    with urllib.request.urlopen(url) as response:
      data = json.loads(response.read().decode())
      print(data)
  except urllib.error.HTTPError as e:
    # Print response even on HTTP errors (non-200 status codes)
    data = json.loads(e.read().decode())
    print(f"HTTP Error {e.code}: {data}")
  