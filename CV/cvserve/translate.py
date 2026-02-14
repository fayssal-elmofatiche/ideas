"""CV translation from English to German via Claude API."""

import os
import sys

import yaml

from .utils import CACHE_FILE, OUTPUT_DIR, load_cv


def translate_cv(cv: dict, retranslate: bool = False) -> dict:
    """Translate CV content from English to German using Claude API.
    Uses cached translation if available, unless retranslate is True."""
    if not retranslate and CACHE_FILE.exists():
        print(f"Using cached translation from {CACHE_FILE}")
        return load_cv(CACHE_FILE)

    try:
        import anthropic
    except ImportError:
        print("Error: 'anthropic' package required for translation. Install with: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        if CACHE_FILE.exists():
            print("ANTHROPIC_API_KEY not set — falling back to cached translation.")
            return load_cv(CACHE_FILE)
        print("Error: ANTHROPIC_API_KEY not set and no cached translation found.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    cv_yaml = yaml.dump(cv, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print("Translating CV to German via Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": (
                    "Translate the following CV from English to German. "
                    "Return ONLY the translated YAML — no explanation, no code fences. "
                    "Keep the YAML structure and keys exactly the same (keys stay in English). "
                    "Translate all values that are natural language text (descriptions, bullets, titles, skills, etc.). "
                    "Do NOT translate: names, organization names, technology/tool names, URLs, email, phone, dates, "
                    "publication titles, degree program names that are commonly kept in English. "
                    "Use professional German suitable for a senior-level CV. "
                    "Here is the YAML:\n\n"
                    f"{cv_yaml}"
                ),
            }
        ],
    )

    translated_yaml = message.content[0].text.strip()
    if translated_yaml.startswith("```"):
        translated_yaml = "\n".join(translated_yaml.split("\n")[1:])
    if translated_yaml.endswith("```"):
        translated_yaml = "\n".join(translated_yaml.split("\n")[:-1])

    translated_cv = yaml.safe_load(translated_yaml)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        yaml.dump(translated_cv, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Cached translation to {CACHE_FILE}")

    return translated_cv
