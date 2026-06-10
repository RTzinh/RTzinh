# Redesign "Lâmina" do Perfil GitHub — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reescrever o README do perfil RTzinh/RTzinh na direção "Lâmina" (dark + acento vermelho), com cards SVG próprios para os 4 projetos e suporte a tema dark/light via `<picture>`.

**Architecture:** Um script Python gera os 8 SVGs de card (4 projetos × dark/light) a partir de uma tabela de dados — garante consistência e facilita edição futura. O README é HTML/markdown estático que referencia esses SVGs (via raw.githubusercontent) e serviços externos (typing, streak, stats, graph, shields) com parâmetros de transparência **já validados por curl em 2026-06-10**.

**Tech Stack:** Python 3.12 (stdlib apenas), SVG, GitHub-flavored markdown, shields.io, readme-typing-svg, streak-stats, github-readme-stats, github-readme-activity-graph.

**Spec:** `docs/superpowers/specs/2026-06-10-perfil-github-lamina-design.md`

**Diretório de trabalho:** `C:\Users\ryan.tereciani\Desktop\RTzinh-profile` (clone de https://github.com/RTzinh/RTzinh)

**Descobertas de validação (não mudar esses parâmetros sem retestar):**
- Activity graph: `bg_color=transparent` gera `fill="#transparent"` (INVÁLIDO → renderiza preto). Usar `bg_color=00000000` (gera `fill="#00000000"`, válido).
- Streak-stats: `background=00000000` é IGNORADO (alpha descartado, cai no default `#151515`). Usar `theme=transparent` + overrides de cor (testado: `fill-opacity='0'`).
- github-readme-stats: `bg_color=00000000` funciona (`fill="#00000000"`).
- typing-svg: `background=00000000` é o próprio default transparente do serviço.
- `card_width=400` funciona no streak e no stats (deixa os dois lado a lado em ~830px).

---

### Task 1: Gerador de cards SVG

**Files:**
- Create: `scripts/generate_cards.py`
- Create (gerados): `assets/cards/{sales-analytics,investe-bem-brasil,media,retailrocket-topn}-{dark,light}.svg`

- [ ] **Step 1: Escrever o script gerador**

Criar `scripts/generate_cards.py` com este conteúdo exato:

```python
#!/usr/bin/env python3
"""Gera os cards SVG de projeto (dark/light) em assets/cards/.

Edite PROJECTS e rode:  py -3.12 scripts/generate_cards.py
Anatomia e tokens: docs/superpowers/specs/2026-06-10-perfil-github-lamina-design.md
"""
from pathlib import Path

THEMES = {
    "dark": {
        "fill": "rgba(255,255,255,0.015)",
        "border": "#30363d",
        "accent": "#f85149",
        "title": "#f85149",
        "text": "#8b949e",
        "muted": "#6e7681",
    },
    "light": {
        "fill": "rgba(0,0,0,0.012)",
        "border": "#d0d7de",
        "accent": "#da3633",
        "title": "#cf222e",
        "text": "#57606a",
        "muted": "#8c959f",
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
            path = out_dir / f'{p["slug"]}-{theme_name}.svg'
            path.write_text(render_card(p, t), encoding="utf-8")
            print(f"wrote {path.relative_to(out_dir.parent.parent)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o gerador**

Run (na raiz do repo): `py -3.12 scripts/generate_cards.py`
Expected: 8 linhas `wrote assets\cards\<slug>-<tema>.svg` (4 slugs × dark/light)

- [ ] **Step 3: Validar que os 8 SVGs são XML bem-formado**

Run: `py -3.12 -c "import xml.etree.ElementTree as ET, glob; fs = sorted(glob.glob('assets/cards/*.svg')); [ET.parse(f) for f in fs]; print(len(fs), 'svgs ok')"`
Expected: `8 svgs ok` (qualquer erro de parse explode com ParseError)

- [ ] **Step 4: Commit**

```bash
git add scripts/generate_cards.py assets/cards/
git commit -m "feat: cards SVG de projeto (dark/light) + gerador

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: README novo

**Files:**
- Modify: `README.md` (substituição completa)

- [ ] **Step 1: Substituir o conteúdo de README.md**

Conteúdo completo e exato (as URLs foram validadas — ver "Descobertas de validação" no topo):

````markdown
<div align="center">

<img src="assets/banner.gif" width="100%" alt="banner"/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=600&size=22&pause=1200&color=F85149&background=00000000&center=true&vCenter=true&width=600&height=50&lines=Full-Stack+Developer;Data+%26+AI;Turning+data+into+decisions">
  <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=600&size=22&pause=1200&color=CF222E&background=00000000&center=true&vCenter=true&width=600&height=50&lines=Full-Stack+Developer;Data+%26+AI;Turning+data+into+decisions" alt="Full-Stack Developer · Data & AI · Turning data into decisions"/>
</picture>

# Ryan Tereciani

<a href="https://github.com/RTzinh"><img src="https://img.shields.io/badge/GitHub-161B22?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
<a href="mailto:rtereciani5@gmail.com"><img src="https://img.shields.io/badge/Email-161B22?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://amazonsalesanalysis-dhpqhakxwxwwh3o2tt3q4v.streamlit.app/"><img src="https://img.shields.io/badge/%E2%96%B6_Live_Demo-DA3633?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo"/></a>

</div>

---

### About me

Full-stack developer focused on **data and AI** — I build web apps, BI dashboards and automations that turn raw data into decisions.

- Development Intern @ **IEV – Inteligência em Vendas**
- **Systems Analysis & Development** student
- Reach me: **rtereciani5@gmail.com**

---

### Featured Projects

<table>
  <tr>
    <td align="center" width="50%">
      <a href="https://github.com/RTzinh/amazon_sales_analysis">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/sales-analytics-dark.svg">
          <img src="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/sales-analytics-light.svg" alt="Sales Analytics Dashboard"/>
        </picture>
      </a>
      <br/>
      <a href="https://amazonsalesanalysis-dhpqhakxwxwwh3o2tt3q4v.streamlit.app/"><img src="https://img.shields.io/badge/%E2%96%B6_LIVE_DEMO-DA3633?style=flat-square" alt="live demo"/></a>
    </td>
    <td align="center" width="50%">
      <a href="https://github.com/RTzinh/investe-bem-brasil">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/investe-bem-brasil-dark.svg">
          <img src="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/investe-bem-brasil-light.svg" alt="Investe Bem Brasil"/>
        </picture>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <a href="https://github.com/RTzinh/MedIATCC">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/media-dark.svg">
          <img src="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/media-light.svg" alt="MedIA"/>
        </picture>
      </a>
    </td>
    <td align="center" width="50%">
      <a href="https://github.com/RTzinh/retailrocket-topn">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/retailrocket-topn-dark.svg">
          <img src="https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/retailrocket-topn-light.svg" alt="RetailRocket Top-N"/>
        </picture>
      </a>
    </td>
  </tr>
</table>

---

### Tech Stack

<div align="center">

![LANGUAGES](https://img.shields.io/badge/LANGUAGES-DA3633?style=flat-square) ![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-161B22?style=flat-square&logo=typescript&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-161B22?style=flat-square&logo=javascript&logoColor=white) ![PHP](https://img.shields.io/badge/PHP-161B22?style=flat-square&logo=php&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-161B22?style=flat-square)

![FRAMEWORKS](https://img.shields.io/badge/FRAMEWORKS-DA3633?style=flat-square) ![React](https://img.shields.io/badge/React-161B22?style=flat-square&logo=react&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-161B22?style=flat-square&logo=fastapi&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-161B22?style=flat-square&logo=nodedotjs&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-161B22?style=flat-square&logo=streamlit&logoColor=white)

![DATA & AI](https://img.shields.io/badge/DATA_%26_AI-DA3633?style=flat-square) ![MySQL](https://img.shields.io/badge/MySQL-161B22?style=flat-square&logo=mysql&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-161B22?style=flat-square&logo=pandas&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-161B22?style=flat-square&logo=plotly&logoColor=white) ![Gemini](https://img.shields.io/badge/Gemini-161B22?style=flat-square&logo=googlegemini&logoColor=white) ![Llama 3](https://img.shields.io/badge/Llama_3-161B22?style=flat-square&logo=meta&logoColor=white)

![TOOLS](https://img.shields.io/badge/TOOLS-DA3633?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-161B22?style=flat-square&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-161B22?style=flat-square&logo=git&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-161B22?style=flat-square&logo=linux&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-161B22?style=flat-square)

</div>

---

### Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=RTzinh&theme=transparent&hide_border=true&card_width=400&ring=F85149&fire=F85149&currStreakNum=E6EDF3&currStreakLabel=8B949E&sideNums=E6EDF3&sideLabels=8B949E&dates=8B949E">
  <img src="https://streak-stats.demolab.com/?user=RTzinh&theme=transparent&hide_border=true&card_width=400&ring=DA3633&fire=DA3633&currStreakNum=24292F&currStreakLabel=57606A&sideNums=24292F&sideLabels=57606A&dates=57606A" alt="GitHub streak"/>
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=RTzinh&show_icons=true&hide_border=true&card_width=400&bg_color=00000000&title_color=F85149&icon_color=F85149&text_color=8B949E&ring_color=F85149">
  <img src="https://github-readme-stats.vercel.app/api?username=RTzinh&show_icons=true&hide_border=true&card_width=400&bg_color=00000000&title_color=CF222E&icon_color=DA3633&text_color=57606A&ring_color=DA3633" alt="GitHub stats"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=RTzinh&bg_color=00000000&color=8B949E&line=F85149&point=E6EDF3&area=true&area_color=F85149&hide_border=true">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=RTzinh&bg_color=00000000&color=57606A&line=DA3633&point=24292F&area=true&area_color=DA3633&hide_border=true" alt="Contribution graph"/>
</picture>

</div>

---

<div align="center">

⚔️ *"The path of data is walked one commit at a time."*

<img src="https://komarev.com/ghpvc/?username=RTzinh&color=8B949E&style=flat" alt="profile views"/>

</div>
````

- [ ] **Step 2: Sanity checks do README**

Run: `grep -c "<picture>" README.md`
Expected: `8` (1 typing + 4 cards + streak + stats + graph)

Run: `grep -q "010409\|skillicons" README.md && echo SUJO || echo CLEAN`
Expected: `CLEAN` (nenhum fundo preto antigo, nenhum skillicons)

Run: `grep -c "prefers-color-scheme" README.md`
Expected: `8`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: README redesign 'Lamina' — dark + acento vermelho, cards SVG, tema dark/light

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Verificação visual local (gate do usuário)

**Files:**
- Create: `<sessão companion>/content/verificacao-final.html` (fora do repo — `rt/.superpowers/brainstorm/deno-1781063297/content/`)

- [ ] **Step 1: Montar tela de verificação no companion**

Escrever um fragmento HTML que embute o CONTEÚDO dos 8 SVGs gerados (ler os arquivos de `assets/cards/` e injetar inline): os 4 dark sobre painel `#0d1117` em grade 2×2, os 4 light sobre painel branco. Incluir opções `aprovar` / `ajustar`.

- [ ] **Step 2: Usuário aprova no companion/terminal**

Expected: aprovação explícita do usuário antes de qualquer push. Se houver ajuste (texto, chip, emoji), editar `PROJECTS` em `scripts/generate_cards.py`, rodar de novo (Task 1 Steps 2–3), commitar e repetir.

---

### Task 4: Publicação e verificação ao vivo

- [ ] **Step 1: Push (ação pública — só após o gate da Task 3)**

Run: `git push origin main`
Expected: push aceito; commits de spec/plano/cards/README publicados.

- [ ] **Step 2: Conferir os SVGs servidos pelo raw**

Run: `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/RTzinh/RTzinh/main/assets/cards/sales-analytics-dark.svg`
Expected: `200`

- [ ] **Step 3: Conferir o perfil renderizado**

Fetch de `https://github.com/RTzinh` e confirmar: tabela 2×2 de projetos presente, sem skillicons, stats com tema novo. Usuário confere no navegador nos DOIS temas (Settings → Appearance, ou modo claro/escuro do SO) e na largura mobile.

Critérios de aceite (do spec): sem caixas pretas nos dois temas; projetos em grade 2×2 logo após About; uma única linguagem visual; banner intocado.

- [ ] **Step 4: Encerrar sessão do companion**

Parar o servidor Deno (processo em background `bg123s4rc`) quando o usuário der o OK final.
