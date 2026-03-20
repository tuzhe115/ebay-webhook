from flask import Flask, request, Response
import hashlib
import json

app = Flask(__name__)

VERIFICATION_TOKEN = "ewaste-project-verification-token-2026-secure"
ENDPOINT = "https://saleably-nonbeneficial-allegra.ngrok-free.dev/webhook"

@app.route("/webhook", methods=["GET"])
def webhook():
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return Response("OK", status=200)

    challenge_response = hashlib.sha256(
        (challenge_code + VERIFICATION_TOKEN + ENDPOINT).encode("utf-8")
    ).hexdigest()

    return Response(
        json.dumps({"challengeResponse": challenge_response}),
        status=200,
        content_type="application/json"
    )

if __name__ == "__main__":
    app.run(port=5000)