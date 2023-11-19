

from flask import Flask, request, jsonify


app = Flask(__name__)
def sublists(lst):
    n = len(lst)
    sublists = []

    for start in range(n):
        for end in range(start + 1, n + 1):
            sublists.append(lst[start:end])

    return sublists

# Your existing JSON processing function
def process_json(data):
    all_list = []
    for inputs_set in data['inputs']:
        cutoff=int(inputs_set[0])
        lists=(inputs_set[2])
        substrings = lists.split()

        # Convert substrings to integers
        lists = list(map(int, substrings))
        print(type(lists))
        print(lists)
        sublist=sublists(lists)
        print(sublist)
        sums_per_list = [sum(int(x) for x in inner_list if str(x).isdigit()) for inner_list in sublist]
        unique=list(set(sums_per_list))
        print(unique)
        ctr=0
        for i in range(len(unique)):
            if unique[i]<cutoff:
                ctr+=1
        print(ctr)
        all_list.append(ctr)

    return all_list


# Expose a POST endpoint /time-intervals
@app.route('/mlmm-program', methods=['POST'])
def time_intervals_post():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            if json_data is None:
                raise ValueError("Invalid JSON data")


            result = process_json(json_data)
            return jsonify({"answer": result})
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500



# Expose a GET endpoint /time-intervals
@app.route('/mlmm-program', methods=['GET'])
def time_intervals_get():
    # json_data='''{
    # "inputs": [
    # [
    #     "16",
    #     "4",
    #     "10 5 2 6"
    # ]
    # ]

    # }'''
    # data=json.loads(json_data)
    # process_json(data)

    try:
        json_data = request.args.get('inputs')

        if not json_data:
            return jsonify({"error": "No inputs provided"}), 400
        result = process_json(json_data)
        return jsonify({"answer": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    # main()
    app.run(host='0.0.0.0', port=4098, debug=True)

