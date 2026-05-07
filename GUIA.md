# 🚀 Guia de Uso — Como rodar e disparar os testes

---

## 1. Pré-requisitos

Antes de tudo, garanta que você tem instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/) (qualquer versão recente)
- [Git](https://git-scm.com/)
- [GitHub CLI](https://cli.github.com/) *(opcional, para disparar Actions pelo terminal)*

---

## 2. Rodando na sua máquina

### Clone e instale

```bash
git clone https://github.com/WarneyRego/Teste-Qualidade-CICD.git
cd Teste-Qualidade-CICD

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Rodar testes de API

```bash
# Todos os testes de API
PYTHONPATH=. pytest api_tests/ -v

# Módulo específico
PYTHONPATH=. pytest api_tests/tests/test_pet.py -v
PYTHONPATH=. pytest api_tests/tests/test_store.py -v
PYTHONPATH=. pytest api_tests/tests/test_user.py -v

# Com relatório HTML
PYTHONPATH=. pytest api_tests/ -v -p reporter --custom-html=reports/api-report.html --custom-html-title="API Tests — Petstore"
```

### Rodar testes Web

```bash
# Fluxo E2E completo (abre o Chrome visualmente)
PYTHONPATH=. pytest web_tests/ -v

# Modo headless (igual ao CI, sem abrir o browser)
CI=true PYTHONPATH=. pytest web_tests/ -v

# Com relatório HTML
PYTHONPATH=. pytest web_tests/ -v -p reporter --custom-html=reports/web-report.html --custom-html-title="Web Tests — SauceDemo"
```

> **Dica:** o relatório gerado fica em `reports/`. Para visualizá-lo, abra o arquivo `.html` direto no browser.

---

## 3. Disparando as GitHub Actions

### Opção A — Pelo site do GitHub (mais fácil)

1. Acesse o repositório: [github.com/WarneyRego/Teste-Qualidade-CICD](https://github.com/WarneyRego/Teste-Qualidade-CICD)
2. Clique na aba **Actions**
3. No menu lateral, escolha o workflow:
   - `API Tests — Petstore`
   - `Web Tests — SauceDemo`
4. Clique em **Run workflow** → **Run workflow** (botão verde)

> As pipelines também disparam automaticamente a cada `push` ou `pull request` na branch `main`.

---

### Opção B — Pelo terminal com GitHub CLI

Instale o GitHub CLI se ainda não tiver:

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Autentique
gh auth login
```

Dispare os workflows:

```bash
# Disparar testes de API
gh workflow run api-tests.yml --repo WarneyRego/Teste-Qualidade-CICD

# Disparar testes Web
gh workflow run web-tests.yml --repo WarneyRego/Teste-Qualidade-CICD
```

Acompanhe em tempo real:

```bash
# Ver as últimas execuções
gh run list --repo WarneyRego/Teste-Qualidade-CICD

# Assistir a execução ao vivo (use o ID da run)
gh run watch <run-id> --repo WarneyRego/Teste-Qualidade-CICD
```

Baixe o relatório HTML gerado pelo CI:

```bash
# Lista os artefatos da última run
gh run download <run-id> --repo WarneyRego/Teste-Qualidade-CICD
```

---

### Opção C — Push na branch main (automático)

Qualquer commit na `main` já dispara os dois workflows automaticamente:

```bash
git add .
git commit -m "sua mensagem"
git push origin main
```

---

## 4. Verificando o resultado

| Onde | O que ver |
|------|-----------|
| GitHub → Actions | Status ✅ / ❌ de cada pipeline |
| Aba de cada run → Artifacts | Baixar `api-test-report` ou `web-test-report` |
| `reports/*.html` (local) | Abrir no browser após rodar localmente |
| Links no README | Ver relatório online via raw.githack.com |
