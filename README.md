# Gmail Calendar Agent

A smart agent that helps you manage your Gmail and Calendar. It extracts important information from your emails, categorizes them, and can help you schedule events.

## Features

- **Email Extraction**: Fetches recent emails from your Gmail inbox.
- **Smart Filtering**: Categorizes emails (e.g., Work, Personal, Spam).
- **Calendar Integration**: (Planned/In Progress) Helps schedule events based on email content.
- **Chrome Extension**: A popup extension to view agent status and recent emails.

## Prerequisites

- **Python 3.8+**
- **Node.js** (for building the extension, if applicable, though currently it's vanilla JS/HTML)
- **Google Chrome** (to load the extension)
- **Google Cloud Console Project**: You need a project with Gmail API enabled and `credentials.json`.

## Setup

1.  **Clone the repository** (if you haven't already).

2.  **Set up the Python Environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` and add your OpenAI API Key:
      ```text
      OPENAI_API_KEY=your_actual_api_key_here
      ```
    - Place your `credentials.json` (from Google Cloud Console) in the root directory.

## Usage

### Backend Server

1.  Start the backend server:
    ```bash
    python src/server.py
    ```
    The server will start on `http://127.0.0.1:8000`.

### Chrome Extension

1.  Open Google Chrome and navigate to `chrome://extensions/`.
2.  Enable **Developer mode** (top right toggle).
3.  Click **Load unpacked**.
4.  Select the `extension` directory in this project.
5.  You should now see the Gmail Calendar Agent icon in your toolbar. Click it to interact with the agent.

## Project Structure

- `src/`: Python source code for the agent and server.
- `extension/`: Source code for the Chrome Extension (HTML, CSS, JS).
- `tests/`: Tests for the project.
- `credentials.json`: (Required) Google OAuth credentials.
- `token.json`: (Generated) Stores user access tokens.

## License

[License Name]
