from core.integration.ragflow.errors import RAGFlowHealthCheckError
from typing import Dict, Any, Optional, TYPE_CHECKING
import requests
from ragflow_sdk import RAGFlow
from loguru import logger
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

  def ensure_knowledge_base(self, kb_name: str, permission: str = "me"):
    """
    Ensures a dataset (knowledge base) exists with the given name and permissions.
    If it doesn't exist, creates it. If it exists, verifies access.

    Permission Model:
      - First checks if dataset exists at all (case-insensitive)
      - Then checks if current user has access to it
      - If exists but no access, raises clear PermissionError
      - If doesn't exist, creates it with specified permission

    Args:
      kb_name: The name of the knowledge base (dataset)
      permission: Permission level for the dataset. Options:
        - "me": Only you can manage the dataset (default)
        - "team": All team members can manage the dataset

    Returns:
      The DataSet object (either existing or newly created)

    Raises:
      Exception: If the operation fails
      ValueError: If invalid permission value provided
      PermissionError: If dataset exists but user lacks permission
    """
    # Validate permission parameter
    if permission not in ["me", "team"]:
      raise ValueError(f"Invalid permission '{permission}'. Must be 'me' or 'team'")

    # List all datasets to check existence
    all_datasets = self.rag_flow.list_datasets()
    logger.debug(f"Total datasets accessible: {len(all_datasets)}")

    # Check if any dataset has the name we want (case-insensitive)
    exists = any(ds.name.lower() == kb_name.lower() for ds in all_datasets)
    logger.debug(f"Dataset '{kb_name}' exists: {exists}")

    if exists:
      # Dataset exists, check if we have access to it by name
      datasets_by_name = self.rag_flow.list_datasets(name=kb_name)
      logger.debug(f"Datasets matching name '{kb_name}': {len(datasets_by_name)}")

      if datasets_by_name and len(datasets_by_name) > 0:
        # Dataset exists and we have access
        logger.info(f"Found existing dataset '{kb_name}' with access")
        return datasets_by_name[0]
      else:
        # Dataset exists but we don't have access
        raise PermissionError(
          f"Dataset '{kb_name}' exists but you don't have access to it.\n"
          f"Solutions:\n"
          f"  1. Ask the dataset owner to grant you '{permission}' permission\n"
          f"  2. Use a different dataset name (e.g., '{kb_name}_v2')\n"
          f"  3. If the owner set permission='me', they need to update it to permission='team'\n"
          f"  4. Delete the existing dataset (if you have admin access) and recreate it"
        )
    else:
      # Dataset doesn't exist, create it
      logger.info(f"Dataset '{kb_name}' doesn't exist, creating with permission='{permission}'")
      try:
        return self.rag_flow.create_dataset(name=kb_name, permission=permission)
      except Exception as e:
        error_msg = str(e)
        # This shouldn't happen since we already checked, but handle it gracefully
        if "lacks permission" in error_msg or "already exists" in error_msg.lower():
          raise PermissionError(
            f"Failed to create dataset '{kb_name}'. It may have been created by another process.\n"
            f"Original error: {error_msg}"
          ) from e
        # Re-raise other errors as-is
        raise

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
