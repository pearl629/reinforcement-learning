from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from copy import deepcopy
from checkers import available, apply_move, check_game_status, choose_action, reverse

app = Flask(__name__)
CORS(app)

# Load the Q-table
try:
    with open('q_table.pkl', 'rb') as f:
        Q_table = pickle.load(f)
    print("Q-table loaded successfully!")
except FileNotFoundError:
    print("Warning: q_table.pkl not found. Creating empty Q-table.")
    Q_table = {}

# Store current game state
current_board = []

@app.route('/')
def index():
    return "Checkers API is running! Use /api endpoints."

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'q_table_loaded': len(Q_table) > 0
    })

@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Initialize a new game"""
    global current_board
    board = [[" "] * 4 for _ in range(4)]
    board[0][1] = 1
    board[0][3] = 1
    board[3][0] = 0
    board[3][2] = 0
    current_board = board
    return jsonify({
        'board': board,
        'currentPlayer': 0,
        'gameOver': False,
        'winner': None
    })

@app.route('/api/available-moves', methods=['POST'])
def get_available_moves():
    """Get available moves for current player"""
    data = request.json
    board = data['board']
    player = data['player']

    avail_moves = available(player, board)

    # Convert to serializable format
    moves_list = []
    for pos, dirs in avail_moves.items():
        for idx, v in enumerate(dirs):
            if v == 1:
                moves_list.append({
                    'position': list(pos),
                    'direction': int(idx)
                })

    return jsonify({'moves': moves_list})

@app.route('/api/make-move', methods=['POST'])
def make_move():
    """Apply a human move"""
    global current_board
    data = request.json
    board = data['board']
    action = data['action']
    player = data['player']

    # Convert action format
    pos = tuple(action['position'])
    direction = action['direction']
    formatted_action = (pos, direction)

    # Apply the move
    new_board, reward, count = apply_move(deepcopy(board), formatted_action, player, 0)
    current_board = new_board

    # Check if game is over
    next_player = 1 if player == 0 else 0
    game_status = check_game_status(0, next_player, new_board)

    return jsonify({
        'board': new_board,
        'gameOver': game_status == -10,
        'winner': player if game_status == -10 else None,
        'reward': reward
    })

@app.route('/api/agent-move', methods=['POST'])
def agent_move():
    """Get the agent's move using Q-table"""
    global current_board
    data = request.json
    board = data['board']

    # Agent plays as player 1
    avail_moves = available(1, board)

    if not avail_moves:
        return jsonify({
            'board': board,
            'gameOver': True,
            'winner': 0,
            'action': None
        })

    # Get agent's action from Q-table
    action = choose_action(board, avail_moves, Q_table, epsilon=0.0)

    if action is None:
        return jsonify({
            'board': board,
            'gameOver': True,
            'winner': 0,
            'action': None
        })

    # Apply the move
    new_board, reward, count = apply_move(deepcopy(board), action, 1, 0)
    current_board = new_board

    # Check if game is over
    game_status = check_game_status(0, 0, new_board)

    return jsonify({
        'board': new_board,
        'gameOver': game_status == -10,
        'winner': 1 if game_status == -10 else None,
        'action': {
            'position': list(action[0]),
            'direction': int(action[1])
        }
    })

if __name__ == '__main__':
    # Run Flask server on port 5000
    app.run(debug=True, port=5000)
