from pydantic import BaseModel, Field
from typing import List
import json
from pathlib import Path


class AnnualReportFile(BaseModel):
  """Represents a single annual report file for a specific year."""
  year: str = Field(..., description="The year of the annual report")
  file_path: str = Field(..., description="Path to the PDF file")


class CompanyAnnualReports(BaseModel):
  """Represents all annual reports for a single company."""
  code: str = Field(..., description="Stock code of the company")
  files: List[AnnualReportFile] = Field(default_factory=list, description="List of annual report files")
  full_name: str = Field(..., description="Full name of the company")
  short_name: str = Field(..., description="Short name of the company")


class ChinaAnnualReportList(BaseModel):
  """Represents a collection of annual reports for multiple companies."""
  companies: List[CompanyAnnualReports] = Field(default_factory=list, description="List of companies with their annual reports")
  base_path: str | None = Field(None, description="Optional base directory path for the report files")

  @classmethod
  def from_list(cls, data: List[dict], base_path: str | None = None) -> "ChinaAnnualReportList":
    """
    Create ChinaAnnualReportList from a list of dictionaries.

    Args:
      data: List of company data dictionaries
      base_path: Optional base directory path for the report files

    Returns:
      ChinaAnnualReportList instance
    """
    companies = [CompanyAnnualReports(**company) for company in data]
    return cls(companies=companies, base_path=base_path)

  @classmethod
  def from_file(cls, file_path: str | Path, base_path: str | None = None) -> "ChinaAnnualReportList":
    """
    Create ChinaAnnualReportList from a JSON file.

    Args:
      file_path: Path to the JSON file containing company data
      base_path: Optional base directory path for the report files

    Returns:
      ChinaAnnualReportList instance

    Raises:
      FileNotFoundError: If the file doesn't exist
      json.JSONDecodeError: If the file is not valid JSON
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
      data = json.load(f)
    return cls.from_list(data, base_path=base_path)
