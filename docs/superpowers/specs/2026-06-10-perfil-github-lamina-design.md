# Design: Redesign do perfil GitHub (RTzinh/RTzinh) — direção "Lâmina"

**Data:** 2026-06-10 · **Status:** aprovado (brainstorm com companion visual)

## Contexto e problema

O README atual tem banner cinematográfico (samurai na chuva) que o usuário **quer manter** — "gostei da cinematografia". Três problemas foram confirmados pelo usuário:

1. **Caixas pretas:** os SVGs dinâmicos (typing, streak, activity graph) usam fundo `#010409`, mas o GitHub dark é `#0d1117` — sobram retângulos com emenda visível. No tema claro viram blocos pretos.
2. **Hierarquia invertida:** os 4 projetos (conteúdo nº 1 para recrutador) são bullets de uma linha, enquanto estatísticas ganham cards grandes.
3. **Duas linguagens visuais:** skillicons coloridos brigando com o resto monocromático.

## Objetivo e público

- **Público:** recrutadores — o perfil é um currículo vivo.
- **Idioma:** inglês.
- **Identidade:** assumir o "dark cinematográfico" do banner como sistema único, com acento vermelho dosado — direção **"Lâmina"** (escolhida entre Lâmina / Aço / Filme P&B).

## Tokens de design

| Token | Tema dark | Tema light |
|---|---|---|
| Acento (títulos de projeto, detalhes) | `#f85149` | `#cf222e` (texto) / `#da3633` (formas e badges) |
| Texto primário | `#e6edf3` | `#24292f` |
| Texto secundário | `#8b949e` | `#57606a` |
| Bordas | `#30363d` | `#d0d7de` |
| Fundo de cards | transparente (`rgba(255,255,255,0.015)` no SVG dark; `rgba(0,0,0,0.012)` no light) | idem |

**Regra de dosagem:** vermelho só em destaques — typing text, títulos dos cards de projeto, fio lateral dos cards, badge Live Demo, rótulos de categoria do stack, acentos dos stats e linha do gráfico. Nunca em texto corrido.

## Estrutura do README (6 seções)

1. **HERO** — `assets/banner.gif` intocado; typing-svg com fundo transparente e texto vermelho, ciclando 3 frases: "Full-Stack Developer", "Data & AI", "Turning data into decisions"; nome; badges `for-the-badge`: GitHub e Email em cinza-escuro `#161b22`, **Live Demo em vermelho `#da3633` — único CTA vermelho do hero**.
2. **ABOUT** — 3–4 linhas de markdown puro com negritos: dev full-stack focado em dados e IA; Development Intern @ IEV; estudante de ADS; e-mail. Sem cor custom (limitação do GitHub, aceita pelo usuário).
3. **FEATURED PROJECTS** (seção estrela) — tabela HTML 2×2; cada célula: `<a href="repo"><picture>…<img card SVG></picture></a>`. Badge vermelho `▶ LIVE DEMO` clicável abaixo do card do Sales Analytics.
4. **TECH STACK** — uma linha por categoria: badge-rótulo vermelho (`LANGUAGES`, `FRAMEWORKS`, `DATA & AI`, `TOOLS`) seguido de badges shields.io `flat-square` fundo `#161b22` com logo branco. Sai o skillicons.
5. **STATS** — streak + github-stats lado a lado, activity graph abaixo; todos com fundo transparente e acentos vermelhos; todos embrulhados em `<picture>` com variantes dark/light.
6. **FOOTER** — citação curta com ⚔️ + contador de views komarev discreto (cinza).

Cabeçalhos de seção em markdown puro (`###`) e divisores `---` padrão — o ritmo vermelho vem dos assets, não dos cabeçalhos.

## Cards SVG de projeto (especificação)

- **Dimensão:** 400×140, `viewBox="0 0 400 140"`.
- **Arquivos:** `assets/cards/<slug>-dark.svg` e `<slug>-light.svg` — 4 projetos × 2 temas = 8 arquivos.
- **Anatomia:** retângulo de borda `rx=8`; fio vermelho vertical 3px à esquerda; título 16px bold vermelho com emoji; `↗` cinza no canto superior direito (affordance de clique); descrição em 2 linhas 12px; chips de tech (rect `rx=10.5`, contorno na cor de borda, texto 10px).
- **Fontes:** `'Segoe UI',Ubuntu,sans-serif` — fontes de sistema apenas (SVG servido via `<img>` não carrega fontes externas).
- **Protótipo aprovado:** ver `design-completo.html` e `svg-cards.html` na sessão de brainstorm (`rt/.superpowers/brainstorm/deno-1781063297/content/`).

