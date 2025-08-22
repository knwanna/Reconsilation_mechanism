from flask import Flask
from adapters.entrypoints.flask_app import create_app

app = create_app()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    app.run(host='0.0.0.0', port=port, debug=True)
