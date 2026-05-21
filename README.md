# 📇 AI-Powered Business Card Scanner & CRM

A full-stack Customer Relationship Management (CRM) platform built with Django and powered by local AI vision models. This application allows users to snap photos of business cards, automatically extracts the contact data using Llama 3.2 Vision, and intelligently stitches individuals into a self-assembling relational corporate network.

## ✨ Core Features

* **📸 AI Vision OCR:** Upload business card images and let a local, privacy-first AI model (`llama3.2-vision` via Ollama) extract names, emails, phone numbers, and companies with high accuracy.
* **🕸️ The Relational Graph:** The database automatically detects overlapping companies and builds dedicated corporate network pages, showing everyone you know at a specific organization.
* **🧠 Chat with your Database:** An integrated AI assistant that reads your verified database and answers natural-language questions about your contacts (e.g., "Who do I know at Globex?").
* **🛡️ Verification Queue & Duplicate Detection:** Scans are safely held in a queue for human review. The system automatically flags duplicate emails and phone numbers before they pollute your database.
* **⚡ Live Search & Export:** Instantly filter your approved contacts with lightning-fast JavaScript search, or export your entire Rolodex to CSV with a single click.
* **🔐 Secure Authentication:** A fully custom registration and login system ensuring that every user gets their own private, secure dashboard.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, JavaScript, Bootstrap 5 (CSS)
* **AI & Machine Learning:** Ollama (Local AI Server), Llama 3.2 Vision Model
* **Database:** SQLite (Default Django DB)

## 🚀 Getting Started

### Prerequisites
1. **Python 3.x** installed on your machine.
2. **Ollama** installed and running in the background.
3. The Llama 3.2 Vision model pulled locally. Open your terminal and run:
   ```bash
   ollama run llama3.2-vision

```

### Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
cd YOUR_REPOSITORY

```


2. **Install dependencies:**
```bash
pip install django requests

```


3. **Apply database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


4. **Start the development server:**
```bash
python manage.py runserver

```


5. **Open the app:**
Navigate to `http://127.0.0.1:8000/` in your web browser.

## 📖 How to Use

1. **Sign Up:** Create a new secure account on the landing page.
2. **Scan a Card:** Click "Scan New Card" and upload a photo of a business card. Add optional manual notes.
3. **Verify:** Review the AI's extraction in the Verification Queue. Fix any typos and click "Approve Record."
4. **Explore the Network:** Click on any bolded Company Name (e.g., `🏢 Microsoft (View Network)`) to see all known contacts from that organization.
5. **Ask AI:** Click "Ask AI" and type a question like, "What is Olivia's phone number?" to query your verified contacts.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
