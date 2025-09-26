import pickle
from fastapi import FastAPI, HTTPException
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from tictactoe import TicTacToe, AIPlayer

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000",
                   "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Q-table from Colab
with open("q_table.pkl", "rb") as f:
    Q_table = pickle.load(f)

ai_player = AIPlayer(Q_table)
games = {}

# ---------------- Utility ----------------
def serialize_board(board):
    """Convert numeric board to X/O/blank for frontend"""
    return ['X' if x == 1 else 'O' if x == -1 else ' ' for x in board]

def serialize_player(player):
    return "x" if player == 1 else "o"

# ---------------- Models ----------------
class GameState(BaseModel):
    board: List[str]
    current_player: str
    winner: Optional[int]
    game_over: bool

class MoveRequest(BaseModel):
    game_id: str
    position: Optional[int] = None

class NewGameRequest(BaseModel):
    game_id: str

# ---------------- Routes ----------------
@app.get("/")
async def root():
    return {"message": "TicTacToe API running!"}

@app.post("/new-game", response_model=GameState)
async def new_game(request: NewGameRequest):
    game = TicTacToe()
    games[request.game_id] = game

    # If AI starts (X), make first move
    if game.current_player == 1:
        ai_move = ai_player.get_move(game.board)
        if ai_move is not None:
            game.make_move(ai_move)

    winner = game.check_winner()
    return GameState(
        board=serialize_board(game.board),
        current_player=serialize_player(game.current_player),
        winner=winner,
        game_over=winner is not None
    )

@app.post("/make-move", response_model=GameState)
async def make_move(request: MoveRequest):
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[request.game_id]

    # Human move
    if request.position is not None:
        if not game.make_move(request.position):
            raise HTTPException(status_code=400, detail="Invalid move")

    winner = game.check_winner()
    if winner is not None:
        return GameState(
            board=serialize_board(game.board),
            current_player=serialize_player(game.current_player),
            winner=winner,
            game_over=True
        )

    # AI move
    if game.current_player == 1:
        ai_move = ai_player.get_move(game.board)
        if ai_move is not None:
            game.make_move(ai_move)

    winner = game.check_winner()
    return GameState(
        board=serialize_board(game.board),
        current_player=serialize_player(game.current_player),
        winner=winner,
        game_over=winner is not None
    )

@app.get("/game/{game_id}", response_model=GameState)
async def get_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    winner = game.check_winner()
    return GameState(
        board=serialize_board(game.board),
        current_player=serialize_player(game.current_player),
        winner=winner,
        game_over=winner is not None
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



