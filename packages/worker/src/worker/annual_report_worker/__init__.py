from core.models.china_mainland_listed_company import ChinaAnnualReportList
from worker.config import WorkerConfigLoader, WorkerConfig
from core.integration.ragflow.client import RAGFlowClient
from core.integration.ragflow.errors import RAGFlowHealthCheckError
import requests
from tqdm import tqdm
from pathlib import Path
import time
from typing import Set, Dict
from collections import deque


def parse_documents_in_queue(
  rag_client: RAGFlowClient,
  dataset_id: str,
  document_ids: list[str],
  max_parallel: int = 5,
  poll_interval: float = 2.0,
) -> Dict[str, str]:
  """
  Parse documents in a queue-based manner with parallel processing.

  Args:
    rag_client: RAGFlowClient instance
    dataset_id: The dataset ID containing the documents
    document_ids: List of document IDs to parse
    max_parallel: Maximum number of documents to parse in parallel (default: 5)
    poll_interval: Time in seconds between status checks (default: 2.0)

  Returns:
    Dictionary mapping document_id to final status ("DONE", "FAIL", or "CANCEL")
  """
  if not document_ids:
    print("No documents to parse")
    return {}

  # Initialize queues and tracking
  pending_queue = deque(document_ids)
  active_parsing: Set[str] = set()
  completed: Dict[str, str] = {}

  print(f"\nStarting document parsing:")
  print(f"  Total documents: {len(document_ids)}")
  print(f"  Max parallel: {max_parallel}")
  print(f"  Poll interval: {poll_interval}s\n")

  with tqdm(total=len(document_ids), desc="Parsing documents", unit="doc") as pbar:
    while pending_queue or active_parsing:
      # Start new parsing jobs if we have capacity
      while pending_queue and len(active_parsing) < max_parallel:
        doc_id = pending_queue.popleft()
        try:
          # Get dataset to access documents
          dataset = rag_client.rag.list_datasets(id=dataset_id)[0]
          dataset.async_parse_documents([doc_id])
          active_parsing.add(doc_id)
          pbar.set_postfix(
            active=len(active_parsing),
            pending=len(pending_queue),
            completed=len(completed)
          )
        except Exception as e:
          print(f"\nError starting parse for document {doc_id}: {e}")
          completed[doc_id] = "FAIL"
          pbar.update(1)

      # Check status of active parsing jobs
      if active_parsing:
        time.sleep(poll_interval)

        try:
          # Get dataset and check document statuses
          dataset = rag_client.rag.list_datasets(id=dataset_id)[0]

          # Check each active document
          finished_docs = []
          for doc_id in active_parsing:
            try:
              docs = dataset.list_documents(id=doc_id)
              if docs:
                doc = docs[0]
                # Check if parsing is complete
                if doc.run in ["DONE", "FAIL", "CANCEL"]:
                  completed[doc_id] = doc.run
                  finished_docs.append(doc_id)
                  pbar.update(1)

                  # Update description with latest status
                  if doc.run == "FAIL":
                    pbar.write(f"Failed: {doc_id} - {doc.progress_msg}")
            except Exception as e:
              print(f"\nError checking status for {doc_id}: {e}")
              completed[doc_id] = "FAIL"
              finished_docs.append(doc_id)
              pbar.update(1)

          # Remove finished documents from active set
          for doc_id in finished_docs:
            active_parsing.remove(doc_id)

          pbar.set_postfix(
            active=len(active_parsing),
            pending=len(pending_queue),
            completed=len(completed)
          )

        except Exception as e:
          print(f"\nError checking document statuses: {e}")
          time.sleep(poll_interval * 2)  # Wait longer on error

  # Print summary
  print("\nParsing complete:")
  success_count = sum(1 for status in completed.values() if status == "DONE")
  fail_count = sum(1 for status in completed.values() if status == "FAIL")
  cancel_count = sum(1 for status in completed.values() if status == "CANCEL")

  print(f"  Success: {success_count}")
  print(f"  Failed: {fail_count}")
  print(f"  Cancelled: {cancel_count}")

  return completed


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

  # Load annual report list
  print("Loading annual report list...")
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

  # Parse uploaded documents in queue
  if uploaded_doc_ids:
    print(f"\nStarting to parse {len(uploaded_doc_ids)} newly uploaded documents...")
    parse_documents_in_queue(
      rag_client=rag_client.rag_flow,
      dataset_id=kb.id,
      document_ids=uploaded_doc_ids,
      max_parallel=5,  # Default to 5 parallel parsing jobs
      poll_interval=2.0,
    )
  else:
    print("\nNo newly uploaded documents to parse.")
