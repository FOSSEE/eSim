# Automated Integration Testing Framework

This module provides automated integration testing for eSim simulations using pytest and ngspice.

---

## Features

- Automated ngspice simulation execution
- Multi-circuit regression testing
- GitHub Actions CI/CD integration
- HTML test report generation
- Parameterized pytest framework

---

## Folder Structure

```text
integration_tests/
testcases/
utils/
reports/
```

---

## Supported Testcases

- RC Circuit
- RL Circuit
- RLC Circuit

---

## Run Tests

Activate virtual environment:

```bash
source venv/bin/activate
```

Run all tests:

```bash
pytest
```

---

## Generate HTML Report

```bash
pytest --html=reports/report.html
```

---

## CI/CD Pipeline

GitHub Actions automatically runs tests on:
- push
- pull requests

Workflow file:

```text
.github/workflows/tests.yml
```

---

## Technologies Used

- Python
- pytest
- ngspice
- GitHub Actions
- pytest-html