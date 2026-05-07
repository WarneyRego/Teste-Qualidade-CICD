<div align="center">

# 🧪 Teste Qualidade — CI/CD

**Automação de testes completa com API REST + Web E2E, integrada a pipelines de CI/CD no GitHub Actions.**

[![API Tests](https://github.com/WarneyRego/Teste-Qualidade-CICD/actions/workflows/api-tests.yml/badge.svg)](https://github.com/WarneyRego/Teste-Qualidade-CICD/actions/workflows/api-tests.yml)
[![Web Tests](https://github.com/WarneyRego/Teste-Qualidade-CICD/actions/workflows/web-tests.yml/badge.svg)](https://github.com/WarneyRego/Teste-Qualidade-CICD/actions/workflows/web-tests.yml)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.27-43B02A?logo=selenium&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.3.5-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## 📋 Visão Geral

Este projeto implementa **duas suítes de automação independentes**, cada uma com sua própria pipeline de CI/CD:

| Suíte | Alvo | Padrão de Design | Tecnologia |
|-------|------|-----------------|------------|
| 🔌 API | [Petstore Swagger](https://petstore.swagger.io/v2) | Service Object | pytest + requests |
| 🌐 Web | [SauceDemo](https://www.saucedemo.com/) | Page Object Model | pytest + Selenium |

### O que é testado?

**API — Petstore:**
- `Pet` → criar, buscar por status, buscar por ID, atualizar e deletar pets
- `Store` → consultar inventário, criar e buscar pedidos
- `User` → criar, autenticar, buscar, atualizar e deletar usuários

**Web — SauceDemo (E2E):**
- Login com credenciais válidas
- Adição de múltiplos produtos ao carrinho
- Validação dos itens no carrinho
- Preenchimento de dados e finalização do checkout
- Confirmação da compra ("Thank you for your order!")

---

## 🏗️ Arquitetura do Projeto

```
Teste-Qualidade-CICD/
│
├── 📂 api_tests/
│   ├── services/
│   │   ├── pet_service.py       # Service Object → endpoints /pet
│   │   ├── store_service.py     # Service Object → endpoints /store
│   │   └── user_service.py      # Service Object → endpoints /user
│   ├── tests/
│   │   ├── test_pet.py          # Testes CRUD de Pet
│   │   ├── test_store.py        # Testes de inventário e pedidos
│   │   └── test_user.py         # Testes de usuário e autenticação
│   └── conftest.py              # Fixture de sessão HTTP compartilhada
│
├── 📂 web_tests/
│   ├── pages/
│   │   ├── login_page.py        # POM → tela de login
│   │   ├── inventory_page.py    # POM → catálogo de produtos
│   │   ├── cart_page.py         # POM → carrinho de compras
│   │   └── checkout_page.py     # POM → fluxo de checkout
│   ├── tests/
│   │   └── test_e2e_purchase.py # Fluxo E2E completo de compra
│   └── conftest.py              # Fixture do WebDriver (Chrome headless)
│
├── 📂 .github/workflows/
│   ├── api-tests.yml            # Pipeline CI → API
│   └── web-tests.yml            # Pipeline CI → Web
│
├── 📂 reports/
│   ├── api-report.html          # Relatório HTML → API
│   └── web-report.html          # Relatório HTML → Web
│
├── reporter.py                  # Plugin customizado de relatório HTML
└── requirements.txt
```

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11 | Linguagem principal |
| pytest | 8.3.5 | Runner e framework de asserções |
| requests | 2.32.3 | Cliente HTTP para testes de API |
| Selenium | 4.27.1 | Automação de browser (E2E) |
| pytest-html | 4.1.1 | Geração de relatórios HTML |
| GitHub Actions | — | Pipeline de CI/CD |
| Chrome (headless) | latest | Browser para testes Web em CI |

> O **Selenium 4.6+** inclui o `selenium-manager` embutido, que gerencia o ChromeDriver automaticamente — sem dependências extras.

---

## ⚙️ Como Instalar

**Pré-requisitos:** Python 3.11+, Git e Google Chrome instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/WarneyRego/Teste-Qualidade-CICD.git
cd Teste-Qualidade-CICD

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Como Executar

### 🔌 Testes de API

```bash
# Roda toda a suíte
PYTHONPATH=. pytest api_tests/ -v

# Roda por módulo
PYTHONPATH=. pytest api_tests/tests/test_pet.py -v
PYTHONPATH=. pytest api_tests/tests/test_store.py -v
PYTHONPATH=. pytest api_tests/tests/test_user.py -v

# Com relatório HTML customizado
PYTHONPATH=. pytest api_tests/ -v -p reporter --custom-html=reports/api-report.html
```

### 🌐 Testes Web

```bash
# Roda o fluxo E2E completo
PYTHONPATH=. pytest web_tests/ -v

# Com relatório HTML customizado
PYTHONPATH=. pytest web_tests/ -v -p reporter --custom-html=reports/web-report.html
```

---

## 📊 Relatórios HTML

Os testes geram relatórios HTML detalhados na pasta `reports/`, com status de cada teste, logs e duração.

### Visualizar os relatórios

> **O GitHub não renderiza arquivos `.html` diretamente no repositório — mas você pode visualizá-los de duas formas:**

**1. 🌐 Via htmlpreview (sem instalar nada):**

| Relatório | Link |
|-----------|------|
| API Tests | [▶ Abrir relatório API](https://htmlpreview.github.io/?https://raw.githubusercontent.com/WarneyRego/Teste-Qualidade-CICD/main/reports/api-report.html) |
| Web Tests | [▶ Abrir relatório Web](https://htmlpreview.github.io/?https://raw.githubusercontent.com/WarneyRego/Teste-Qualidade-CICD/main/reports/web-report.html) |

**2. 📦 Via artefatos do GitHub Actions:**

Cada execução da pipeline faz upload do relatório como artefato. Para acessar:
1. Vá em **Actions** no repositório
2. Clique na execução desejada
3. Baixe o artefato `api-test-report` ou `web-test-report`

---

## 🔄 CI/CD — GitHub Actions

O projeto possui **dois workflows independentes**, disparados automaticamente em todo `push` ou `pull request` para a branch `main`.

### `api-tests.yml`

```
Push/PR → main
    └── api-tests (ubuntu-latest)
            ├── Checkout do repositório
            ├── Setup Python 3.11
            ├── pip install -r requirements.txt
            ├── pytest api_tests/ → relatório HTML
            └── Upload do relatório como artefato
```

### `web-tests.yml`

```
Push/PR → main
    └── web-tests (ubuntu-latest)
            ├── Checkout do repositório
            ├── Setup Python 3.11
            ├── Instala Chrome (browser-actions/setup-chrome)
            ├── pip install -r requirements.txt
            ├── pytest web_tests/ em modo --headless=new
            └── Upload do relatório como artefato
```

---

## 🧩 Padrões de Design

### Service Object (API)
Cada recurso da API (`Pet`, `Store`, `User`) é encapsulado em uma classe de serviço que centraliza todas as chamadas HTTP. Os testes consomem apenas esses serviços, sem URLs ou headers espalhados pelo código.

### Page Object Model (Web)
Cada tela da aplicação SauceDemo é representada por uma classe (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`). Os seletores e as interações ficam dentro de cada Page Object — os testes descrevem apenas o fluxo de negócio, sem manipular o DOM diretamente.

---

## 📌 Decisões Técnicas

- **`selenium-manager`** (embutido no Selenium 4.6+) substitui o `webdriver-manager`, eliminando falhas de rate limit no CI.
- **`--headless=new`** é usado em CI pois o modo `--headless` legado tem comportamento inconsistente no Chrome 112+.
- **`form.requestSubmit()`** é usado para submeter o formulário de checkout — garante que os event listeners do JavaScript disparem corretamente em ambientes headless Linux.
- **`HTMLInputElement.value` setter nativo** é usado para preencher campos React, garantindo que o estado interno da lib atualize corretamente.

---

<div align="center">

Feito com 🧠 e ☕ · [Warney Rego](https://github.com/WarneyRego)

</div>
