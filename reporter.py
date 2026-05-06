import os
import time
from datetime import datetime
from pathlib import Path

import pytest


class TestReport:
    def __init__(self, title: str, output_path: str):
        self.title = title
        self.output_path = output_path
        self.results = []
        self.start_time = time.time()
        self.suite_name = ""

    def add_result(self, report):
        if report.when != "call" and not (report.when == "setup" and report.failed):
            return
        self.results.append({
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": getattr(report, "duration", 0),
            "stdout": getattr(report, "capstdout", "") or "",
            "longrepr": str(report.longrepr) if report.failed else "",
        })

    def generate(self):
        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        duration = time.time() - self.start_time
        total   = len(self.results)
        passed  = sum(1 for r in self.results if r["outcome"] == "passed")
        failed  = sum(1 for r in self.results if r["outcome"] == "failed")
        skipped = sum(1 for r in self.results if r["outcome"] == "skipped")
        pass_pct = round((passed / total * 100) if total else 0)

        rows = ""
        for i, r in enumerate(self.results):
            cls = r["outcome"]
            badge = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP"}.get(cls, cls.upper())
            dur = f"{r['duration']:.3f}s"
            parts = r["nodeid"].split("::")
            module = parts[0].replace("\\", "/")
            test   = "::".join(parts[1:]) if len(parts) > 1 else module

            log_html = ""
            stdout = r.get("stdout", "").strip()
            longrepr = r.get("longrepr", "").strip()

            if stdout:
                safe_out = stdout.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                log_html += f'<div class="log-section"><div class="log-label">📋 Logs</div><pre class="log-output">{safe_out}</pre></div>'
            if longrepr:
                safe_err = longrepr.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                log_html += f'<div class="log-section"><div class="log-label">❌ Traceback</div><pre class="traceback">{safe_err}</pre></div>'

            detail = ""
            if log_html:
                detail = f'<tr class="detail-row" id="detail-{i}"><td colspan="4"><div class="detail-wrap">{log_html}</div></td></tr>'

            rows += f"""
            <tr class="result-row {cls}" onclick="toggle({i})">
              <td class="col-badge"><span class="badge {cls}">{badge}</span></td>
              <td class="col-module">{module}</td>
              <td class="col-test">{test}</td>
              <td class="col-dur">{dur} <span class="expand-hint">{'▼' if log_html else ''}</span></td>
            </tr>{detail}"""

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{self.title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
:root {{
  --bg:       #05070c;
  --s1:       #090d14;
  --s2:       #0d1320;
  --border:   #162030;
  --border2:  #1e2f45;
  --accent:   #00c8ff;
  --acc2:     #007fa3;
  --pass:     #00e676;
  --pass-d:   rgba(0,230,118,.12);
  --pass-b:   rgba(0,230,118,.3);
  --fail:     #ff3d57;
  --fail-d:   rgba(255,61,87,.12);
  --fail-b:   rgba(255,61,87,.3);
  --skip:     #455a64;
  --text:     #a0b4c8;
  --muted:    #4a6075;
  --head:     #ddeeff;
  --mono:     'JetBrains Mono', monospace;
  --display:  'Syne', sans-serif;
  --radius:   10px;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 100% 35% at 50% 0, rgba(0,200,255,.06) 0%, transparent 70%);
  color: var(--text);
  font-family: var(--mono);
  font-size: 13px;
  min-height: 100vh;
}}

