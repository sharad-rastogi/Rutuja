# Sauce Demo UI Automation

Python UI tests for [Sauce Demo](https://www.saucedemo.com), using Playwright's synchronous API and pytest. The suite focuses on the required login, sorting, cart, and checkout flows.

## Setup

Python 3.10 or later, Git, and an internet connection are required. From the project root:

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
$env:SAUCE_USERNAME = "<Sauce Demo username>"
$env:SAUCE_PASSWORD = "<Sauce Demo password>"
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
export SAUCE_USERNAME="<Sauce Demo username>"
export SAUCE_PASSWORD="<Sauce Demo password>"
```

The browser can be changed to Firefox or WebKit after installing that browser with `python -m playwright install firefox` or `python -m playwright install webkit`.

## Running tests

The full suite runs in parallel and creates reports and test artifacts with one command:

```powershell
.\run_tests.ps1
```

```bash
./run_tests.sh
```

The equivalent direct pytest command is `python -m pytest`. Useful targeted runs:

```bash
python -m pytest tests/test_login.py::test_valid_login_lands_on_inventory
python -m pytest -m smoke
python -m pytest -m regression
python -m pytest --browser firefox
python -m pytest --headed
```

Configuration can be supplied through the `SAUCE_BASE_URL`, `SAUCE_USERNAME`, and `SAUCE_PASSWORD` environment variables or the `--base-url`, `--username`, and `--password` pytest options. Supply the demo credentials provided with the assessment; they are not stored in this repository. Browser and headed mode are available through pytest-playwright's `--browser` and `--headed` options; `PLAYWRIGHT_BROWSER` and `PLAYWRIGHT_HEADED=true` can set defaults. `PLAYWRIGHT_HEADLESS=false` is also accepted.

The Azure pipeline expects `SAUCE_USERNAME` and `SAUCE_PASSWORD` to be configured as pipeline variables, with the password marked secret. Do not commit credentials or browser authentication state.

## Framework design

- `pages/` contains focused page objects for login, inventory, cart, and checkout. Page objects keep page-specific locators and actions together; tests retain the business assertions.
- `conftest.py` exposes page-object fixtures and the configuration options.
- Playwright's test-id selector is configured to use Sauce Demo's `data-test` attributes.
- Login tests use the `no_auth` marker and start with a fresh context. Other tests create one authenticated storage-state file per pytest-xdist worker and use it to start each test with a clean, logged-in context. The file is created under pytest's worker-specific temporary directory, not in the repository. This avoids shared-file races and prevents one test's cart changes from leaking to another.
- `pytest.ini` defines smoke/regression markers, runs tests in parallel, and configures JUnit, self-contained HTML, and Playwright's retain-on-failure trace, screenshot, and video modes.

## Reports and debugging

`reports/junit.xml` and `reports/report.html` are generated on each run. Failure screenshots, traces, and videos are written under `test-results/`; successful-test artifacts are discarded by Playwright. Open a failed test's trace with:

```bash
python -m playwright show-trace test-results/<trace-file>.zip
```

`sample-reports/` contains the reports from one successful local run.

## Azure Pipelines

`azure-pipelines.yml` runs for pushes and pull requests. It selects Python, installs the pinned dependencies and Chromium, runs the same test script, publishes JUnit results with `PublishTestResults@2`, and publishes the HTML report and failure artifacts even when tests fail. The `useSelfHosted`, `selfHostedPool`, and `vmImage` parameters select either a self-hosted pool or a Microsoft-hosted image. A self-hosted agent must have a compatible Python tool cache and the system libraries needed by Playwright.

## Assumptions and limitations

- The suite targets Sauce Demo's current UI and uses its accessible labels and `data-test` attributes where available.
- The pipeline example runs Chromium on Linux. Browser-specific matrix runs, Allure, and container support are intentionally out of scope.
- The application is an external demo site, so local and CI runs require network access.

## Possible next steps

Add a browser matrix, make artifact retention configurable, and add a small set of deterministic tests against a controlled test deployment if the application under test becomes configurable.

## AI usage

GitHub Copilot was used to help draft and review the test framework, pipeline, and documentation. The repository owner should review the implementation and be prepared to explain and modify each part during the follow-up discussion.
