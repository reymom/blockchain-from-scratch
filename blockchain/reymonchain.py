from app import app
from app.models import Blockchain


@app.shell_context_processor
def make_shell_context():
    return {'blockchain': Blockchain}