| Projeto | Emoji | Descrição (2 linhas) | Chips | Extra |
|---|---|---|---|---|
| Sales Analytics Dashboard | 📊 | AI-powered dashboard turning spreadsheets into KPIs and interactive charts. | Python · Streamlit · Gemini | badge ▶ LIVE DEMO abaixo |
| Investe Bem Brasil | 📈 | Full-stack investment intelligence platform with real-time tracking. | React · FastAPI · Docker | — |
| MedIA | 🩺 | Multimodal clinical AI assistant for triage, exam reading and automated reports. | Streamlit · Llama 3 · Gemini | — |
| RetailRocket Top-N | 🛒 | Top-N recommendation engine for e-commerce built on real user behavior. | Python · Machine Learning | — |

Links dos repositórios: `amazon_sales_analysis`, `investe-bem-brasil`, `MedIATCC`, `retailrocket-topn`. Live demo: app do Streamlit já usado no README atual.

## Restrições técnicas (GitHub README)

- GitHub **remove atributos `style` e CSS inline** do markdown — cor só existe dentro de SVG, badges e emoji.
- SVG via `<img>`: **um link por imagem** — o card inteiro clica para o repo; demo é badge separado.
- Suporte a tema: `<picture><source media="(prefers-color-scheme: dark)" srcset="…-dark.svg"><img src="…-light.svg"></picture>` para **todos** os SVGs (estáticos e dinâmicos).

## Serviços externos (parâmetros-chave)

- **Typing:** `readme-typing-svg.demolab.com` — `background=00000000`, `color` vermelho conforme tema.
- **Streak:** `streak-stats.demolab.com` — `background=00000000`, `hide_border=true`, cores por tema.
- **Stats:** `github-readme-stats.vercel.app` — `bg_color=00000000`, `hide_border=true`.
- **Graph:** `github-readme-activity-graph.vercel.app` — `bg_color=transparent`, linha/pontos vermelhos.
- **Badges:** `img.shields.io`.

## O que sai do README atual

- Bloco skillicons colorido; todos os parâmetros de fundo `#010409`; lista de bullets dos projetos; cabeçalhos duplicados "Statistics" / "Contribution Graph" (consolidados em "Stats").

## Fora de escopo

- Otimizar o `banner.gif` (2,5 MB) — anotado como melhoria futura.
- Versão em português do README.
- Mudanças nos repositórios dos projetos (descrições, pins).

## Critérios de aceite

1. Nenhuma caixa preta/emenda visível nos temas dark **e** light.
2. Projetos em grade 2×2 como primeira seção forte de conteúdo após o About.
3. Uma única linguagem visual — sem skillicons coloridos, badges num estilo só.
4. Banner intocado.
5. README renderiza corretamente no GitHub real (sem depender de CSS inline).

## Verificação

Após push: conferir `github.com/RTzinh` com tema dark e light (e largura mobile). Os SVGs dos cards podem ser pré-validados abrindo localmente no navegador antes do push.

## Revisão v2 (2026-06-10, pós-publicação — feedback do usuário)

1. **Variante única universal no lugar de `<picture>` dark/light.** Descoberta: `prefers-color-scheme` segue o tema do **SO/navegador**, não o tema configurado no GitHub. Com GitHub dark + Windows claro, o navegador servia as variantes light (texto escuro) sobre página escura — tudo ilegível. Solução: uma única variante com cores legíveis nos dois fundos — acento `#e5534b`, texto `#8b949e`, borda `#30363d`. Cards agora são `assets/cards/<slug>.svg` (4 arquivos, sem sufixo de tema); typing/streak/stats/graph com essas mesmas cores, sem `<picture>`.
2. **Live Demo monocromático.** O badge vermelho do hero destoava — voltou a `#161B22` com logo branco, idêntico aos demais (vermelho fica nos rótulos do stack, acentos dos cards e stats).
3. **Cards de projeto idênticos.** Removido o badge `▶ LIVE DEMO` sob o card do Sales Analytics, que quebrava a igualdade da grade. O demo continua acessível pelo badge do hero.
4. **Tech Stack em tabela.** As linhas de badges centralizadas tinham espaçamento irregular; viraram tabela HTML com rótulos à direita e badges à esquerda.
