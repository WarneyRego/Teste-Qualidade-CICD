# Teste Qualidade — CI/CD

Projeto de automação de testes com duas suítes independentes: testes de API REST e testes Web E2E, integradas a pipelines de CI/CD no GitHub Actions.

---

## Visao Geral

| Suite | Alvo | Framework |
|-------|------|-----------|
| API   | [Petstore Swagger](https://petstore.swagger.io/v2) | pytest + requests |
| Web   | [SauceDemo](https://www.saucedemo.com/) | pytest + Selenium |

Os testes de API cobrem os recursos **Pet**, **Store** e **User** da API Petstore, incluindo cenários de criação, leitura, atualização e exclusão.

O teste Web executa um fluxo E2E completo: login → adição de produtos ao carrinho → checkout → confirmação de compra.

---

## Tecnologias

- **Python 3.11**
- **pytest 8.3.5** — runner e framework de asserções
- **requests 2.32.3** — cliente HTTP para testes de API
- **selenium 4.27.1** — automação de browser
- **webdriver-manager 4.0.2** — gerenciamento automático do ChromeDriver
- **pytest-html 4.1.1** — geração de relatórios HTML

---

## Estrutura de Pastas

```
.
├── api_tests/
│   ├── services/
│   │   ├── pet_service.py       # Service Object para /pet
│   │   ├── store_service.py     # Service Object para /store
│   │   └── user_service.py      # Service Object para /user
│   ├── tests/
│   │   ├── test_pet.py
│   │   ├── test_store.py
│   │   └── test_user.py
│   └── conftest.py              # Fixtures de sessão HTTP
│
├── web_tests/
│   ├── pages/
│   │   ├── login_page.py        # Page Object da tela de login
│   │   ├── inventory_page.py    # Page Object do catálogo de produtos
│   │   ├── cart_page.py         # Page Object do carrinho
│   │   └── checkout_page.py     # Page Object do fluxo de checkout
│   ├── tests/
│   │   └── test_e2e_purchase.py # Teste E2E de compra completa
│   └── conftest.py              # Fixture do WebDriver (Chrome headless)
│
├── .github/
│   └── workflows/
│       ├── api-tests.yml        # Pipeline CI para testes de API
│       └── web-tests.yml        # Pipeline CI para testes Web
│
├── requirements.txt
└── README.md
```

---

## Como Instalar

1. Clone o repositório e entre na pasta:

```bash
git clone https://github.com/seu-usuario/Teste-Qualidade-CICD.git
cd Teste-Qualidade-CICD
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Como Executar

### Testes de API

```bash
pytest api_tests/ -v --html=reports/api-report.html --self-contained-html
```

### Testes Web

```bash
pytest web_tests/ -v --html=reports/web-report.html --self-contained-html
```

Os relatórios HTML ficam salvos na pasta `reports/` após cada execução.

Para rodar uma suíte específica de testes de API:

```bash
pytest api_tests/tests/test_pet.py -v
pytest api_tests/tests/test_store.py -v
pytest api_tests/tests/test_user.py -v
```

---

## CI/CD

O projeto possui dois workflows no GitHub Actions, acionados em todo **push** ou **pull request** para a branch `main`.

### api-tests.yml

1. Configura o Python 3.11 no runner Ubuntu.
2. Instala as dependências do `requirements.txt`.
3. Executa `pytest api_tests/` com saída verbosa e geração de relatório HTML.
4. Faz upload do relatório como artefato no GitHub Actions.

### web-tests.yml

1. Configura o Python 3.11 no runner Ubuntu.
2. Instala o **Google Chrome** via repositório oficial.
3. Instala as dependências do `requirements.txt` (o `webdriver-manager` baixa o ChromeDriver compatível automaticamente).
4. Executa `pytest web_tests/` em modo headless — sem necessidade de display gráfico.
5. Faz upload do relatório HTML como artefato.

Os artefatos ficam disponíveis na aba **Actions** do repositório GitHub, dentro de cada execução de workflow.

---

## Prints

Os prints das execuções dos testes (locais e CI) estão disponíveis no repositório, na pasta `prints/` (a ser adicionada conforme execuções forem realizadas).
