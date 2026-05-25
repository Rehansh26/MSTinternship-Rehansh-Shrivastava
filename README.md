# AI-Powered Smart CRM & Card Scanner

A complete, end-to-end CRM and networking platform that automates business card ingestion, maps professional relationships using a Knowledge Graph, tracks sales pipelines, and provides an AI-powered assistant using local Large Language Models (LLMs).

## 🚀 Key Features

* **Smart Business Card Scanner:** Automated OCR ingestion of physical business cards.
* **Knowledge Graph Engine:** Maps relationships between contacts, companies, events, domains, and sales opportunities to visualize your network.
* **Opportunity Pipeline:** Full-stack pipeline management to track deal stages (Lead, Pitching, Negotiation, Closed Won/Lost).
* **Domain-Based Tagging:** Tag contacts by industry/domain to discover connections across your network.
* **Local AI Assistant:** A privacy-first RAG (Retrieval-Augmented Generation) chat assistant powered by Llama 3.2, capable of answering queries based on your private CRM data without sending info to the cloud.
* **Background Processing:** Utilizes Celery and Redis to handle heavy AI/OCR tasks asynchronously without lagging the UI.

## 🛠 Tech Stack

* **Backend:** Django (Python)
* **Database:** PostgreSQL
* **Task Queue:** Redis + Celery
* **AI/LLM:** Ollama (Llama 3.2)
* **Frontend:** Bootstrap 5, Vanilla JavaScript
* **Vector Store:** ChromaDB

## 📦 Prerequisites

1.  **Python 3.12+**
2.  **PostgreSQL** (Database)
3.  **Redis** (Task Broker)
4.  **Ollama** (Local LLM Server)
    * Download [Ollama](https://ollama.com/)
    * Run `ollama pull llama3.2`

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Rehansh26/MSTinternship-Rehansh-Shrivastava.git](https://github.com/Rehansh26/MSTinternship-Rehansh-Shrivastava.git)
    cd CardScanner
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    Create a `.env` file in the root directory and add your secret keys and database configuration:
    ```text
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgresql://user:password@localhost:5432/crm_db
    ```

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start Services:**
    * **Start Redis:** (Ensure redis-server is running)
    * **Start Celery:**
        ```bash
        celery -A card_manager worker --loglevel=info -P solo
        ```
    * **Start Django:**
        ```bash
        python manage.py runserver
        ```

## 🧠 Using the AI Assistant

Ensure Ollama is running in the background. The CRM interacts with the local API at `http://localhost:11434`. You can test the connection by running:

bash
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "prompt":"test"}'


## 📂 Project Structure

* `scanner/`: Main app containing models, views, and graph services.
* `scanner/graph_services.py`: Logic for mapping entities and relationships.
* `scanner/rag_services.py`: Handles vector storage and AI context retrieval.
* `templates/scanner/`: HTML files for Dashboard, Edit, and Chat views.



*Developed by Rehansh Shrivastava*

```

```
