"""Build command — generate full CV documents from YAML source."""

import time
from pathlib import Path
from typing import Annotated, Optional

import typer

from .utils import DEFAULT_YAML, load_cv, open_file, convert_to_pdf
from .translate import translate_cv
from .docx_builder import build_docx


def build(
    lang: Annotated[Optional[str], typer.Option(help="Output language (en or de). Omit to generate both.")] = None,
    retranslate: Annotated[bool, typer.Option("--retranslate", help="Force re-translation via Claude API (ignores cache).")] = False,
    source: Annotated[Path, typer.Option(help="Path to source YAML.")] = DEFAULT_YAML,
    pdf: Annotated[bool, typer.Option("--pdf", help="Also generate PDF from the Word documents.")] = False,
    watch: Annotated[bool, typer.Option("--watch", help="Watch the source YAML for changes and auto-rebuild.")] = False,
):
    """Build full CV documents from YAML source."""
    langs = [lang] if lang else ["en", "de"]

    def do_build():
        cv_en = load_cv(source)
        outputs = []
        for l in langs:
            cv = cv_en
            if l == "de":
                cv = translate_cv(cv_en, retranslate=retranslate)
            output_path = build_docx(cv, l)
            outputs.append(output_path)
            if pdf:
                pdf_path = convert_to_pdf(output_path)
                outputs.append(pdf_path)
        return outputs

    # Initial build
    outputs = do_build()
    for output_path in outputs:
        typer.echo(f"Generated: {output_path}")
        open_file(output_path)

    if watch:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class RebuildHandler(FileSystemEventHandler):
            def __init__(self):
                self._last_build = 0

            def on_modified(self, event):
                if event.is_directory:
                    return
                if Path(event.src_path).resolve() != source.resolve():
                    return
                now = time.time()
                if now - self._last_build < 1:
                    return
                self._last_build = now
                typer.echo(f"\n--- {source.name} changed, rebuilding... ---")
                try:
                    outs = do_build()
                    for out in outs:
                        typer.echo(f"Generated: {out}")
                except Exception as e:
                    typer.echo(f"Build error: {e}")

        observer = Observer()
        observer.schedule(RebuildHandler(), str(source.parent), recursive=False)
        observer.start()
        typer.echo(f"\nWatching {source} for changes. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            typer.echo("\nStopped watching.")
        observer.join()
