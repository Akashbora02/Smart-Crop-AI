from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    try:
        moisture = float(data.get('moisture', -1))
        leaf = float(data.get('leaf', -1))
        color = int(data.get('color', -1))
        pest = int(data.get('pest', -1))

        # 🚫 Validation
        if moisture < 0 or moisture > 100:
            return jsonify({"error": "Invalid moisture value (0–100)"})
        if leaf < 1 or leaf > 6:
            return jsonify({"error": "Leaf damage must be between 1–6"})
        if color < 1 or color > 5:
            return jsonify({"error": "Invalid color selection"})
        if pest not in [0,1]:
            return jsonify({"error": "Invalid pest value"})

        # 🧠 Disease logic
        if color >= 5 and leaf >= 4:
            disease = "Leaf Blight"
            advice = "Apply fungicide spray immediately."
        elif color == 4 and pest == 1:
            disease = "Bacterial Spot"
            advice = "Reduce irrigation and apply bactericide."
        elif color == 3 and leaf >= 3:
            disease = "Yellow Rust"
            advice = "Use resistant seeds."
        elif moisture > 80:
            disease = "Root Rot"
            advice = "Improve drainage."
        elif pest == 1:
            disease = "Pest Attack"
            advice = "Use pesticide."
        else:
            disease = "Healthy"
            advice = "Maintain crop care."

        # 📊 Score
        score = (moisture/20)+(leaf*2)+(color*3)+(pest*8)

        if score > 25:
            risk="⚠ High Risk"
        elif score > 12:
            risk="⚡ Moderate Risk"
        else:
            risk="✅ Low Risk"

        return jsonify({
            "risk":risk,
            "disease":disease,
            "advice":advice
        })

    except:
        return jsonify({"error": "Invalid input format"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)