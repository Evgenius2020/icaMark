import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from flask import Flask, request, jsonify

from classifier import Classifier

app = Flask(__name__)

classifier = Classifier()

@app.route('/label', methods=['POST'])
def test():
    file = request.files['plot']
    filename = file.filename
    file.save(filename)

    global classifier
    label = classifier.get_label(filename)
    print('Predicted {}'.format(filename, label))
    os.remove(filename)

    return jsonify({"label": label})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
