"""Tailor command — produce a CV variant emphasizing relevant experience for a project/job."""

import re
from pathlib import Path
from typing import Annotated, Optional

import yaml
import typer

from .utils import DEFAULT_YAML, OUTPUT_DIR, load_cv, open_file, convert_to_pdf, get_anthropic_client
from .translate import translate_cv
from .docx_builder import build_docx


def tailor_cv(cv: dict, description_text: str) -> dict:
    """Use Claude API to tailor the CV for a specific project/job description.

    Claude reorders experience by relevance, rewrites the profile summary,
    and foregrounds matching skills. It does NOT invent content — only
    reorganizes and emphasizes existing data.
    """
    client = get_anthropic_client()

    cv_yaml = yaml.dump(cv, allow_unicode=True, default_flow_style=False, sort_keys=False)

    typer.echo("Tailoring CV via Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a professional CV consultant. Given a CV in YAML format and a project/job description, "
                    "produce a tailored version of the CV that highlights the most relevant experience and skills.\n\n"
                    "Rules:\n"
                    "- Return ONLY the tailored YAML — no explanation, no code fences.\n"
                    "- Keep the exact same YAML structure and keys.\n"
                    "- Do NOT invent, fabricate, or add any new content that isn't in the original CV.\n"
                    "- Rewrite the profile summary to emphasize relevance to the description.\n"
                    "- Reorder the experience entries so the most relevant ones come first.\n"
                    "- For each experience entry, you may reorder bullets to foreground relevant ones.\n"
                    "- You may slightly rephrase bullets to better highlight relevance, but do not change facts.\n"
                    "- Keep all experience entries — do not remove any.\n"
                    "- Reorder skills to foreground the most relevant ones.\n"
                    "- Keep education, certifications, publications, volunteering, and references unchanged.\n\n"
                    f"PROJECT/JOB DESCRIPTION:\n{description_text}\n\n"
                    f"CV YAML:\n{cv_yaml}"
                ),
            }
        ],
    )

    tailored_yaml = message.content[0].text.strip()
    if tailored_yaml.startswith("```"):
        tailored_yaml = "\n".join(tailored_yaml.split("\n")[1:])
    if tailored_yaml.endswith("```"):
        tailored_yaml = "\n".join(tailored_yaml.split("\n")[:-1])

    return yaml.safe_load(tailored_yaml)


def _slugify(text: str, max_len: int = 30) -> str:
    """Create a filesystem-safe slug from text."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "_", slug).strip("_")
    return slug[:max_len]


def tailor(
    description_file: Annotated[Path, typer.Argument(help="Path to a .txt or .md file with the project/job description.")],
    lang: Annotated[Optional[str], typer.Option(help="Output language (en or de). Default: en.")] = "en",
    source: Annotated[Path, typer.Option(help="Path to source YAML.")] = DEFAULT_YAML,
    pdf: Annotated[bool, typer.Option("--pdf", help="Also generate PDF.")] = False,
    open: Annotated[bool, typer.Option("--open/--no-open", help="Open the generated file.")] = True,
):
    """Produce a tailored CV variant for a specific project or job description."""
    if not description_file.exists():
        typer.echo(f"Error: File not found: {description_file}", err=True)
        raise typer.Exit(1)

    description_text = description_file.read_text(encoding="utf-8").strip()
    if not description_text:
        typer.echo("Error: Description file is empty.", err=True)
        raise typer.Exit(1)

    # Load and tailor the EN CV
    cv_en = load_cv(source)
    tailored_cv = tailor_cv(cv_en, description_text)

    # Translate if needed
    if lang == "de":
        tailored_cv = translate_cv(tailored_cv, retranslate=True)

    # Build the docx — use a custom output filename
    slug = _slugify(description_file.stem)
    output_path = build_docx(tailored_cv, lang)

    # Rename to tailored filename
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tailored_filename = f"Fayssal_El_Mofatiche_CV_{lang.upper()}_tailored_{slug}.docx"
    tailored_path = OUTPUT_DIR / tailored_filename
    output_path.rename(tailored_path)

    typer.echo(f"Generated: {tailored_path}")

    outputs = [tailored_path]
    if pdf:
        pdf_path = convert_to_pdf(tailored_path)
        typer.echo(f"Generated: {pdf_path}")
        outputs.append(pdf_path)

    if open:
        for p in outputs:
            open_file(p)
