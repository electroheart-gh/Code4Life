import sys
import time
from inspect import currentframe


class DebugTool:
    def __init__(self):
        try:
            self.fd = open(r"input.txt")
        except (ImportError, OSError):
            self.debug_mode = False
        else:
            import matplotlib.pyplot as plt
            self.plt = plt
            self.fg = None
            self.ax = None
            self.debug_mode = True
            self.timer = None

    def input(self):
        if self.debug_mode:
            data = self.fd.readline()
        else:
            data = input()
        print(data, file=sys.stderr, flush=True)
        return data

    def start_timer(self):
        self.timer = time.time()

    def elapsed_time(self):
        end_time = time.time()
        interval = end_time - self.timer
        self.stderr(interval * 1000, "m sec")

    @staticmethod
    def stderr(*args):
        cf = currentframe()
        print(*args, "@" + str(cf.f_back.f_lineno), file=sys.stderr, flush=True)

    def plot_vector_clock(self, vct, clr="b", txt=""):
        # todo: refactor in OO style
        self.plt.plot((0, vct[0]), (0, vct[1]), color=clr)
        self.plt.text(vct[0], vct[1], txt)


class Robot:
    def __init__(self, target, eta, score,
                 storage_a, storage_b, storage_c, storage_d, storage_e,
                 expertise_a, expertise_b, expertise_c, expertise_d, expertise_e):
        self.target = target
        self.eta = int(eta)
        self.score = int(score)
        self.storage = (int(storage_a), int(storage_b), int(storage_c), int(storage_d), int(storage_e))
        self.expertise = (int(expertise_a), int(expertise_b), int(expertise_c), int(expertise_d), int(expertise_e))


class MoleculeSet:
    def __init__(self, type_a=0, type_b=0, type_c=0, type_d=0, type_e=0):
        self.a = int(type_a)
        self.b = int(type_b)
        self.c = int(type_c)
        self.d = int(type_d)
        self.e = int(type_e)

    def as_list(self):
        return [self.a, self.b, self.c, self.d, self.e]


class SampleData:
    def __init__(self, sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e):
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.cost = (int(cost_a), int(cost_b), int(cost_c), int(cost_d), int(cost_e))


class SampleDataList(list):
    def __init__(self, data_list=()):
        super().__init__(data_list)

    def ours(self):
        class_name = type(self)
        return class_name([e for e in self if e.carried_by == 0])  # type: class_name

    def theirs(self):
        class_name = type(self)
        return class_name([e for e in self if e.carried_by == 1])  # type: class_name

    def cloud(self):
        class_name = type(self)
        return class_name([e for e in self if e.carried_by == -1])  # type: class_name


#######################################
# Debugger Instantiation
#######################################
DT = DebugTool()

#######################################
# Constant Values
#######################################
DIAGNOSIS = "DIAGNOSIS"
MOLECULES = "MOLECULES"
LABORATORY = "LABORATORY"
CONNECT = "CONNECT "
GOTO = "GOTO "
TYPES = ("A", "B", "C", "D", "E")
# A = TYPES[0]
# B = TYPES[1]
# C = TYPES[2]
# D = TYPES[3]
# E = TYPES[4]


#######################################
# Parameters to be adjusted
#######################################

#######################################
# Initialization
#######################################
# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
#
project_count = int(DT.input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in DT.input().split()]

#######################################
# Game Loop
#######################################
while True:
    our_robot = Robot(*DT.input().split())
    their_robot = Robot(*DT.input().split())
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in DT.input().split()]
    sample_count = int(DT.input())
    samples = SampleDataList()
    for i in range(sample_count):
        samples.append(SampleData(*DT.input().split()))

    command = ""
    # At DIAGNOSIS, get minimum sample by 3 or go to MOLECULES
    if our_robot.target == DIAGNOSIS:
        # ToDo: Consider strategy (low cost first or high health and so on)
        if len(samples.ours()) < 3 and len(samples.cloud()) > 0:
            DT.stderr(min(samples.cloud(), key=lambda x: len(x.cost)))
            DT.stderr(min(samples.cloud(), key=lambda x: sum(x.cost)))
            command = CONNECT + str(min(samples.cloud(), key=lambda x: sum(x.cost)).sample_id)
        else:
            command = GOTO + MOLECULES

    # At MOLECULES, get molecules required for sample data or go to LABORATORY
    elif our_robot.target == MOLECULES:
        for i in range(len(TYPES)):
            if sum([s.cost[i] for s in samples.ours()]) > our_robot.storage[i]:
                command = CONNECT + TYPES[i]
                break
        if not command:
            command = GOTO + LABORATORY

    # At LABORATORY, if pass the possessions or go to DIAGNOSIS
    elif our_robot.target == LABORATORY:
        for s in samples.ours():
            command = CONNECT + str(s.sample_id)
        if not command:
            command = GOTO + DIAGNOSIS

    else:
        command = GOTO + DIAGNOSIS

    print(command)
