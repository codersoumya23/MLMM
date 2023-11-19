

from flask import Flask, request, jsonify


app = Flask(__name__)
def sublists(L,L2=None):
    if L2==None:
        L2 = L[:-1]

    if L==[]:
        if L2==[]:
            return []
        return sublists(L2,L2[:-1])
    return [L]+sublists(L[1:],L2)
    #sublists=[L[i:i+j] for i in range(0,len(L)) for j in range(1,len(L)-i+1)]
    # n = len(lst)
    # sublists = []

    # for start in range(n):
    #     for end in range(start + 1, n + 1):
    #         sublists.append(lst[start:end])

    # return sublists

# Your existing JSON processing function
def process_json(data):
    all_list = []
    for inputs_set in data['inputs']:
        cutoff=int(inputs_set[0])
        lists=(inputs_set[2])
        substrings = lists.split()

        # Convert substrings to integers
        lists = list(map(int, substrings))

        sublist=sublists(lists)

        sums_per_list = [sum(int(x) for x in inner_list if str(x).isdigit()) for inner_list in sublist]
        #unique=list(set(sums_per_list))

        ctr=0
        for i in range(len(sums_per_list)):
            if sums_per_list[i]<cutoff:
                ctr+=1

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

