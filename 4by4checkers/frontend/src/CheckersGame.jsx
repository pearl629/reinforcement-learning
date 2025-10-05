import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5000/api";

const CheckersGame = () => {
  const [board, setBoard] = useState([]);
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [availableMoves, setAvailableMoves] = useState([]);
  const [message, setMessage] = useState("");
  const [isThinking, setIsThinking] = useState(false);

  useEffect(() => {
    initGame();
  }, []);

  const initGame = async () => {
    const res = await fetch(`${API_URL}/new-game`, { method: "POST" });
    const data = await res.json();
    setBoard(data.board);
    setSelectedPiece(null);
    setAvailableMoves([]);
    setMessage("AI is thinking...");
    setIsThinking(true);

    // Let agent make the first move automatically
    setTimeout(() => agentMove(data.board), 500);
  };

  const agentMove = async (currentBoard) => {
    const res = await fetch(`${API_URL}/agent-move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board: currentBoard }),
    });
    const aiData = await res.json();
    setBoard(aiData.board);
    setSelectedPiece(null);
    setAvailableMoves([]);
    setIsThinking(false);

    if (aiData.gameOver) {
      setMessage("AI won!");
    } else {
      setMessage("Your turn! Click a piece to move.");
    }
  };

  const handlePieceClick = async (i, j) => {
    if (isThinking) return;

    const res = await fetch(`${API_URL}/available-moves`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board, player: 0 }),
    });
    const data = await res.json();
    const pieceMoves = data.moves.filter(
      (m) => m.position[0] === i && m.position[1] === j
    );
    setSelectedPiece({ row: i, col: j });
    setAvailableMoves(pieceMoves);
    setMessage(`Selected piece at (${i}, ${j}). Click a highlighted square to move.`);
  };

  const handleSquareClick = async (i, j) => {
    if (!selectedPiece || isThinking) return;

    const move = availableMoves.find(
      (m) =>
        m.position[0] === selectedPiece.row &&
        m.position[1] === selectedPiece.col &&
        getDestination(m).row === i &&
        getDestination(m).col === j
    );
    if (!move) return;

    setIsThinking(true);

    // Send player move to backend
    const res = await fetch(`${API_URL}/make-move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        board,
        player: 0,
        action: move,
      }),
    });
    const data = await res.json();
    setBoard(data.board);
    setSelectedPiece(null);
    setAvailableMoves([]);

    if (data.gameOver) {
      setMessage("You won!");
      setIsThinking(false);
      return;
    }

    setMessage("AI is thinking...");
    setTimeout(() => agentMove(data.board), 500);
  };

  const getPieceSymbol = (cell) => {
    if (cell === " ") return "";
    return cell > 0 ? "●" : "○";
  };

  const getDestination = (move) => {
    const [i, j] = move.position;
    const dir = move.direction;
    if (dir === 0) return { row: i - 1, col: j - 1 };
    if (dir === 1) return { row: i - 1, col: j + 1 };
    if (dir === 2) return { row: i + 1, col: j - 1 };
    if (dir === 3) return { row: i + 1, col: j + 1 };
    return { row: i, col: j };
  };

  const isHighlighted = (i, j) => {
    return availableMoves.some((m) => {
      const dest = getDestination(m);
      return dest.row === i && dest.col === j;
    });
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        flexDirection: "column",
        backgroundColor: "#222",
        color: "#fff",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>4×4 Checkers</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 60px)",
          gap: "5px",
        }}
      >
        {board.map((row, i) =>
          row.map((cell, j) => (
            <div
              key={`${i}-${j}`}
              onClick={() => {
                if (cell <= 0 && cell !== " ") handlePieceClick(i, j);
                else handleSquareClick(i, j);
              }}
              style={{
                width: "60px",
                height: "60px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: (i + j) % 2 === 0 ? "#eee" : "#555",
                color: cell > 0 ? "red" : "blue",
                fontSize: "32px",
                border: isHighlighted(i, j) ? "3px solid green" : "1px solid #333",
                cursor: "pointer",
              }}
            >
              {getPieceSymbol(cell)}
            </div>
          ))
        )}
      </div>
      <button
        onClick={initGame}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#6b46c1",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        New Game
      </button>
      <div style={{ marginTop: "10px" }}>{message}</div>
    </div>
  );
};

export default CheckersGame;
