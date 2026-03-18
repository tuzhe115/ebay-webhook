from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

VERIFICATION_TOKEN = "ewaste-project-verification-token-2026-secure"


def generate_response(challenge_code):
    return hashlib.sha256(
        (challenge_code + VERIFICATION_TOKEN).encode()
    ).hexdigest()


@app.route("/", methods=["GET"])
@app.route("/webhook", methods=["GET"])
def webhook():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return "OK"

    challenge_response = generate_response(challenge_code)

    return jsonify({
        "challengeResponse": challenge_response
    })


if __name__ == "__main__":
    app.run()