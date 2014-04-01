import main

def test_functional():
    app = TestApp(main.bottle)

    assert mywebapp.index() == 'Hi!'