from flask import Flask, render_template, request, jsonify, session
import yaml

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於啟用 Flask 的 session

# 讀取遊戲名稱資料，並將所有鍵轉換為字串
with open('games.yaml', 'r', encoding='utf-8') as f:
    GAME_DATA = yaml.safe_load(f)
    GAME_DATA = {
        str(key): {
            "name": value["name"],
            "levels": {str(k): v for k, v in value.get("levels", {}).items()}
        }
        for key, value in GAME_DATA.items()
    }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game/<game_id>')
def game(game_id):
    game = GAME_DATA.get(game_id, {})
    game_name = game.get("name", "未知遊戲")
    levels = game.get("levels", {}).keys()  # 獲取所有關卡的 ID
    levels = sorted(map(int, levels))  # 將關卡 ID 轉為整數並排序

    # 獲取使用者的進度，並確保第一關預設為已解鎖
    progress_key = f'progress_{game_id}'
    if progress_key not in session:
        session[progress_key] = 1  # 初始化進度為第一關已解鎖

    progress = session.get(progress_key, 0)

    return render_template('levels.html', game_id=game_id, game_name=game_name, levels=levels, progress=progress)

@app.route('/game/<game_id>/level/<level_id>')
def level(game_id, level_id):
    game = GAME_DATA.get(game_id, {})
    game_name = game.get("name", "未知遊戲")
    level_data = game.get("levels", {}).get(level_id, {})
    description = level_data.get("description", "沒有劇情描述")
    hint = level_data.get("hint", "沒有提示")

    # 確保使用者只能訪問已解鎖的關卡
    progress = session.get(f'progress_{game_id}', 0)
    if int(level_id) > progress + 1:
        return "尚未解鎖此關卡", 403

    return render_template(
        'level.html',
        game_id=game_id,
        level_id=level_id,
        game_name=game_name,
        description=description,
        hint=hint
    )

@app.route('/game/<game_id>/level/<level_id>/hints')
def hints(game_id, level_id):
    game = GAME_DATA.get(game_id, {})
    game_name = game.get("name", "未知遊戲")
    level_data = game.get("levels", {}).get(level_id, {})
    hints = level_data.get("hints", [])

    return render_template(
        'hints.html',
        game_id=game_id,
        level_id=level_id,
        game_name=game_name,
        hints=hints
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

        # 更新使用者的進度
        progress_key = f'progress_{game_id}'
        current_progress = session.get(progress_key, 0)
        session[progress_key] = max(current_progress, next_level_id)

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

