import json
import re
import numpy as np
from numpy.polynomial import Polynomial


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)


def evaluate_polynomial(coeffs, x, p):
    result = 0
    for coeff in coeffs:
        result = (result * x + coeff) % p
    return result


def interpolate(f: list, n, p):
    result = np.poly1d([0])
    for i in range(n):
        term = f[i].y
        poly = np.poly1d([1])
        for j in range(n):
            if j != i:
                bottom = (f[i].x - f[j].x)
                #print(f"bottom {bottom}")
                poly *= np.poly1d([1, -f[j].x])
                poly = mod_poly(poly, p)
                term = (term * (pow(bottom, -1, p))) % p
        result += term * poly
        result = mod_poly(result, p)
        #print(result)
        #print("-----------")
    l = []
    for i in result:
        l.append(i % p)
    return l


def mod_poly(poly, p):
    coeffs = poly.coeffs % p
    return np.poly1d(coeffs)


def interpolate_test(f: list, xi: int, n: int) -> float:
    # Initialize result
    result = 0.0
    for i in range(n):

        # Compute individual terms of above formula
        term = f[i].y
        for j in range(n):
            if j != i:
                term = term * (xi - f[j].x) / (f[i].x - f[j].x)

        # Add current term to result
        result += term

    return result


if __name__ == "__main__":

    #file_path = 'console-export-2024-5-21_15-32-24.txt'
    file_path = '20240711.txt'
    # file_path = 'console-export-2024-5-21_12-44-3.txt'
    #encoding = {"a": 1, "b": 2, "new_label": 3}
    encoding = {"a": 1, "p": 2, "l": 3, "e": 4, "new_label": 5}
    target = ["a", "p","l", "e" ]
    k = 5
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
                if lbl and lbl not in target:
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

    m = []
    n = []

    for transition in dfa_dict["transitions"]:
        from_state = int(transition["from"])
        to_state = int(transition["to"])
        inputs = transition["input"]

        for inp in inputs:
            if inp in encoding:
                m_i = from_state * k + encoding[inp]
                n_i = to_state
                m.append(m_i)
                n.append(n_i)

    print("m:", m)
    print("m len", len(m))
    print("n:", n)
    print("n len", len(n))

    points = [Data(m[i], n[i]) for i in range(0, len(m))]
    coef = interpolate(points, len(points), 101)
    polynomial = np.poly1d(coef)
    for point in points:
        print(f"Data(x={point.x}, y={point.y})")

    for point in points[:]:
        print(f"x={point.x}, y={evaluate_polynomial(coef, point.x, 101) % 101}")

    print(polynomial)
    print("final result :", coef[::-1])
