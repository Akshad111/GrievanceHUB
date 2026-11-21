<div align="center">

# GrievanceHUB

**Consumer grievance redressal for power distribution utilities**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Built and maintained by [Akshad Dhamgaye](https://github.com/Akshad111)*

</div>

---

## Overview

GrievanceHUB implements the consumer complaint lifecycle of a power distribution utility as a web application, modeled on the MSEDCL (Maharashtra State Electricity Distribution Co. Ltd. / Mahavitaran) grievance workflow.

A complaint is registered against a consumer/CA number, categorised by fault type, routed to a subdivision officer under role-based access, and tracked through a defined status lifecycle from `registered` to `resolved`. Every transition is recorded, producing a complete audit trail per complaint.

The grievance process is modeled as a state machine with explicit role boundaries, not a generic ticketing queue. That is the shape the domain actually takes: complaints keyed to a consumer identity, routed by fault category, resolved by the subdivision desk that owns the connection.

---

## Features

| | |
|---|---|
| **Registration** | Complaints keyed to consumer/CA number; unique complaint ID on submission |
| **Categorisation** | Five fault categories — billing, metering, outage, voltage, new connection |
| **Lifecycle** | registered → assigned → in-progress → resolved |
| **Access control** | Three roles — consumer, subdivision officer, admin |
| **Officer dashboard** | Open complaints per logged-in officer |
| **Audit trail** | Every state transition logged with timestamp and actor |

---

## Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11 · Flask 3.0 |
| **Database** | SQLite 3 |
| **Frontend** | HTML · CSS · Bootstrap 5 |
| **Auth** | Session-based |

---

## Architecture

~~~
GrievanceHUB/
  app.py              # application entry point and routes
  models.py           # database models
  templates/          # Jinja2 HTML templates
  static/             # CSS, JS
  requirements.txt    # dependencies
  LICENSE             # MIT license
  README.md           # this file
~~~

### Data model

SQLite database with tables for consumers, complaints, officers, and a status log recording each complaint's state transitions.

---

## Roles

| Role | Capabilities |
|---|---|
| **Consumer** | Register a complaint; view own complaints and their status |
| **Subdivision Officer** | View assigned complaints; update status; resolve |
| **Admin** | View all complaints; assign officers; manage categories |

---

## Quick start

```bash
git clone https://github.com/Akshad111/GrievanceHUB.git
cd GrievanceHUB

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
