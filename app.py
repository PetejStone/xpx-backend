from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import pandas as pd

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        file.save(tmp.name)
        html = extract_from_xlsx(tmp.name, file.filename)
        os.unlink(tmp.name)

    return jsonify({'html': html})

def extract_from_xlsx(filepath, filename):
    df = pd.read_excel(filepath)
    df.fillna("", inplace=True)

    def cell_html(content, is_header=False):
        if is_header:
            return f'''
            <td valign="bottom" style="border-top:none;border-left:none;border-bottom:solid black 1.0pt;background:var(--inner-bg-alt);padding:0in 5.75pt 0in 5.75pt;height:14.5pt;text-align:center;">
                <p class="row-text" style="color:#fff;">{content}</p>
            </td>
            '''
        else:
            return f'''
            <td valign="bottom" style="border:solid black 1.0pt;padding:0in 5.75pt;height:14.5pt;text-align:center;">
                <p class="row-text"><span style="color:#787873;">{content}</span></p>
            </td>
            '''

    rows_html = ""
    for i, row in df.iterrows():
        rows_html += "<tr style='height:14.5pt;'>"
        for cell in row:
            rows_html += cell_html(cell)
        rows_html += "</tr>"

    header_html = ""
    if len(df) > 0:
        header_html = "<tr style='height:14.5pt;'>"
        for col in df.columns:
            header_html += cell_html(col, is_header=True)
        header_html += "</tr>"

    table_html = f'''
    <div class="TableContainer">
        <h3 style="color:#fff;background-color:var(--buttons);width:100%;margin-bottom:0px;text-align:center;padding:1rem;font-weight:100;">{filename}</h3>
        <table id="TableContainer" class="table-container" border="0" cellspacing="0" cellpadding="0" style="font-size:var(--content-font-size);text-align:left;color:var(--text-dark);font-family:var(--main-font);border-collapse:separate;width:100%;">
            {header_html}
            {rows_html}
        </table>
    </div>
    '''
    return table_html

if __name__ == '__main__':
    app.run()
