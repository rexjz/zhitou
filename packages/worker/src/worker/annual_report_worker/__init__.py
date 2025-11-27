from core.models.china_mainland_listed_company import ChinaAnnualReportList
from worker.config import WorkerConfigLoader, WorkerConfig
from core.integration.ragflow.client import RAGFlowClient
from core.integration.ragflow.errors import RAGFlowHealthCheckError
import requests
from tqdm import tqdm
from pathlib import Path


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
