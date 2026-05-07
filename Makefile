REPO = WarneyRego/Teste-Qualidade-CICD

test-api:
	PYTHONPATH=. python3 -m pytest api_tests/ -v -p reporter --custom-html=reports/api-report.html --custom-html-title="API Tests — Petstore"

test-web:
	PYTHONPATH=. python3 -m pytest web_tests/ -v -p reporter --custom-html=reports/web-report.html --custom-html-title="Web Tests — SauceDemo"

test-all: test-api test-web

ci-api:
	gh workflow run api-tests.yml --repo $(REPO)

ci-web:
	gh workflow run web-tests.yml --repo $(REPO)

ci-all: ci-api ci-web

run-all: test-all ci-all

status:
	gh run list --limit 5 --repo $(REPO)
