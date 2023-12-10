import messstellenbetreiber.start_msb as msb
from messstellenbetreiber.simulationTools.simulationTooling import SimulationTooling

tools: SimulationTooling = SimulationTooling("messstellenbetreiber/msbDatabase/msb.db")
tools.reset_db()
tools.add_testcase_data()
tools.add_random_stromzahler(8)

msb.start_msb("messstellenbetreiber/msbDatabase/msb.db")
