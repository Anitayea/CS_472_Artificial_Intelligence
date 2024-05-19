class BackEnd:
    def __init__(self):
        self.bindings = {}
        self.jump_atoms = {}

    def process(self, input_file_path, output_file_path):
        self.read_input(input_file_path)
        if not self.bindings:
            self.write_output(output_file_path, ["NO SOLUTION"])
        else:
            jumps = self.find_jumps()
            self.write_output(output_file_path, jumps)

    def read_input(self, input_file_path):
        with open(input_file_path, "r") as file:
            lines = file.readlines()
            self.parse_bindings(lines)
            self.parse_jump_atoms(lines)

    def parse_bindings(self, lines):
        #extract bindings from the input file
        for line in lines:
            line = line.strip()
            if line == "0":
                break

            x, val = map(str, line.split())
            self.bindings[int(x)] = val

    def parse_jump_atoms(self, lines):
        #extract Jump(A,B,C,I) atoms from input
        for line in lines[len(self.bindings) + 1:]:
            if line == "0" or "Peg" in line:
                continue

            x, val = map(str, line.strip().split("Jump"))
            self.jump_atoms[int(x)] = val

    def find_jumps(self):
        jumps = []
        max_jump_atom_index = max(self.jump_atoms.keys())
        for atom_index, val in self.bindings.items():
            if val == "T" and atom_index <= max_jump_atom_index:
                jumps.append(self.jump_atoms[atom_index])
        return jumps

    def write_output(self, output_file_path, jumps):
        sorted_jumps = sorted(jumps, key=lambda x: int(x.strip().split(", ")[-1].split(")")[0]))
        with open(output_file_path, "w") as file:
            for jump in sorted_jumps:
                file.write(f"Jump{jump}\n")


#main
if __name__ == "__main__":
    backend = BackEnd()
    input_file_path = "dp_output.txt"
    output_file_path = "be_output.txt"
    backend.process(input_file_path, output_file_path)
