from flask import Flask, request, Response, jsonify
import hashlib
import json

app = Flask(__name__)

VERIFICATION_TOKEN = "ewaste-project-verification-token-2026-secure"
ENDPOINT = "https://ebay-webhook-yfbd.onrender.com/webhook"

def build_challenge_response(challenge_code: str) -> str:
    return hashlib.sha256(
        (challenge_code + VERIFICATION_TOKEN + ENDPOINT).encode("utf-8")
    ).hexdigest()

@app.route("/", methods=["GET"])
def home():
    return "Server is running", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1) eBay challenge verification
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            return Response("OK", status=200)

        challenge_response = build_challenge_response(challenge_code)

        return Response(
            json.dumps({"challengeResponse": challenge_response}),
            status=200,
            content_type="application/json"
        )

    # 2) eBay test/real notification delivery
    if request.method == "POST":
        payload = request.get_json(silent=True)

        print("Received eBay notification:")
        print(json.dumps(payload, indent=2))

        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000)