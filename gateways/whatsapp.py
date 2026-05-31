import os
import sys
from agent.agent import LatticeAgent

class WhatsAppGateway:
    """
    WhatsAppGateway handles routing of live instant messaging event streams
    from WhatsApp webhook providers (like Twilio) to the LatticeAgent.
    It provisions a robust, lightweight Flask server to intercept and process messages.
    """
    def __init__(self, agent: LatticeAgent):
        self.agent = agent

    def start(self):
        """Starts the Flask server to listen for incoming WhatsApp webhooks."""
        print("\n\x1b[36;1m=======================================================")
        print("         LATTICE WHATSAPP INTEGRATION GATEWAY")
        print("=======================================================\x1b[0m")
        
        # Double check Twilio configuration
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        if not account_sid or not auth_token:
            print("\x1b[33mWarning: TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not defined in environment.\x1b[0m")
            print("\x1b[33mLattice will run the WhatsApp gateway server in sandboxed mock mode.\x1b[0m\n")

        try:
            from flask import Flask, request, Response
        except ImportError:
            print("\x1b[31;1mError: Flask is required to run the WhatsApp Webhook Gateway.\x1b[0m")
            print("Please run: \x1b[32mpip install flask\x1b[0m or make sure it is installed in your venv.")
            sys.exit(1)

        app = Flask(__name__)

        @app.route("/", methods=["GET"])
        def index():
            return {
                "status": "online",
                "gateway": "whatsapp",
                "framework": "Lattice Agent Engine",
                "instructions": "Send a POST webhook payload to /webhook containing Twilio WhatsApp parameters (Body, From)."
            }

        @app.route("/webhook", methods=["POST"])
        def webhook():
            # Support both standard URL-encoded form data (Twilio standard) and raw JSON payloads
            if request.is_json:
                data = request.get_json()
                sender = data.get("sender", "whatsapp:+123456789")
                query = data.get("message", "").strip()
            else:
                sender = request.form.get("From", "whatsapp:+123456789")
                query = request.form.get("Body", "").strip()

            if not query:
                return Response(
                    "<Response><Message>Error: Empty query payload.</Message></Response>",
                    mimetype="text/xml"
                )

            # Process the query using our decoupled handle_incoming_message logic
            final_answer = self.handle_incoming_message(sender, query)

            # Respond using Twilio TwiML format (XML)
            twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{final_answer}</Message>
</Response>"""
            return Response(twiml_response, mimetype="text/xml")

        # Read host and port configurations from environment
        port = int(os.getenv("PORT", "5000"))
        host = os.getenv("HOST", "0.0.0.0")

        print(f"\x1b[32m✔ WhatsApp Webhook Server Booted successfully.\x1b[0m")
        print(f"  \x1b[90mListening at: http://{host}:{port}/webhook\x1b[0m")
        print(f"  \x1b[90mConfigure your Twilio Sandbox Webhook to point here using ngrok!\x1b[0m\n")

        # Run Flask server locally
        app.run(host=host, port=port, debug=False, use_reloader=False)

    def handle_incoming_message(self, sender_number: str, message_text: str) -> str:
        """
        Routes an incoming message from a WhatsApp webhook to the LatticeAgent,
        returning the final synthesized research result.
        """
        print(f"\n\x1b[36m[WhatsApp Webhook Received]\x1b[0m")
        print(f"  Sender: {sender_number}")
        print(f"  Message: \"{message_text}\"")
        print(f"  \x1b[90mStarting autonomous reasoning loop...\x1b[0m")

        # Drive the autonomous agent loop sequentially
        result = self.agent.run(message_text)

        print(f"\x1b[32m✔ Synthesis Complete.\x1b[0m Routing reply back to {sender_number}.")
        return result
