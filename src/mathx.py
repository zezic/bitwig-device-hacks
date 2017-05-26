from lib import atoms
from lib import util

knobA = atoms.DecimalValue('A', default = 0,
    min = -10, max = 10)

knobB = atoms.DecimalValue('B', default = 0,
    min = -10, max = 10)

nitro = (atoms.Nitro()
    .add_inport(knobA)
    .add_inport(knobB)
    .set_source_file('mathx.nitro'))

modulator = (atoms.Modulator('Test')
    .set_description('Test device')
    .add_component(knobA)
    .add_component(knobB))

util.json_print(modulator.meta.serialize())
util.json_print(modulator.serialize())
