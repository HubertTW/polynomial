import json
import re
import numpy as np


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def interpolate(f: list, n: int, p) -> float:
    result = np.poly1d([0])
    for i in range(n):
        term = f[i].y
        temp = 1
        for j in range(n):
            if j != i:
                t = (f[i].x - f[j].x)
                print("t: ", t)
                # term = term * (xi - f[j].x) / (f[i].x - f[j].x)
                temp = temp * np.poly1d([1, -f[j].x]) * pow(t, -1, p)
                # print(temp)
        temp = temp * term
        result += temp
    print(result)
    l = []
    for i in result:
        l.append(i % p)
    return l


if __name__ == "__main__":

    #file_path = 'console-export-2024-5-21_15-32-24.txt'
    file_path = '20240704.txt'
    # file_path = 'console-export-2024-5-21_12-44-3.txt'
    with open(file_path, 'r') as file:
        file_content = file.read()

    lines = file_content.strip().split('\n')
    transitions = []

    for line in lines:
        if '->' in line:
            parts = line.split('->')
            start = parts[0].strip()
            rest = parts[1].strip().split('[')
            end = rest[0].strip()
            label = ""
            dir_back = False
            if len(rest) > 1:
                rest_parts = rest[1].split()
                for part in rest_parts:
                    #print(rest_parts)
                    if 'label' in part:
                        label_parts = rest[1].split('"')
                        if len(label_parts) > 1:
                            label = label_parts[1].strip()
                    #if 'dir' in part and 'back' in part:
                    if 'dir' in rest_parts:
                        dir_back = True

            labels = label.split(',')
            for lbl in labels:
                lbl = lbl.strip()
                if lbl and lbl not in ["a", "p", "l", "e"]:
                    lbl = "new_label"
                if lbl:
                    if dir_back:
                        transitions.append((end, start, lbl))  # Reverse from and to
                    else:
                        transitions.append((start, end, lbl))

    # Combine transitions with the same 'from' and 'to'
    combined_transitions = {}
    for t in transitions:
        key = (t[0], t[1])
        if key not in combined_transitions:
            combined_transitions[key] = set()
        combined_transitions[key].add(t[2])

    # Construct the JSON-like dictionary
    dfa_dict = {
        "states": list(set([t[0] for t in transitions] + [t[1] for t in transitions])),
        "transitions": [
            {
                "from": k[0],
                "to": k[1],
                "input": list(v)
            } for k, v in combined_transitions.items()
        ]
    }

    # Convert to JSON string for readability
    dfa_json = json.dumps(dfa_dict, indent=2)
    print(dfa_json)

    encoding = {"a": 1, "p": 2, "l": 3, "e": 4, "new_label": 5}

    # 初始化 m 和 n 的列表
    m = []
    n = []

    # 遍歷 transitions 列表
    for transition in dfa_dict["transitions"]:
        from_state = int(transition["from"])
        to_state = int(transition["to"])
        inputs = transition["input"]

        for inp in inputs:
            if inp in encoding:
                m_i = from_state * 5 + encoding[inp]
                n_i = to_state
                m.append(m_i)
                n.append(n_i)

    # 打印結果
    print("m:", m)
    print("m len", len(m))
    print("n:", n)
    print("n len", len(n))


    #points = [Data(1, 1), Data(2, 4), Data(3, 9)]
    points = [Data(1,1),Data(2,2)]
    #points = [Data(m[i], n[i]) for i in range(len(m))]

    # 打印結果
    for point in points:
        print(f"Data(x={point.x}, y={point.y})")



    #p = np.poly1d([4, 1, 3])
    #q = np.poly1d([2, 4])

    print(interpolate(points, 40, 61))


'''    node_pattern = re.compile(r'node \[shape = doublecircle\]; (.+) ;')
    edge_pattern = re.compile(r'(\d+) -> (\d+) \[ label = "(.*?)"  (dir = back)?\];')

    nodes_match = node_pattern.search(file_content)
    edges_match = edge_pattern.findall(file_content)

    data = {
        "nodes": nodes_match.group(1) if nodes_match else "",
        "edges": [{"from": m[0], "to": m[1], "label": m[2]} for m in edges_match]
    }
    #alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    single = ['f', 'o', 'd']


    print(len(data['edges']))
    json_data = json.dumps(data, indent=4)
    print(json_data)

    #for i in range(0, len(data['edges'])):

'''