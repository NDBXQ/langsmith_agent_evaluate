from flask import Flask, request, jsonify
from dataset import DataSets


dataset = DataSets()
app = Flask(__name__)

@app.route('/add_datasets', methods=['POST'])
def add_datasets():
    print("Received request to add datasets")
    data_str = request.data.decode('utf-8')
    data = data_str.split("//")
    query  = data[0]
    information = data[1]
    dataset.add_dataset([query], [information], dataset_name="况总")
    print("add an example dataset")

    return jsonify({'message': 'Datasets added successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7870, debug=True)

