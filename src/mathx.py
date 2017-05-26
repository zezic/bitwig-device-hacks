from lib import atoms
from lib import util

nitro_source = '''
component math2000 {
    audio_inport f32 a;
    audio_inport f32 b;
    value_inport i32 op;
    audio_outport f32 out;

    process {
        if (op == 0) {
            out = a + b;
        }
        else if (op == 1) {
            out = a - b;
        }
        else if (op == 2) {
            out = a * b;
        }
        else if (op == 3) {
            out = a / b;
        }
        else if (op == 4) {
            out = fabs(a);
        }
        else if (op == 5) {
            out = copysign(1.0, a);
        }
        else if (op == 6) {
            out = fmin(a, b);
        }
        else if (op == 7) {
            out = fmax(a, b);
        }
        else if (op == 8) {
            out = a * a;
        }
        else if (op == 9) {
            out = pow(a, b);
        }
        else if (op == 10) {
            out = sqrt(a);
        }
        else if (op == 11) {
            out = exp(a) * b;
        }
        else if (op == 12) {
            out = log(a) / log(b);
        }
        else if (op == 13) {
            out = log2(a);
        }
        else if (op == 14) {
            out = log10(a);
        }
        else if (op == 15) {
            out = log(a);
        }
        else if (op == 16) {
            out = b * sin(a);
        }
        else if (op == 17) {
            out = b * cos(a);
        }
        else if (op == 18) {
            out = b * sin(a) / cos(a);
        }
        else if (op == 19) {
            f32 bb = 20 * fmax(fabs(b), 0.00001);
            out = copysign(1.0, b) * trunc(a * bb) / bb;
        }
    }
}
'''.strip()

device_tooltip = '''
ADD - A + B
SUB - A - B
MUL - A * B
DIV - A / B
ABS - abs(A)
SIG - sig(A)
MIN - min(A, B)
MAX - max(A, B)
SQR - A^2
POW - A^B
SQRT - sqrt(A)
EXP - e^A * B
LOG - log{b}(A)
LOG2 - log2(A) * B
LOG10 - log10(A) * B
LN - ln(A) * B
SIN - sin(2π * A) * B
COS - cos(2π * A) * B
TAN - cos(2π * A) * B
QUA - Quantize A, with step size B
'''.strip()

modes = [
    'ADD', 'SUB', 'MUL', 'DIV',
    'ABS', 'SIG', 'MIN', 'MAX',
    'SQR', 'POW', 'SQRT', 'EXP',
    'LOG', 'LOG2', 'LOG10', 'LN',
    'SIN', 'COS', 'TAN', 'QUA',
]

value_a = atoms.DecimalValue('A', default = 0, min = -100, max = 100, step = 0.01)
value_b = atoms.DecimalValue('B', default = 0, min = -100, max = 100, step = 0.01)
value_mode = atoms.IndexedValue('MODE', default = 0, items = modes)

nitro = (atoms.Nitro()
    .add_inport(value_a)
    .add_inport(value_b)
    .add_inport(value_mode)
    .set_source(nitro_source))

mod_source = atoms.ModulationSource('MATH').add_inport(nitro)
poly_observer = atoms.PolyphonicObserver().add_inport(nitro)

grid_panel = (atoms.GridPanel()
    .add_item(atoms.MappingSourcePanelItem(model = mod_source)
        .set_position(0, 13))
    .add_item(atoms.PopupChooserPanelItem(model = value_mode)
        .set_tooltip(device_tooltip)
        .set_position(5, 0))
    .add_item(atoms.NumberFieldPanelItem(model = value_a, style = 2)
        .set_tooltip('Signal A')
        .set_position(2, 4)
        .with_value_bar())
    .add_item(atoms.NumberFieldPanelItem(model = value_b, style = 2)
        .set_tooltip('Signal B')
        .set_position(2, 9)
        .with_value_bar()))

modulator = (atoms.Modulator('Test')
    .set_description('Test device')
    .add_component(value_a)
    .add_component(value_b)
    .add_component(nitro)
    .add_component(mod_source)
    .add_component(poly_observer)
    .add_component(value_mode)
    .add_panel(atoms.Panel(grid_panel)))

device = modulator.serialize()
print(device)
