# nubank-data-engineer-challenge
Code Challenge: Autorizador
=======
# Nubank Challenge

## About

The program will receive input lines in json format on standard input (stdin) and must provide
one output in json format for each of the inputs on standar output (stdout).

The program must deal with two types of operations, deciding which one to execute according to the line
that is being processed:

1. Account creation
2. Authorizing an account transaction

## Implemented business rules:

* Account not initialized: No transactions should be accepted until the account has been initialized. This violation is indentified by: `account-not-initialized`
* Card not active: No transactions should be accepted when the card is not active. This violation is identified by: `card-not-active`
* Insufficient limit: Transaction amount must not exceed available limit. This violation is identified by: `insufficient-limit`
* High frequency in a small interval: There should be no more than 3 transactions from any merchant in a 2 minute interval. This violation is identified by: `high-frequency-small-interval`
* Doubled transaction: There must be no more than 1 similar transaction (same value and merchant) within 2 minutes. This violation is identified by: `double-transaction`


## Technologies

* Python 3.9.7 (with virtualenv)
* Docker version 20.10.7, build 20.10.7-0ubuntu5.1

## Code Architecture

The project was built using object-oriented concepts. Below, the main classes and their respective function: 

* **BankAccount:** Represents the bank account where transactions will be performed
* **BankStatement:** Used to record and query transactions
* **Authorizer:** Orchestrates the main flow of the authorizer, based on incoming events, applies validations in order to find violations
* **BaseValidation:** Abstract class that represents the basics of a validation. If you want to implement new validations, just implement its abstract methods
* **SomeValidation:** Any concrete class that implements the `BaseValidation` class. It can be provided to the authorizer, through the `Authorizer` class, to be included in the validations

### Project folder structure
 ```bash
.
├── app
│   ├── auth
│   │   ├── authorizer.py
│   │   ├── __init__.py
│   │   └── validation
│   │       ├── base_validation.py
│   │       ├── custom_validation.py
│   │       ├── __init__.py
│   ├── bank
│   │   ├── account.py
│   │   ├── __init__.py
│   │   └── transactions.py
│   ├── __init__.py
│   ├── parse
│   │   ├── __init__.py
│   │   └── io.py
│   └── service
│       ├── __init__.py
│       └── logging
│           ├── __init__.py
│           └── local_logging.py
├── dockerfile
├── project_tree.txt
├── README.md
├── requirements.txt
├── run.py
├── tests
│   ├── app
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── test_authorizer.py
│   │   │   └── validation
│   │   │       ├── __init__.py
│   │   │       ├── test_base_validation.py
│   │   │       └── test_custom_validation.py
│   │   ├── bank
│   │   │   ├── __init__.py
│   │   │   ├── test_account.py
│   │   │   └── test_transactions.py
│   │   ├── parse
│   │   │   ├── __init__.py
│   │   │   └── test_io.py
│   ├── __init__.py
```

## Running

Before starting, you will need to create a json format file with the operations you want to verify. An example of an accepted file:

```bash
$ cat operations.jsonl
{"account": {"active-card": true, "available-limit": 100}}
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
{"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:00:00.000Z"}}
{"transaction": {"merchant": "McDonald's", "amount": 30, "time": "2019-02-13T12:00:00.000Z"}}
```

### Local running
To run outside a containerized environment, being in the project's root directory:

#### Installing requirements
```bash
$ pip3 install -r requirements.txt
```

#### Running tests
```bash
$ pytest tests/
```

#### Executing the code
```bash
$ python3 run.py < operations.jsonl
```

### Running with Docker

### Build

We strongly recommend that you run using docker in order to avoid environmental issues.

Once in the project's root directory, run in the terminal:

**Observation:** Make sure you have the docker installed in your environment.

```bash
$ docker build -t authorizer .
```

This stage is responsible for:

* Python image download
* Installation of pypi dependencies
* Execution of tests
* Code execution

Once you've built your docker container, run the following:

```bash
docker run -i  authorizer < operations.jsonl
```
