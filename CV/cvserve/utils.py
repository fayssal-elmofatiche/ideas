"""Shared constants, paths, colors, labels, and helpers."""

import os
import platform
import subprocess
import sys
from pathlib import Path

import yaml
from docx.shared import Pt, Cm, RGBColor

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_YAML = BASE_DIR / "cv.yaml"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_FILE = OUTPUT_DIR / ".cv_de_cache.yaml"
ASSETS_DIR = BASE_DIR / "assets"

# ── Colors (matching original CV) ──
NAVY = RGBColor(0x0F, 0x14, 0x1F)       # Sidebar background & name
NAVY_HEX = "0F141F"
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
WHITE_HEX = "FFFFFF"
SLATE = RGBColor(0x7A, 0x85, 0x99)      # Dates, muted text
DARK_TEXT = RGBColor(0x33, 0x33, 0x33)   # Body text
TEAL = RGBColor(0x0A, 0xA8, 0xA7)       # Accent (section headings in main)
TEAL_HEX = "0AA8A7"

# ── Layout ──
SIDEBAR_WIDTH_CM = 5.3
MAIN_WIDTH_CM = 12.7
PAGE_TOP_MARGIN = Cm(1.1)
PAGE_BOTTOM_MARGIN = Cm(1.1)
PAGE_LEFT_MARGIN = Cm(1.4)
PAGE_RIGHT_MARGIN = Cm(1.4)

# ── Section icons ──
SECTION_ICONS = {
    "Profile": "icon_profile.png",
    "Project / Employment History": "icon_experience.png",
    "Education": "icon_education.png",
    "Volunteering": "icon_volunteering.png",
    "Certifications": "icon_certifications.png",
    "Publications": "icon_publications.png",
    "References": "icon_profile.png",
    "Testimonials": "icon_testimonials.png",
}

# ── i18n labels ──
LABELS = {
    "en": {
        "details": "details",
        "nationality": "Nationality",
        "links": "Links",
        "skills": "skills",
        "leadership_skills": "Leadership Skills",
        "languages": "Languages",
        "profile": "Profile",
        "experience": "Project / Employment History",
        "education": "Education",
        "volunteering": "Volunteering",
        "references": "References",
        "certifications": "Certifications",
        "publications": "Publications",
        "testimonials_heading": "WHAT CLIENTS SAY:",
    },
    "de": {
        "details": "Kontakt",
        "nationality": "Nationalität",
        "links": "Links",
        "skills": "Kompetenzen",
        "leadership_skills": "Führungskompetenzen",
        "languages": "Sprachen",
        "profile": "Profil",
        "experience": "Projekt- / Berufserfahrung",
        "education": "Ausbildung",
        "volunteering": "Ehrenamt",
        "references": "Referenzen",
        "certifications": "Zertifizierungen",
        "publications": "Publikationen",
        "testimonials_heading": "WAS KUNDEN SAGEN:",
    },
}

# ── Date parsing for sorting ──

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    # German months
    "januar": 1, "februar": 2, "märz": 3, "mai": 5, "juni": 6,
    "juli": 7, "oktober": 10, "dezember": 12,
}


def parse_start_date(date_str: str) -> tuple:
    """Parse a start date string into (year, month) for sorting. Higher = more recent."""
    parts = date_str.strip().lower().split()
    if len(parts) == 2:
        month_str, year_str = parts
        month = MONTH_MAP.get(month_str, 0)
        try:
            year = int(year_str)
        except ValueError:
            year = 0
        return (year, month)
    if len(parts) == 1:
        try:
            return (int(parts[0]), 0)
        except ValueError:
            return (0, 0)
    return (0, 0)


def load_cv(yaml_path: Path) -> dict:
    """Load CV data from a YAML file."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def open_file(path: Path):
    """Open a file with the system default application."""
    if platform.system() == "Darwin":
        subprocess.Popen(["open", str(path)])
    elif platform.system() == "Windows":
        os.startfile(str(path))
    else:
        subprocess.Popen(["xdg-open", str(path)])


def convert_to_pdf(docx_path: Path) -> Path:
    """Convert a .docx file to PDF."""
    from docx2pdf import convert
    pdf_path = docx_path.with_suffix(".pdf")
    convert(str(docx_path), str(pdf_path))
    return pdf_path


def get_anthropic_client():
    """Get an Anthropic API client, or exit with an error."""
    try:
        import anthropic
    except ImportError:
        print("Error: 'anthropic' package required. Install with: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    return anthropic.Anthropic(api_key=api_key)
