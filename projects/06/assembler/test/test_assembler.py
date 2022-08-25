from assembler import Assembler

class TestAssembler:
    def test_instruction(self):
        # Check test/fixtures/instruction.hack manually
        Assembler.assemble('test/fixtures/instruction.asm')
