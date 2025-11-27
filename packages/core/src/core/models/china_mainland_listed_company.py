from pydantic import BaseModel, Field
from typing import List
import json
from pathlib import Path


class ChinaMainlandListedCompany(BaseModel):
  """Represents a China mainland listed company."""
  code: str = Field(..., description="Stock code of the company")
  full_name: str = Field(..., description="Full name of the company")
  short_name: str = Field(..., description="Short name of the company")


class AnnualReportFile(BaseModel):
  """Represents a single annual report file for a specific year."""
  year: str = Field(..., description="The year of the annual report")
  file_path: str = Field(..., description="Path to the PDF file")

  @property
  def display_name(self) -> str:
    """
    Returns the filename extracted from the file path.

    Returns:
      The filename portion of the file_path
    """
    return Path(self.file_path).name

  def get_standardized_display_name(self, stock_code: str, short_name: str) -> str:
    """
    Generates a standardized display name for RAGFlow upload.

    Args:
      stock_code: Stock code of the company
      short_name: Short name of the company

    Returns:
      Standardized display name in format: {year}_{stock_code}_{short_name}_年度报告.pdf
    """
    return f"{self.year}_{stock_code}_{short_name}_年度报告.pdf"


class CompanyAnnualReports(BaseModel):
  """Represents all annual reports for a single company."""
  company: ChinaMainlandListedCompany = Field(..., description="Company information")
  files: List[AnnualReportFile] = Field(default_factory=list, description="List of annual report files")

  # Backward compatibility properties
  @property
  def code(self) -> str:
    """Stock code of the company (backward compatibility)."""
    return self.company.code

  @property
  def full_name(self) -> str:
    """Full name of the company (backward compatibility)."""
    return self.company.full_name

  @property
  def short_name(self) -> str:
    """Short name of the company (backward compatibility)."""
    return self.company.short_name

  def get_file_display_name(self, file: AnnualReportFile) -> str:
    """
    Get the standardized display name for a file belonging to this company.

    Args:
      file: The AnnualReportFile to get the display name for

    Returns:
      Standardized display name
    """
    return file.get_standardized_display_name(self.company.code, self.company.short_name)


class ChinaAnnualReportList(BaseModel):
  """Represents a collection of annual reports for multiple companies."""
  companies: List[CompanyAnnualReports] = Field(default_factory=list, description="List of companies with their annual reports")
  base_path: str | None = Field(None, description="Optional base directory path for the report files")

  @classmethod
  def from_list(cls, data: List[dict], base_path: str | None = None) -> "ChinaAnnualReportList":
    """
    Create ChinaAnnualReportList from a list of dictionaries.

    Args:
      data: List of company data dictionaries with flat structure
            (code, full_name, short_name, files at same level)
      base_path: Optional base directory path for the report files

    Returns:
      ChinaAnnualReportList instance
    """
    companies = []
    for company_data in data:
      # Transform flat structure to nested structure
      transformed_data = {
        "company": {
          "code": company_data["code"],
          "full_name": company_data["full_name"],
          "short_name": company_data["short_name"]
        },
        "files": company_data["files"]
      }
      companies.append(CompanyAnnualReports(**transformed_data))

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
