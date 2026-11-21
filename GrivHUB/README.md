# GrievanceHUB

**Author:** Akshad Dhamgaye — [github.com/Akshad111](https://github.com/Akshad111)

An intelligent electricity grievance management system — an academic prototype modeled on the MSEDCL (Maharashtra State Electricity Distribution Co. Ltd. / Mahavitaran) consumer grievance workflow.

> **Status:** Academic prototype. Not commissioned work, not affiliated with MSEDCL. Built to study how consumer complaints in a power distribution utility move through registration, assignment, resolution, and escalation.

---

## What it does

Consumer electricity complaints in a distribution utility follow a defined lifecycle: a consumer raises a billing, metering, outage, voltage, or new-connection complaint against their consumer number; the subdivision officer picks it up; the complaint moves through states until it is resolved; if it is not resolved within a service-level window, it escalates.

GrievanceHUB implements that workflow as a web application.

- **Complaint registration** keyed to consumer number / CA number, with a unique complaint ID issued on submission.
- **Five fault categories:** billing faults, metering faults, power supply outage, voltage complaints, new-connection requests.
- **Status lifecycle:** `registered → assigned → in-progress → resolved`.
- **Role-based access** for three roles: consumer, subdivision officer, admin.
- **Officer caseload dashboard** showing open complaints assigned to the logged-in officer.
- **[SLA-aging flags and IGRC-to-CGRF escalation tiers — fill in if built, else delete this bullet]**

---

## Why this project

Complaint handling in Indian power distribution is a workflow problem before it is a technology problem. Complaints arrive in bulk, they are keyed to a consumer identity, they route to the wrong desk if categorised poorly, and they get lost between assignment and resolution. Utilities already run grievance systems — MSEDCL's Mahavitaran portal, the national CPGRAMS — and those are the domain reference here, not the competition.

This prototype isolates the workflow: how a complaint moves, who can see it at each stage, what happens when it ages past its SLA. The longer-term interest is the text layer on top — routing code-mixed Marathi–Hindi–English complaints to the right department automatically. That is a separate project; see the related work below.

---

## Stack

- **Backend:** [Python, Flask — confirm]
- **Database:** [SQLite — confirm]
- **Frontend:** [HTML, CSS, Bootstrap — confirm]
- **Auth:** [session-based / Flask-Login — confirm]

---

## Data model

Core tables:

- **consumer** — consumer number / CA number, name, subdivision.
- **complaint** — complaint ID, consumer reference, category, description, status, assigned officer, timestamps (`registered_at`, `assigned_at`, `resolved_at`).
- **officer** — officer ID, subdivision, role.
- **status_log** — every state transition for a complaint, with timestamp and actor.

[Adjust to match your actual schema. If you used an ORM — SQLAlchemy models — mention it.]

---

## Running it locally

```bash
git clone https://github.com/Akshad111/GrievanceHUB.git
cd GrievanceHUB
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
