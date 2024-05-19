class FrontEnd:
    def __init__(self):
        self.peg_atoms = {}
        self.jump_atoms = {}
        self.steps = 0
        self.init_empty_hole = 0
        self.clauses = []

    def preprocess(self, input_file):
        with open(input_file, "r") as file:
            lines = file.readlines()

        hole_num, self.init_empty_hole = map(int, lines[0].strip().split())
        self.steps = hole_num - 1
        atom_count = 0

        for line in lines[1:]:
            A, B, C = map(int, line.split())
            for step in range(1, self.steps):
                atom_count += 1
                self.jump_atoms[(A, B, C, step)] = atom_count
                atom_count += 1
                self.jump_atoms[(C, B, A, step)] = atom_count

        for j in range(1, hole_num + 1):
            for step in range(1, hole_num):
                atom_count += 1
                self.peg_atoms[(j, step)] = atom_count

    #encode preconditions for each jump atom into clauses
    def encode_preconditions(self):
        for jump_atom, jump_idx in self.jump_atoms.items():
            A, B, C, step = jump_atom
            self.clauses.append("-{} {}".format(jump_idx, self.peg_atoms[(A, step)]))
            self.clauses.append("-{} {}".format(jump_idx, self.peg_atoms[(B, step)]))
            self.clauses.append("-{} -{}".format(jump_idx, self.peg_atoms[(C, step)]))

    #causal axioms into clauses
    def encode_causal_axioms(self):
        for jump_atom, jump_idx in self.jump_atoms.items():
            A, B, C, step = jump_atom
            if step >= self.steps:
                continue
            self.clauses.append("-{} -{}".format(jump_idx, self.peg_atoms[(A, step + 1)]))
            self.clauses.append("-{} -{}".format(jump_idx, self.peg_atoms[(B, step + 1)]))
            self.clauses.append("-{} {}".format(jump_idx, self.peg_atoms[(C, step + 1)]))

    #frame axioms to cluases
    def encode_frame_axioms(self):
        for peg_atom, peg_idx in self.peg_atoms.items():
            hole, step = peg_atom
            if step >= self.steps:
                continue

            append_flag = False
            clause = "-{} {}".format(peg_idx, self.peg_atoms[(hole, step + 1)])
            for jump_atom, jump_idx in self.jump_atoms.items():
                A, B, C, jump_step = jump_atom
                if B == hole and jump_step == step or A == hole and jump_step == step:
                    append_flag = True
                    clause += " " + str(jump_idx)
            if append_flag:
                self.clauses.append(clause)

            append_flag = False
            clause = "{} -{}".format(peg_idx, self.peg_atoms[(hole, step + 1)])
            for jump_atom, jump_idx in self.jump_atoms.items():
                if jump_atom[2] == hole and jump_atom[3] == step:  # C == hole and jump_step == step
                    append_flag = True
                    clause += " " + str(jump_idx)
            if append_flag:
                self.clauses.append(clause)

    #ensures one action at a time
    def encode_one_action(self):
        filter_list = []
        for jump_atom_i, jump_idx_i in list(self.jump_atoms.items()):
            for jump_atom_j, jump_idx_j in self.jump_atoms.items():
                if jump_idx_i >= jump_idx_j or jump_atom_i[-1] != jump_atom_j[-1] or (jump_idx_i, jump_idx_j) in filter_list:
                    continue
                filter_list.extend([(jump_idx_i, jump_idx_j), (jump_idx_j, jump_idx_i)])
                self.clauses.append("-{} -{}".format(jump_idx_i, jump_idx_j))

    def encode_optional_actions(self):
        for step in range(1, self.steps):
            clause = " ".join(str(self.jump_atoms[jump_atom]) for jump_atom in self.jump_atoms if jump_atom[-1] == step)
            if clause:  # ensure clause is not empty
                self.clauses.append(clause)

    def encode_start_and_end_conditions(self):
        #start conditions
        for peg_atom, peg_idx in self.peg_atoms.items():
            if peg_atom[1]!= 1:
                continue
            if peg_atom[0] == self.init_empty_hole:
                self.clauses.append("-{}".format(peg_idx))
            else:
                self.clauses.append("{}".format(peg_idx))

        #end conditions
        for peg_atom, peg_idx in self.peg_atoms.items():
            if peg_atom[1] != self.steps:
                continue
            self.clauses.append(str(peg_idx))

    def generate_clauses(self):
        self.encode_preconditions()
        self.encode_causal_axioms()
        self.encode_frame_axioms()
        self.encode_one_action()
        self.encode_optional_actions()
        self.encode_start_and_end_conditions()

    def write_output_file(self, output_file):
        with open(output_file, "w") as file:
            for clause in self.clauses:
                file.write(clause + "\n")
            file.write("0\n")
            for jump, idx in self.jump_atoms.items():
                file.write("{} Jump{}\n".format(idx, jump))
            for peg, idx in self.peg_atoms.items():
                file.write("{} Peg{}\n".format(idx, peg))

    def process(self, input_file, output_file):
        self.preprocess(input_file)
        self.generate_clauses()
        self.write_output_file(output_file)
                
if __name__ == "__main__":
    frontend = FrontEnd()
    input_file = "fe_input.txt"
    output_file = "dp_input.txt"
    frontend.process(input_file, output_file)

