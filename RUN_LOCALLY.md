# How to Run Locally

Follow these exact steps to run the AI Communication Scoring Tool on your local machine.

## Prerequisites

Ensure you have the following installed:
1. **Node.js** (v18 or higher)
2. **Python** (v3.11 or higher)
3. **pnpm** (or npm)
4. **uv** (Python package manager) - *Optional but recommended*

## Step 1: Backend Setup

1. Open a terminal.
2. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   # Using uv (Recommended)
   uv sync
   
   # OR using pip
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   # Using uv
   uv run uvicorn main:app --reload --port 8000
   
   # OR using python directly
   python -m uvicorn main:app --reload --port 8000
   ```
5. The backend is now running at `http://localhost:8000`.
   - Health check: `http://localhost:8000/health`
   - API Docs: `http://localhost:8000/docs`

## Step 2: Frontend Setup

1. Open a **new** terminal window (keep the backend running).
2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
3. Create a `.env` file:
   - Copy `.env.example` to `.env`
   - Or create a new file named `.env` with this content:
     ```
     VITE_API_URL=http://localhost:8000
     ```
4. Install dependencies:
   ```bash
   pnpm install
   ```
5. Start the frontend development server:
   ```bash
   pnpm dev
   ```
6. The frontend is now running at `http://localhost:5173`.

## Step 3: Usage

1. Open your browser and go to `http://localhost:5173`.
2. You will see the "AI Communication Coach" interface.
3. Enter a transcript in the text area.
   - *Sample*: "Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. I am 13 years old. I live with my family."
4. Click **Analyze Transcript**.
5. View the detailed scores and feedback.

## Troubleshooting

- **Backend not starting?** Check if port 8000 is free.
- **Frontend API errors?** Ensure the backend is running and `VITE_API_URL` is set correctly in `frontend/.env`.
- **CORS errors?** The backend is configured to allow all origins (`*`) by default, so this shouldn't happen locally.
