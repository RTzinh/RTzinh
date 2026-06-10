#!/usr/bin/env python3
"""Gera os cards SVG de projeto (dark/light) em assets/cards/.

Edite PROJECTS e rode:  py -3.12 scripts/generate_cards.py
Anatomia e tokens: docs/superpowers/specs/2026-06-10-perfil-github-lamina-design.md
"""
from pathlib import Path

# Variante única com cores universais: legíveis sobre #0d1117 E sobre branco.
# (prefers-color-scheme segue o tema do SO, não o do GitHub — variantes duplas
# quebram quando os dois divergem.)
THEMES = {
    "universal": {
        "fill": "rgba(255,255,255,0.015)",
        "border": "#30363d",
        "accent": "#e5534b",
        "title": "#e5534b",
        "text": "#8b949e",
        "muted": "#8b949e",
    },
}

PROJECTS = [
    {
        "slug": "sales-analytics",
        "title": "📊 Sales Analytics Dashboard",
        "desc": ["AI-powered dashboard turning spreadsheets into", "KPIs and interactive charts."],
        "chips": ["Python", "Streamlit", "Gemini"],
    },
    {
        "slug": "investe-bem-brasil",
        "title": "📈 Investe Bem Brasil",
        "desc": ["Full-stack investment intelligence platform with", "real-time tracking."],
        "chips": ["React", "FastAPI", "Docker"],
    },
    {
        "slug": "media",
        "title": "🩺 MedIA",
        "desc": ["Multimodal clinical AI assistant for triage,", "exam reading and automated reports."],
        "chips": ["Streamlit", "Llama 3", "Gemini"],
    },
    {
        "slug": "retailrocket-topn",
        "title": "🛒 RetailRocket Top-N",
        "desc": ["Top-N recommendation engine for e-commerce", "built on real user behavior."],
        "chips": ["Python", "Machine Learning"],
    },
]

FONT = "'Segoe UI',Ubuntu,sans-serif"


def chip_width(label: str) -> int:
    return 22 + round(len(label) * 5.2)


def render_card(p: dict, t: dict) -> str:
    parts = [
        '<svg width="400" height="140" viewBox="0 0 400 140" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect x="0.5" y="0.5" width="399" height="139" rx="8" fill="{t["fill"]}" stroke="{t["border"]}"/>',
        f'  <rect x="0" y="10" width="3" height="120" rx="1.5" fill="{t["accent"]}"/>',
        f'  <text x="20" y="33" font-family="{FONT}" font-size="16" font-weight="700" fill="{t["title"]}">{p["title"]}</text>',
        f'  <text x="382" y="30" font-family="{FONT}" font-size="13" fill="{t["muted"]}" text-anchor="end">↗</text>',
        f'  <text x="20" y="58" font-family="{FONT}" font-size="12" fill="{t["text"]}">{p["desc"][0]}</text>',
        f'  <text x="20" y="75" font-family="{FONT}" font-size="12" fill="{t["text"]}">{p["desc"][1]}</text>',
        f'  <g font-family="{FONT}" font-size="10">',
    ]
    x = 20
    for chip in p["chips"]:
        w = chip_width(chip)
        parts.append(
            f'    <rect x="{x}" y="98" width="{w}" height="21" rx="10.5" fill="none" stroke="{t["border"]}"/>'
        )
        parts.append(f'    <text x="{x + w / 2:g}" y="112" fill="{t["text"]}" text-anchor="middle">{chip}</text>')
        x += w + 6
    parts.append("  </g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "assets" / "cards"
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        for theme_name, t in THEMES.items():
            path = out_dir / f'{p["slug"]}.svg'
            path.write_text(render_card(p, t), encoding="utf-8")
            print(f"wrote {path.relative_to(out_dir.parent.parent)}")


if __name__ == "__main__":
    main()
