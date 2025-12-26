from core.models.china_mainland_listed_company import ChinaAnnualReportList
from ragflow_sdk import RAGFlow
from worker.config import WorkerConfigLoader, WorkerConfig
from core.integration.ragflow.client import RAGFlowClient
from core.integration.ragflow.errors import RAGFlowHealthCheckError
import requests
from tqdm import tqdm
from pathlib import Path
from typing import Dict
from loguru import logger

def parse_documents_in_queue(
  rag_client: RAGFlow,
  dataset_id: str,
  document_ids: list[str],
  batch_size: int = 10,
) -> Dict[str, Dict[str, int | str]]:
  """
  Parse documents in batches using RAGFlow's parse_documents API.

  This function uses the SDK's built-in parse_documents() method which:
  - Awaits completion of all parsing tasks
  - Returns detailed results including chunk_count and token_count
  - Handles keyboard interruption (Ctrl+C) gracefully

  Args:
    rag_client: RAGFlowClient instance
    dataset_id: The dataset ID containing the documents
    document_ids: List of document IDs to parse
    batch_size: Number of documents to parse in each batch (default: 10)

  Returns:
    Dictionary mapping document_id to result dict with keys:
      - status: "success", "failed", or "cancelled"
      - chunk_count: Number of chunks created
      - token_count: Total tokens processed
  """
  if not document_ids:
    print("No documents to parse")
    return {}

  # Get dataset once
  try:
    dataset = rag_client.list_datasets(id=dataset_id)[0]
  except Exception as e:
    print(f"Error getting dataset: {e}")
    return {}

  print("\nStarting document parsing:")
  print(f"  Total documents: {len(document_ids)}")
  print(f"  Batch size: {batch_size}\n")

  all_results: Dict[str, Dict[str, int | str]] = {}

  # Process documents in batches
  with tqdm(total=len(document_ids), desc="Parsing documents", unit="doc") as pbar:
    for i in range(0, len(document_ids), batch_size):
      batch = document_ids[i:i + batch_size]
      batch_num = i // batch_size + 1
      total_batches = (len(document_ids) + batch_size - 1) // batch_size

      pbar.set_description(f"Parsing batch {batch_num}/{total_batches}")

      try:
        # Use SDK's parse_documents which awaits completion
        finished = dataset.parse_documents(batch)

        # Process results
        for doc_id, status, chunk_count, token_count in finished:
          all_results[doc_id] = {
            "status": status,
            "chunk_count": chunk_count,
            "token_count": token_count,
          }

          # Log failures
          if status == "failed":
            pbar.write(f"Failed: {doc_id}")

          pbar.update(1)

      except KeyboardInterrupt:
        pbar.write("\nParsing interrupted by user. Pending tasks have been cancelled.")
        # Mark remaining documents as cancelled
        for doc_id in batch:
          if doc_id not in all_results:
            all_results[doc_id] = {
              "status": "cancelled",
              "chunk_count": 0,
              "token_count": 0,
            }
        break

      except Exception as e:
        pbar.write(f"\nError parsing batch {batch_num}: {e}")
        # Mark batch documents as failed
        for doc_id in batch:
          if doc_id not in all_results:
            all_results[doc_id] = {
              "status": "failed",
              "chunk_count": 0,
              "token_count": 0,
            }
        pbar.update(len(batch))

  # Print summary
  print("\nParsing complete:")
  success_count = sum(1 for r in all_results.values() if r["status"] == "success")
  fail_count = sum(1 for r in all_results.values() if r["status"] == "failed")
  cancel_count = sum(1 for r in all_results.values() if r["status"] == "cancelled")
  total_chunks = sum(r["chunk_count"] for r in all_results.values())
  total_tokens = sum(r["token_count"] for r in all_results.values())

  print(f"  Success: {success_count}")
  print(f"  Failed: {fail_count}")
  print(f"  Cancelled: {cancel_count}")
  print(f"  Total chunks: {total_chunks}")
  print(f"  Total tokens: {total_tokens}")

  return all_results


def main() -> None:
  loader: WorkerConfigLoader = WorkerConfigLoader()
  config: WorkerConfig = loader.load()

  rag_client = RAGFlowClient(api_key=config.ragflow.apikey, base_url=config.ragflow.url)
  try:
    health_data = rag_client.health_check()
    logger.info("RAGFlow health check passed:")
    logger.info(health_data)
  except RAGFlowHealthCheckError as e:
    logger.error(f"RAGFlow health check failed: {e}")
    return
  except requests.exceptions.RequestException as e:
    logger.error(f"Request error: {e}")
    return

  try:
    kb = rag_client.ensure_knowledge_base(config.ragflow.kb_name)
    logger.info(f"Knowledge base '{config.ragflow.kb_name}' is ready (ID: {kb.id})")
  except Exception as e:
    logger.error(f"Failed to ensure knowledge base: {e}")
    return

  # Load annual report list
  logger.info("Loading annual report list...")
  report_list = ChinaAnnualReportList.from_file(
    file_path=config.china_annual_report_soures.listing_file_path,
    base_path=config.china_annual_report_soures.base_path,
  )

  # Calculate total number of files
  total_files = sum(len(company.files) for company in report_list.companies)
  print(
    f"Found {len(report_list.companies)} companies with {total_files} annual reports"
  )

  # Upload reports with progress bar
  uploaded = 0
  skipped = 0
  failed = 0
  uploaded_doc_ids = []  # Track uploaded document IDs for parsing

  with tqdm(total=total_files, desc="Uploading annual reports", unit="file") as pbar:
    for company in report_list.companies:
      for file_info in company.files:
        # Construct full file path
        if report_list.base_path:
          file_path = Path(report_list.base_path) / file_info.file_path
        else:
          file_path = Path(file_info.file_path)

        # Update progress bar description
        pbar.set_description(f"Uploading {company.code} {file_info.year}")

        try:
          result = rag_client.upload_annual_report(
            dataset_id=kb.id,
            company=company.company,
            report_file=file_info,
            file_path=str(file_path),
            check_exists=True,
          )

          if result is None:
            skipped += 1
            pbar.set_postfix(uploaded=uploaded, skipped=skipped, failed=failed)
          else:
            uploaded += 1
            uploaded_doc_ids.append(result.id)  # Track document ID for parsing
            pbar.set_postfix(uploaded=uploaded, skipped=skipped, failed=failed)

        except Exception as e:
          failed += 1
          pbar.set_postfix(uploaded=uploaded, skipped=skipped, failed=failed)
          print(f"\nError uploading {company.code} {file_info.year}: {e}")

        pbar.update(1)

  print("\nUpload complete:")
  print(f"  Uploaded: {uploaded}")
  print(f"  Skipped (already exists): {skipped}")
  print(f"  Failed: {failed}")

  # Parse uploaded documents in batches
  if uploaded_doc_ids:
    print(f"\nStarting to parse {len(uploaded_doc_ids)} newly uploaded documents...")
    parse_documents_in_queue(
      rag_client=rag_client.rag_flow,
      dataset_id=kb.id,
      document_ids=uploaded_doc_ids,
      batch_size=10,  # Process 10 documents per batch
    )
  else:
    print("\nNo newly uploaded documents to parse.")