/* ── HEADER ── */
.header {{
  padding: 3rem 3rem 2.5rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(160deg, var(--s2) 0%, var(--s1) 100%);
  position: relative;
  overflow: hidden;
}}
.header::after {{
  content: '{pass_pct}%';
  position: absolute;
  right: 3rem;
  top: 50%;
  transform: translateY(-50%);
  font-family: var(--display);
  font-size: clamp(5rem, 14vw, 11rem);
  font-weight: 800;
  color: rgba(0,200,255,.04);
  letter-spacing: -.05em;
  pointer-events: none;
  user-select: none;
  line-height: 1;
}}
.header-eyebrow {{
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: .6rem;
}}
.header h1 {{
  font-family: var(--display);
  font-size: clamp(1.8rem, 4vw, 3.2rem);
  font-weight: 800;
  letter-spacing: -.03em;
  line-height: 1.1;
  background: linear-gradient(120deg, var(--accent) 0%, #80e8ff 40%, var(--head) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.header-meta {{
  margin-top: .8rem;
  font-size: .7rem;
  color: var(--muted);
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}}
.header-meta span {{ display: flex; align-items: center; gap: .4rem; }}

/* ── STAT CARDS ── */
.stats {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.8rem 3rem;
}}
.stat-card {{
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  position: relative;
  overflow: hidden;
  transition: border-color .2s;
}}
.stat-card:hover {{ border-color: var(--border2); }}
.stat-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}}
.stat-card.total::before  {{ background: var(--accent); }}
.stat-card.pass::before   {{ background: var(--pass); }}
.stat-card.fail::before   {{ background: var(--fail); }}
.stat-card.skip::before   {{ background: var(--skip); }}
.stat-label {{
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: .5rem;
}}
.stat-value {{
  font-family: var(--display);
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -.03em;
}}
.stat-card.total .stat-value {{ color: var(--head); }}
.stat-card.pass  .stat-value {{ color: var(--pass); }}
.stat-card.fail  .stat-value {{ color: var(--fail); }}
.stat-card.skip  .stat-value {{ color: var(--muted); }}
.stat-sub {{
  font-size: .65rem;
  color: var(--muted);
  margin-top: .4rem;
}}

/* ── PROGRESS BAR ── */
.progress-wrap {{
  padding: 0 3rem 1.8rem;
}}
.progress-label {{
  display: flex;
  justify-content: space-between;
  font-size: .65rem;
  color: var(--muted);
  margin-bottom: .5rem;
}}
.progress-track {{
  height: 5px;
  background: var(--border);
  border-radius: 99px;
  overflow: hidden;
}}
.progress-fill {{
  height: 100%;
  width: {pass_pct}%;
  background: linear-gradient(90deg, var(--pass), #80ffcc);
  border-radius: 99px;
  transition: width .8s cubic-bezier(.4,0,.2,1);
}}

/* ── TABLE ── */
.table-wrap {{
  padding: 0 3rem 3rem;
}}
.table-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: .8rem;
  flex-wrap: wrap;
  gap: .5rem;
}}
.table-title {{
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
}}
.filter-btns {{
  display: flex;
  gap: .4rem;
}}
.filter-btn {{
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--muted);
  cursor: pointer;
  font-family: var(--mono);
  font-size: .65rem;
  padding: .25rem .7rem;
  transition: border-color .15s, color .15s;
}}
.filter-btn:hover,
.filter-btn.active {{
  border-color: var(--accent);
  color: var(--accent);
}}
table {{
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}}
thead tr {{
  background: var(--s2);
  border-bottom: 2px solid var(--border2);
}}
th {{
  padding: .75rem 1rem;
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  text-align: left;
}}
.result-row {{
  background: var(--s1);
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background .12s;
}}
.result-row:last-child {{ border-bottom: none; }}
.result-row:hover {{ background: rgba(0,200,255,.03); }}
.result-row td {{ padding: .65rem 1rem; vertical-align: middle; }}
td.col-module {{ color: var(--muted); font-size: .7rem; max-width: 260px; word-break: break-all; }}
td.col-test   {{ color: var(--head);  font-size: .75rem; }}
td.col-dur    {{ color: var(--muted); font-size: .7rem; white-space: nowrap; text-align: right; }}

.badge {{
  display: inline-block;
  font-size: .62rem;
  font-weight: 700;
  letter-spacing: .1em;
  padding: .22rem .65rem;
  border-radius: 4px;
}}
.badge.passed {{
  color: var(--pass);
  background: var(--pass-d);
  border: 1px solid var(--pass-b);
}}
.badge.failed {{
  color: var(--fail);
  background: var(--fail-d);
  border: 1px solid var(--fail-b);
}}
.badge.skipped {{
  color: var(--skip);
  background: rgba(69,90,100,.15);
  border: 1px solid rgba(69,90,100,.3);
}}

.result-row.passed td:first-child {{ border-left: 3px solid var(--pass); }}
.result-row.failed td:first-child {{ border-left: 3px solid var(--fail); }}
.result-row.skipped td:first-child {{ border-left: 3px solid var(--skip); }}

.expand-hint {{
  color: var(--muted);
  font-size: .65rem;
  margin-left: .3rem;
  opacity: .6;
}}

.detail-row {{ display: none; }}
.detail-row td {{ padding: 0 !important; }}

.detail-wrap {{
  border-top: 1px solid var(--border2);
  background: #040609;
}}

.log-section {{ border-bottom: 1px solid var(--border); }}
.log-section:last-child {{ border-bottom: none; }}

