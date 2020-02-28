from app import app
from app.models import Transaction


@app.shell_context_processor
def make_shell_context():
    return {'txn': Transaction}
