from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/label', methods=['POST'])
def test():
    file = request.files['plot']
    file.save("plot.jpg")

    # get label
    label = 1

    return jsonify({"label": label})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
