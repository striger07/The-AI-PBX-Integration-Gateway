<div align="center">

# 🎯 AI PBX Gateway
### Async Call Ingestion & AI Processing Service



</div>

---

## 📋 Overview

This project implements a **backend microservice** that simulates a PBX (Private Branch Exchange) system used in call centers. It ingests high-frequency call audio metadata, ensures non-blocking processing, maintains call state reliably, and simulates integration with unreliable external AI services.

The system is designed with **asynchronous processing**, **fault tolerance**, and **concurrency safety** in mind, closely resembling real-world backend systems used in telecom and AI-powered voice applications.

<br>


## 🎯 Methodology

<table>
<tr>
<td>

The core approach of this project is based on **separating fast ingestion from slow processing**.

- **Non-blocking Ingestion**: Incoming call audio metadata is ingested through a fast FastAPI endpoint
- **Immediate Persistence**: Each audio packet is stored immediately in the database without waiting for downstream processing
- **State Machine Management**: Call lifecycle is managed using a robust state machine, ensuring the system can recover from failures
- **Async AI Processing**: Transcription and sentiment analysis are handled asynchronously in the background with retry logic to tolerate failures

</td>
</tr>
</table>

### ✨ Key Benefits

<div align="center">

| ✅ High throughput | ✅ Minimal API latency | ✅ Resilience |
|:------------------:|:---------------------:|:-------------:|
| For incoming requests | Non-blocking operations | Against unreliable services |

</div>

<br>


## 🏗️ Technical Details

### Architecture Overview

<div align="center">

| Component | Technology | Purpose |
|:---------:|:----------:|:--------|
| **API Layer** | FastAPI (Async) | Handles high-concurrency ingestion requests |
| **Database** | PostgreSQL | Source of truth for call state and packet data |
| **ORM** | Async SQLAlchemy | Non-blocking database interactions |
| **Processing** | Background Tasks | AI processing without blocking API responses |
| **Resilience** | Retry + Exponential Backoff | Handles flaky external AI service behavior |
| **Real-time** | WebSockets (optional) | Real-time supervisor updates |

</div>

<br>


### 🔄 Call State Machine

<table>
<tr>
<td>

Each call transitions through the following states:

```
┌─────────────┐
│ IN_PROGRESS │  ──────► Call is active, packets being ingested
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  COMPLETED  │  ──────► Call ingestion finished
└──────┬──────┘
       │
       ▼
┌───────────────┐
│ PROCESSING_AI │ ──────► AI transcription/sentiment processing
└──────┬────────┘
       │
       ├────► ┌──────────┐
       │      │ ARCHIVED │ ──────► Processing completed successfully
       │      └──────────┘
       │
       └────► ┌─────────┐
              │ FAILED  │  ──────► AI processing failed after retries
              └─────────┘
```

> **Note:** This state machine ensures **idempotency and recoverability**.

</td>
</tr>
</table>

<br>


### 📦 Packet Ordering & Concurrency Handling

<table>
<tr>
<td width="33%" align="center">

**Sequence Numbering**

Each packet includes a `sequence` number for ordering

</td>
<td width="33%" align="center">

**Non-blocking Validation**

System validates ordering but does not block ingestion

</td>
<td width="33%" align="center">

**Concurrency Safety**

Database-level constraints and row-level locking

</td>
</tr>
</table>

> 🔒 Using `SELECT … FOR UPDATE` to handle race conditions when multiple packets arrive simultaneously

<br>


### 🤖 Simulated Flaky AI Service

<div align="center">

Simulates real-world AI API instability:

| Feature | Description |
|:-------:|:------------|
| 🎲 **Random failures** | ~25% failure rate |
| ⏱️ **Variable latency** | 1–3 seconds per request |
| 🔄 **Auto-retry** | Exponential backoff ensures eventual consistency |

</div>

<br>


## 🚀 Setup Instructions

<details open>
<summary><b>Prerequisites</b></summary>

<br>

Before you begin, ensure you have the following installed:

- Python **3.10+**
- PostgreSQL **14+**
- Git

</details>

<br>

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/striger07/The-AI-PBX-Integration-Gateway
cd ai-pbx-gateway
```

<br>

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

<br>

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

<br>

### 4️⃣ PostgreSQL Setup

**Start PostgreSQL service:**

```bash
sudo systemctl start postgresql
```

**Create the database:**

```bash
sudo -i -u postgres
psql
CREATE DATABASE ai_calls;
\q
exit
```

<br>

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

<div align="center">

The server will start at: **🌐 http://127.0.0.1:8000**

</div>

<br>


## 📡 API Testing

### Swagger UI Documentation

<div align="center">

Open your browser and navigate to: **http://127.0.0.1:8000/docs**

</div>

<br>

### Example Request

<table>
<tr>
<td width="50%">

**Request**

Endpoint: `POST /ingest/{call_id}`

```json
{
  "sequence": 1,
  "data": "audio_chunk_1",
  "timestamp": 123.45
}
```

</td>
<td width="50%">

**Response**

Status: `200 OK`

```json
{
  "status": "accepted"
}
```

</td>
</tr>
</table>

<br>


## 🧪 Running Tests

```bash
pytest
```

<details>
<summary><b>Test Coverage</b></summary>

<br>

- ✅ Concurrent packet ingestion
- ✅ Race condition handling
- ✅ State machine transitions
- ✅ AI retry logic

</details>

<br>


## 🌟 Key Highlights

<div align="center">

| Feature | Description |
|:-------:|:------------|
| ⚡ **Fully Asynchronous** | Non-blocking request handling for maximum throughput |
| 🗄️ **Database-backed State** | Reliable state machine with PostgreSQL persistence |
| 🔒 **Concurrency-safe** | Race condition prevention with row-level locking |
| 🛡️ **Fault-tolerant** | Exponential backoff retry for AI service failures |
| 🏢 **Production-ready** | Clean architecture following industry best practices |

</div>

<br>


## 📊 Project Structure

<details>
<summary><b>Click to expand project tree</b></summary>

<br>

```
ai-pbx-gateway/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database configuration
│   ├── services/
│   │   ├── ai_service.py    # Simulated AI processing
│   │   └── call_service.py  # Call state management
│   └── routers/
│       └── ingestion.py     # API endpoints
├── tests/
│   └── test_ingestion.py    # Test suite
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

</details>

<br>


## 🎓 Learning Outcomes

<table>
<tr>
<td>

This project demonstrates essential backend engineering principles:

| Principle | Implementation |
|:----------|:---------------|
| **Scalability** | Handling high-frequency requests without bottlenecks |
| **Resilience** | Graceful degradation and recovery from failures |
| **Concurrency Control** | Safe multi-threaded operations |
| **Fault Tolerance** | Retry mechanisms and error handling |
| **State Management** | Reliable lifecycle tracking |

</td>
</tr>
</table>

> 💡 This reflects real-world systems used in **telecom** and **AI-driven voice platforms** rather than a simple CRUD application.

<br>


## 👤 Author

<div align="center">

### Lakshay Sharma

[GitHub](https://github.com/striger07)


</div>

<br>








