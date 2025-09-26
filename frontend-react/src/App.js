import React, { useState, useEffect } from "react";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const App = () => {
  const [gameId, setGameId] = useState(null);
  const [board, setBoard] = useState(Array(9).fill(" "));
  const [currentPlayer, setCurrentPlayer] = useState("x");
  const [winner, setWinner] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  const [winnerLine, setWinnerLine] = useState([]); // for highlighting winning cells

  const startNewGame = async () => {
    try {
      const newId = uuidv4();
      setGameId(newId);

      const response = await axios.post(`${API_URL}/new-game`, { game_id: newId });
      setBoard(response.data.board);
      setWinner(response.data.winner);
      setGameOver(response.data.game_over);
      setCurrentPlayer(response.data.current_player);
      setWinnerLine([]);
    } catch (error) {
      console.error("Error starting new game:", error);
      alert("Cannot connect to backend. Make sure FastAPI is running.");
    }
  };

  const handleMove = async (pos) => {
    if (gameOver || board[pos] !== " " || currentPlayer !== "o") return;

    try {
      const response = await axios.post(`${API_URL}/make-move`, {
        game_id: gameId,
        position: pos,
      });

      setBoard(response.data.board);
      setWinner(response.data.winner);
      setGameOver(response.data.game_over);
      setCurrentPlayer(response.data.current_player);

      // Highlight winning line if game is over
      if (response.data.game_over && response.data.winner !== 0) {
        highlightWinningLine(response.data.board, response.data.winner);
      }
    } catch (error) {
      console.error("Error making move:", error);
    }
  };

  // Dummy function to highlight winning line (optional)
  const highlightWinningLine = (board, winner) => {
    // You can implement logic to detect winning combination here
    // Example: [0,1,2] if top row wins
    setWinnerLine([]); // currently empty; optional enhancement
  };

  const renderCell = (i) => (
    <button
      key={i}
      onClick={() => handleMove(i)}
      className={`cell ${winnerLine.includes(i) ? "winner" : ""}`}
      disabled={board[i] !== " " || gameOver || currentPlayer !== "o"}
    >
      {board[i]}
    </button>
  );

  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div className="app">
      <h1>Tic Tac Toe</h1>
      <div className="board">{board.map((_, i) => renderCell(i))}</div>
      {gameOver ? (
        <h2>
          {winner === 1
            ? "AI (X) wins!"
            : winner === -1
            ? "You (O) win!"
            : "Draw!"}
        </h2>
      ) : (
        <div className="current-turn">Current Turn: {currentPlayer.toUpperCase()}</div>
      )}
      <button className="new-game" onClick={startNewGame}>
        New Game
      </button>
    </div>
  );
};

export default App;
