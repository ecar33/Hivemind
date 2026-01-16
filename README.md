# Hivemind

A real-time web chat application built with **Flask** and **Flask-SocketIO**.  
Hivemind supports user accounts, chatrooms, and live messaging in the browser using WebSockets.

## Features
- Real-time chat with **Socket.IO**
- User authentication (sign up / log in / log out)
- Chatrooms + participant handling
- Profile settings (including avatar upload)
- SQLite database for local development
- Basic rate limiting and structured error handling

## Tech Stack
- **Python / Flask**
- **Flask-SocketIO** (real-time messaging)
- **Flask-Login** (auth)
- **Flask-SQLAlchemy** (database)
- **WTForms** (forms/validation)
- **TailwindCSS + DaisyUI** (styling, optional rebuild)

## Getting Started

### 1) Clone the repo
```bash
git clone https://github.com/ecar33/Hivemind.git
cd Hivemind
```

### 2) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3) Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4) Initialize the database
This project uses SQLite by default in development.
```bash
flask --app run.py initdb
```

(Optional) Seed sample data:
```bash
flask --app run.py forge
```

### 5) Run the app
```bash
python run.py
```

Then open:
```text
http://127.0.0.1:5000
```

## Environment Variables (Optional)
You can create a `.env` file in the project root if you want to set a custom secret key:

```text
SECRET_KEY=your_secret_key_here
```

If not provided, the app uses a development default (`dev`).

## Frontend Styling (Optional)
The compiled CSS file is already included (`static/css/output.css`), so **Node.js is not required** to run the app.

If you want to rebuild Tailwind styles:
```bash
npm install
npm run dev
```

## Project Notes
- Development config uses a local SQLite DB:
  - `data.db` is created in the project directory after initialization
- Avatar uploads are stored in:
  - `hivemind/static/avatars` (default max upload size: 1 MB)

## License
MIT License. See the [LICENSE](LICENSE) file for details.
