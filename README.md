# PromEx

## Introduction

Prometheus is an open-source monitoring and alerting toolkit that provides a flexible and powerful way to monitor systems and applications. FastAPI, on the other hand, is a Python web framework that offers high performance, easy-to-use features for building APIs.

This repository explores the integration of Prometheus monitoring into FastAPI applications, allowing you to collect metrics about your API's performance, resource usage, and other important aspects.

## Installation

To run the experiments in this repository, you'll need to have Python and pip installed. Follow these steps to set up the project:

1. Create a virtual environment (optional but recommended):
```bash
python3 -m venv env
source env/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run the experiments, execute the following command:

```bash
uvicron main:app --reload
```

Once the application is running, you can access the Prometheus metrics endpoint at http://localhost:8000/metrics. This endpoint provides various metrics related to your FastAPI application, such as request duration, HTTP status codes, and more.