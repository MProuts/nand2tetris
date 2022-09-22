from main import Main

class TestMain:
    def test_instruction(self):
        # Check test/fixtures/program.vm manually
        Main.execute('test/fixtures/program.vm')
