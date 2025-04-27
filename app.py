from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 讀取遊戲名稱資料
with open('games.json', 'r', encoding='utf-8') as f:
    GAME_DATA = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game/<game_id>')
def game(game_id):
    game_name = GAME_DATA.get(game_id, {}).get("name", "未知遊戲")
    return render_template('levels.html', game_id=game_id, game_name=game_name)

@app.route('/game/<game_id>/level/<level_id>')
def level(game_id, level_id):
    game = GAME_DATA.get(game_id, {})
    game_name = game.get("name", "未知遊戲")
    level_data = game.get("levels", {}).get(level_id, {})
    description = level_data.get("description", "沒有劇情描述")
    hint = level_data.get("hint", "沒有提示")
    return render_template(
        'index.html',
        game_id=game_id,
        level_id=level_id,
        game_name=game_name,
        description=description,
        hint=hint
    )

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    user_input = data.get('input', '')
    # 假設正確答案是 "daniel"
    if user_input.lower() == 'daniel':
        return jsonify({'result': '正確'})
    else:
        return jsonify({'result': '錯誤'})

