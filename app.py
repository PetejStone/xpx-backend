from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import tempfile
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

@app.route('/')
def home():
    return jsonify({'message': 'Backend is running'})

@app.route('/upload', methods=['POST'])
@cross_origin(origin='*')
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xps') as tmp:
        file.save(tmp.name)
        html = extract_from_xps(tmp.name)
        os.unlink(tmp.name)

    return jsonify({'html': html})

def extract_from_xps(filepath):
    # 🔧 Replace with real parsing later
    return '''
    <div class="TableContainer">
      <h3 style="color:#fff;background-color:var(--buttons);width:100%;margin-bottom:0px;text-align:center;padding:1rem;font-weight:100;">Book1</h3>
      <table><tr><td>Example</td><td>$100</td></tr></table>
    </div>
    '''

if __name__ == '__main__':
    app.run()
