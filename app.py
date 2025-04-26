from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    user_input = data.get('input', '')
    # 假設正確答案是 "daniel"
    if user_input.lower() == 'daniel':
        return jsonify({'result': '正確'})
    else:
        return jsonify({'result': '錯誤'})

