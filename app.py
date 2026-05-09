# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/decode', methods=['POST'])
def decode_base64():
    """
    API endpoint to decode a Base64 string.
    Expects JSON: {"base64": "string_to_decode"}
    Returns JSON: {"decoded": "...", "error": "..."}
    """
    import base64
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, JSON expected"}), 400
    
    base64_string = data.get('base64', '')
    if not base64_string or not base64_string.strip():
        return jsonify({"error": "Empty input! Provide a valid Base64 string."}), 400
    
    try:
        # Attempt to decode the Base64 string
        # First, decode from base64 to bytes
        decoded_bytes = base64.b64decode(base64_string.strip())
        # Then, convert bytes to UTF-8 string
        decoded_text = decoded_bytes.decode('utf-8')
        
        return jsonify({
            "decoded": decoded_text,
            "length": len(decoded_text)
        })
    except base64.binascii.Error as e:
        # Handle specific base64 decoding errors
        return jsonify({"error": f"Invalid Base64 format: {str(e)}"}), 400
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, return the raw bytes as a fallback
        try:
            # Return as Latin-1 which never fails, but user should know
            decoded_bytes = base64.b64decode(base64_string.strip())
            decoded_text = decoded_bytes.decode('latin-1')
            return jsonify({
                "decoded": decoded_text,
                "warning": "Decoded as Latin-1 (non-UTF-8 content)"
            })
        except Exception as fallback_error:
            return jsonify({"error": f"Failed to decode: {str(fallback_error)}"}), 400
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"error": f"Decoding failed: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
