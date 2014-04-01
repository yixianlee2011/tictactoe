from webtest import TestApp
import main

def test_functional():
    app = TestApp(main.app)

    assert app.get('/api/get_bots').status == '200 OK'