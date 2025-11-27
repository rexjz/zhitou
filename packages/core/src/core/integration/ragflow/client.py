from core.integration.ragflow.errors import RAGFlowHealthCheckError
from typing import Dict, Any, Optional, TYPE_CHECKING
import requests
from ragflow_sdk import RAGFlow

if TYPE_CHECKING:
  from core.models.china_mainland_listed_company import (
    AnnualReportFile,
    ChinaMainlandListedCompany,
  )


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

  @staticmethod
  def create_annual_report_metadata(
    stock_code: str, year: str, full_name: str, short_name: str
  ) -> Dict[str, str]:
    """
    Creates metadata dictionary for a China annual report document.

    Metadata Schema:
      - document_type: "china_annual_report" (constant)
      - stock_code: Stock code (e.g., "600018")
      - year: Report year (e.g., "2021")
      - full_name: Full company name (e.g., "上海国际港务集团股份有限公司")
      - short_name: Short company name (e.g., "上港集团")

    Args:
      stock_code: Stock code of the company
      year: Year of the annual report
      full_name: Full name of the company
      short_name: Short name of the company

    Returns:
      Dictionary containing the metadata fields
    """
    return {
      "document_type": "china_annual_report",
      "stock_code": stock_code,
      "year": year,
      "full_name": full_name,
      "short_name": short_name,
    }

  def check_annual_report_exists(
    self, dataset_id: str, stock_code: str, year: str
  ) -> bool:
    """
    Checks if a China annual report already exists in the knowledge base.

    Args:
      dataset_id: ID of the dataset to check
      stock_code: Stock code to search for
      year: Year to search for

    Returns:
      True if a document with the given stock_code and year exists, False otherwise
    """
    try:
      dataset = self.rag_flow.list_datasets(id=dataset_id)
      if not dataset or len(dataset) == 0:
        return False

      dataset = dataset[0]

      documents = dataset.list_documents(
        keywords=f"{stock_code}_{year}", page=1, page_size=100
      )

      for doc in documents:
        # Note: meta_fields might not be directly accessible via the SDK
        # This is a best-effort check based on document name
        if stock_code in doc.name and year in doc.name:
          return True

      return False
    except Exception:
      return False

  def upload_annual_report(
    self,
    dataset_id: str,
    company: "ChinaMainlandListedCompany",
    report_file: "AnnualReportFile",
    file_path: str,
    check_exists: bool = True,
  ) -> Optional[Any]:
    """
    Uploads a China annual report to the knowledge base with proper metadata.

    Args:
      dataset_id: ID of the dataset to upload to
      company: ChinaMainlandListedCompany object containing company information
      report_file: AnnualReportFile object containing report information
      file_path: Full path to the PDF file (including base_path if applicable)
      check_exists: If True, check if document already exists before uploading

    Returns:
      The uploaded Document object, or None if already exists and check_exists=True

    Raises:
      Exception: If the upload fails
    """
    if check_exists and self.check_annual_report_exists(
      dataset_id, company.code, report_file.year
    ):
      return None

    datasets = self.rag_flow.list_datasets(id=dataset_id)
    if not datasets or len(datasets) == 0:
      raise ValueError(f"Dataset with ID {dataset_id} not found")

    dataset = datasets[0]

    metadata = self.create_annual_report_metadata(
      company.code, report_file.year, company.full_name, company.short_name
    )

    display_name = report_file.get_standardized_display_name(
      company.code, company.short_name
    )

    with open(file_path, "rb") as f:
      blob = f.read()

    dataset.upload_documents([{"display_name": display_name, "blob": blob}])

    documents = dataset.list_documents(keywords=display_name, page=1, page_size=1)
    if documents and len(documents) > 0:
      doc = documents[0]
      try:
        doc.update({"meta_fields": metadata})
        return doc
      except Exception as e:
        try:
          dataset.delete_documents(ids=[doc.id])
        except Exception:
          pass
        raise Exception(
          f"Failed to update metadata for document {display_name}: {e}"
        ) from e

    return None
