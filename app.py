from flask import Flask, render_template, request, jsonify
import yaml

app = Flask(__name__)

# 讀取遊戲名稱資料，並將所有鍵轉換為字串
with open('games.yaml', 'r', encoding='utf-8') as f:
    GAME_DATA = yaml.safe_load(f)
    GAME_DATA = {str(key): value for key, value in GAME_DATA.items()}

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
    level_data = game.get("levels", {}).get(str(level_id), {})
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
    game_id = data.get('game_id')
    level_id = int(data.get('level_id'))  # 將 level_id 轉為整數

    # 假設正確答案是 "daniel"
    if user_input.lower() == 'daniel':
        next_level_id = level_id + 1
        # 檢查下一關是否存在
        if str(next_level_id) in GAME_DATA.get(game_id, {}).get("levels", {}):
            next_url = f"/game/{game_id}/level/{next_level_id}"
            return jsonify({'result': '正確', 'next_url': next_url})
        else:
            # 如果沒有下一關，跳轉到結局頁面
            end_url = f"/game/{game_id}/end"
            return jsonify({'result': '正確', 'next_url': end_url})
    else:
        return jsonify({'result': '錯誤'})

@app.route('/game/<game_id>/end')
def end(game_id):
    game_name = GAME_DATA.get(game_id, {}).get("name", "未知遊戲")
    return render_template('end.html', game_name=game_name)

