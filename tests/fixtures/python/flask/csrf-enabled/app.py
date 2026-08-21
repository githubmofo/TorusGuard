class CSRFProtect:
    def __init__(self, app=None):
        self.app = app

class FlaskApp:
    def __init__(self, name):
        self.config = {}

app = FlaskApp("sample_csrf_app")
csrf = CSRFProtect(app)
