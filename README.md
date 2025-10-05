# Tic-Tac-Toe  - Reinforcement Learning

This project implements a **Tic-Tac-Toe game** using **Reinforcement Learning (Q-Learning)** with a web interface.  
You can play against an AI trained with a Q-table. The game runs in your browser using React for the frontend and FastAPI for the backend.

---

## Project Structure

tic-tac-toe/
├─ backend/ # FastAPI backend with game logic and AI
├─ frontend-react/ # React frontend UI
├─ tictactoe.ipynb # Optional Colab notebook
├─ .gitignore # Ignored files (node_modules, pycache, etc.)
└─ README.md # This file
 
---

## Features

- AI player using a **trained Q-table**
- Web-based interface with React
- Playable against AI
- Displays current board state
- Announces winner or draw

---

## Backend & Frontend Setup

### Backend

1. Navigate to the backend folder:

```bash
cd backend
Install dependencies:

 
pip install -r requirements.txt
Run the FastAPI server:
 
uvicorn main:app --reload
Backend runs on http://127.0.0.1:8000

Frontend
Navigate to the frontend folder:

 
cd ../frontend-react
Install dependencies:

 
npm install
Start the React app:

 
npm start
Frontend runs on http://localhost:3000

How to Play
You play as O, AI plays as X.

Click on an empty cell to make your move.

The game shows the current turn and announces the winner or draw.

Q-Learning Details
The AI uses a Q-table trained via reinforcement learning.

Each board state is mapped to Q-values for each possible move.

AI selects the move with the highest Q-value.

Q-values are stored in q_table.pkl in the backend folder.