.log-label {{
  font-size: .58rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  padding: .5rem 1.2rem .3rem;
  background: rgba(255,255,255,.02);
  border-bottom: 1px solid var(--border);
}}

.log-output {{
  color: #7eb8d4;
  font-family: var(--mono);
  font-size: .72rem;
  line-height: 1.65;
  overflow-x: auto;
  padding: .8rem 1.4rem 1rem;
  white-space: pre-wrap;
  word-break: break-word;
  background: transparent;
  margin: 0;
}}

.traceback {{
  background: transparent;
  color: #e07070;
  font-family: var(--mono);
  font-size: .7rem;
  line-height: 1.6;
  overflow-x: auto;
  padding: .8rem 1.4rem 1rem;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}}

/* hide rows by filter */
.filter-passed  .result-row.passed {{ display: none; }}
.filter-failed  .result-row.failed {{ display: none; }}
.filter-skipped .result-row.skipped {{ display: none; }}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 3px; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-eyebrow">Relatório de Testes Automatizados</div>
  <h1>{self.title}</h1>
  <div class="header-meta">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⏱ {duration:.2f}s total</span>
    <span>🧪 {total} testes</span>
  </div>
</div>

<div class="stats">
  <div class="stat-card total">
    <div class="stat-label">Total</div>
    <div class="stat-value">{total}</div>
    <div class="stat-sub">testes executados</div>
  </div>
  <div class="stat-card pass">
    <div class="stat-label">Passou</div>
    <div class="stat-value">{passed}</div>
    <div class="stat-sub">{pass_pct}% de aprovação</div>
  </div>
  <div class="stat-card fail">
    <div class="stat-label">Falhou</div>
    <div class="stat-value">{failed}</div>
    <div class="stat-sub">{'nenhuma falha' if failed == 0 else 'requer atenção'}</div>
  </div>
  <div class="stat-card skip">
    <div class="stat-label">Pulado</div>
    <div class="stat-value">{skipped}</div>
    <div class="stat-sub">ignorados</div>
  </div>
</div>

<div class="progress-wrap">
  <div class="progress-label">
    <span>Taxa de aprovação</span>
    <span>{pass_pct}%</span>
  </div>
  <div class="progress-track"><div class="progress-fill"></div></div>
</div>

<div class="table-wrap">
  <div class="table-header">
    <span class="table-title">Resultados</span>
    <div class="filter-btns">
      <button class="filter-btn active" onclick="filterAll(this)">Todos</button>
      <button class="filter-btn" onclick="filterOut('passed', this)">Ocultar ✓</button>
      <button class="filter-btn" onclick="filterOut('failed', this)">Ocultar ✗</button>
    </div>
  </div>
  <table id="results">
    <thead>
      <tr>
        <th style="width:90px">Resultado</th>
        <th style="width:260px">Arquivo</th>
        <th>Teste</th>
        <th style="width:80px;text-align:right">Duração</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<script>
function toggle(i) {{
  const d = document.getElementById('detail-' + i);
  if (d) d.style.display = d.style.display === 'table-row' ? 'none' : 'table-row';
}}

let activeFilters = new Set();

function filterAll(btn) {{
  activeFilters.clear();
  document.getElementById('results').className = '';
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}}

function filterOut(cls, btn) {{
  const tbody = document.getElementById('results');
  if (activeFilters.has(cls)) {{
    activeFilters.delete(cls);
    tbody.classList.remove('filter-' + cls);
    btn.classList.remove('active');
  }} else {{
    activeFilters.add(cls);
    tbody.classList.add('filter-' + cls);
    btn.classList.add('active');
  }}
  document.querySelector('[onclick="filterAll(this)"]').classList.toggle(
    'active', activeFilters.size === 0
  );
}}
</script>
</body>
</html>"""
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html)


_reports: dict[str, TestReport] = {}


def pytest_configure(config):
    output = getattr(config.option, "custom_html", None)
    title  = getattr(config.option, "custom_html_title", "Test Report")
    if output:
        _reports[output] = TestReport(title=title, output_path=output)


def pytest_runtest_logreport(report):
    for rep in _reports.values():
        rep.add_result(report)


def pytest_sessionfinish(session, exitstatus):
    for rep in _reports.values():
        rep.generate()


def pytest_addoption(parser):
    parser.addoption("--custom-html", dest="custom_html", default=None,
                     help="Caminho para o relatório HTML customizado")
    parser.addoption("--custom-html-title", dest="custom_html_title",
                     default="Test Report", help="Título do relatório")
