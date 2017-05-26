from collections import OrderedDict
from lib import util

## Serializes all device atoms
def serialize(obj, state = None):
    if state == None:
        state = []
    if isinstance(obj, Atom):
        if obj in state:
            return {
                'object_ref': state.index(obj) + 1,
            }
        state.append(obj)
        data = serialize(obj.fields, state)
        return OrderedDict([
            ('class', obj.classname),
            ('object_id', state.index(obj) + 1),
            ('data', data)
        ])
    if isinstance(obj, list):
        return [serialize(x, state) for x in obj]
    if isinstance(obj, dict):
        result = OrderedDict()
        for i, value in obj.items():
            result[i] = serialize(value, state)
        return result
    return obj


class Atom:

    def __init__(self, classname = None, fields = None):
        if classname != None:
            self.classname = classname
        if fields != None:
            self.fields = fields

    def add_inport(self, atom):
        self.fields['settings'].add_connection(InportConnection(atom))
        return self


class Meta(Atom):

    classname = 'meta'

    def __init__(self, name, description = '', type = ''):
        self.fields = OrderedDict([
            ('application_version_name', 'none'),
            ('branch', 'alex/future'),
            ('comment', ''),
            ('creator', 'Bitwig'),
            ('device_category', 'Control'),
            ('device_description', description),
            ('device_id', 'modulator:6146bcd7-f813-44c6-96e5-2e9d77093a81'),
            ('device_name', name),
            ('device_uuid', '6146bcd7-f813-44c6-96e5-2e9d77093a81'),
            ('is_polyphonic', False),
            ('revision_id', 'b3ddbde8410232c8105778921a53ff99045bd547'),
            ('revision_no', 51805),
            ('tags', ''),
            ('type', type)
        ])


class Modulator(Atom):

    classname = 'float_core.modulator_contents'

    def __init__(self, name, description = 'Custom modulator',
            header = 'BtWg000100010088000015e50000000000000000'):
        self.fields = OrderedDict([
            ('settings', None),
            ('child_components', []),
            ('panels', []),
            ('proxy_in_ports', []),
            ('proxy_out_ports', []),
            ('fft_order', 0),
            ('context_menu_panel', None),
            ('device_UUID', '6146bcd7-f813-44c6-96e5-2e9d77093a81'),
            ('device_name', name),
            ('description', description),
            ('creator', 'Bitwig'),
            ('comment', ''),
            ('keywords', ''),
            ('category', 'Control'),
            ('has_been_modified', True),
            ('detail_panel', None),
            ('can_be_polyphonic', True),
            ('should_be_polyphonic_by_default', False),
            ('should_enable_perform_mode_by_default', False)
        ])
        self.meta = Meta(name, description, 'application/bitwig-modulator')
        self.header = header
        self.set_uuid(util.uuid_from_text(name))

    def add_component(self, atom):
        self.fields['child_components'].append(atom)
        return self

    def add_panel(self, atom):
        self.fields['panels'].append(atom)
        return self

    def add_proxy_in(self, atom):
        self.fields['proxy_in_ports'].append(atom)
        return self

    def add_proxy_out(self, atom):
        self.fields['proxy_out_ports'].append(atom)
        return self

    def set_description(self, value):
        self.meta.fields['device_description'] = value
        self.fields['description'] = value
        return self

    def set_uuid(self, value):
        self.meta.fields['device_uuid'] = value
        self.meta.fields['device_id'] = 'modulator:' + value
        self.fields['device_UUID'] = value
        return self

    def serialize(self):
        return util.serialize_bitwig_device(OrderedDict([
            ('header', self.header),
            ('meta', serialize(self.meta)),
            ('contents', serialize(self))
        ]))


class AbstractValue(Atom):

    def __init__(self, name, default = None, tooltip = '', label = ''):
        self.fields = OrderedDict([
            ('settings', Settings()),
            ('channel_count', 0),
            ('oversampling', 0),
            ('name', name),
            ('label', label),
            ('tooltip_text', tooltip),
            ('preset_identifier', name.upper()),
            ('modulations_to_ignore', 'MATH'),
            ('value_type', None),
            ('value', default)
        ])


class DecimalValue(AbstractValue):

    classname = 'float_core.decimal_value_atom'

    def __init__(self, name, default = 0, tooltip = '', label = '',
            min = -1, max = 1, unit = 0, step = -1, precision = -1):
        default = float(default)
        min = float(min)
        max = float(max)
        super().__init__(name, default, tooltip, label)
        self.fields['value_type'] = Atom('float_core.decimal_value_type', OrderedDict([
            ('min', min),
            ('max', max),
            ('default_value', default),
            ('domain', 0),
            ('engine_domain', 0),
            ('value_origin', 0),
            ('pixel_step_size', step),
            ('unit', unit),
            ('decimal_digit_count', precision),
            ('edit_style', 0),
            ('parameter_smoothing', True),
            ('allow_automation_curves', True)
        ]))

    def set_range(self, min, max):
        self.fields['value_type'].fields['min'] = float(min)
        self.fields['value_type'].fields['max'] = float(max)
        return self

    def use_smoothing(self, smoothing = True):
        self.fields['value_type'].fields['parameter_smoothing'] = smoothing

    def set_decimal_digit_count(self, decimal_digit_count):
        self.fields['value_type'].fields['decimal_digit_count'] = decimal_digit_count
        return self

    def set_decimal_digit_count(self, decimal_digit_count):
        self.fields['value_type'].fields['decimal_digit_count'] = decimal_digit_count
        return self

    def set_step(self, step):
        self.fields['value_type'].fields['pixel_step_size'] = step
        return self


class IndexedValue(AbstractValue):

    classname = 'float_core.indexed_value_atom'

    def __init__(self, name, default = 0, tooltip = '', label = '',
            items = []):
        super().__init__(name, default, tooltip, label)
        self.fields['value_type'] = Atom('float_core.indexed_value_type', OrderedDict([
            ('items', []),
            ('edit_style', 0),
            ('columns', 0),
            ('default_value', default)
        ]))
        for x in items:
            self.add_item(x)

    def add_item(self, name):
        items = self.fields['value_type'].fields['items']
        seq_id = len(items)
        items.append(Atom('float_core.indexed_value_item', OrderedDict([
            ('id', seq_id),
            ('name', name)
        ])))
        return self


class Settings(Atom):

    classname = 'float_core.component_settings'

    def __init__(self):
        self.fields = OrderedDict([
            ('desktop_settings', Atom('float_core.desktop_settings', OrderedDict([
                ('x', 0),
                ('y', 0),
                ('color', OrderedDict([
                    ('type', 'color'),
                    ('data', [ 0.5, 0.5, 0.5 ])
                ]))
            ]))),
            ('inport_connections', []),
            ('is_polyphonic', True)
        ])

    def add_connection(self, atom):
        self.fields['inport_connections'].append(atom)
        return self


class InportConnection(Atom):

    classname = 'float_core.inport_connection'

    def __init__(self, atom = None):
        self.fields = OrderedDict([
            ('source_component', atom),
            ('outport_index', 0),
            ('high_quality', True),
            ('unconnected_value', 0.0),
        ])

    def set_source(self, atom):
        self.source_component = atom
        return self


class Nitro(Atom):

    classname = 'float_common_atoms.nitro_atom'

    def __init__(self):
        self.fields = OrderedDict([
            ('settings', Settings()),
            ('channel_count', 1),
            ('oversampling', 0),
            ('code', None),
            ('fft_order', 0)
        ])

    def set_source_file(self, file):
        # TODO
        return self

    def set_source(self, code):
        self.fields['code'] = code
        return self


class ModulationSource(Atom):

    classname = 'float_core.modulation_source_atom'

    def __init__(self, name = ''):
        self.fields = OrderedDict([
            ('settings', Settings()),
            ('channel_count', 1),
            ('oversampling', 0),
            ('name', name),
            ('preset_identifier', name.upper()),
            ('display_settings', OrderedDict([
                ('type', 'map<string,object>'),
                ('data', OrderedDict([
                    ('abique', Atom('float_core.modulation_source_atom_display_settings', {
                        'is_source_expanded_in_inspector': False,
                    })),
                ]))
            ]))
        ])


class PolyphonicObserver(Atom):

    classname = 'float_core.polyphonic_observer_atom'

    def __init__(self):
        self.fields = OrderedDict([
            ('settings', Settings()),
            ('channel_count', 1),
            ('oversampling', 0),
            ('dimensions', 1)
        ])


class AbstractPanel(Atom):

    def __init__(self, tooltip = ''):
        self.fields = OrderedDict([
            ('layout_settings', None),
            ('is_visible', True),
            ('is_enabled', True),
            ('tooltip_text', tooltip)
        ])

    def set_tooltip(self, text):
        self.fields['tooltip_text'] = text
        return self


class AbstractPanelItem(AbstractPanel):

    def __init__(self, tooltip = '', x = 0, y = 0, width = 17, height = 4):
        super().__init__(tooltip)
        self.fields['layout_settings'] = Atom('float_core.grid_panel_item_layout_settings', OrderedDict([
            ('width', width),
            ('height', height),
            ('x', x),
            ('y', y)
        ]))

    def set_size(self, width, height):
        self.fields['layout_settings'].fields['width'] = width
        self.fields['layout_settings'].fields['height'] = height
        return self

    def set_position(self, x, y):
        self.fields['layout_settings'].fields['x'] = x
        self.fields['layout_settings'].fields['y'] = y
        return self

    def set_model(self, atom):
        self.fields['data_model'] = model
        return self


class Panel(AbstractPanel):

    classname = 'float_core.panel'

    def __init__(self, root_item, width = 17, height = 17, name = 'Main',
            tooltip = ''):
        super().__init__(tooltip)
        self.fields['root_item'] = root_item
        self.fields['name'] = name
        self.fields['width'] = width
        self.fields['height'] = height
        self.fields['expressions'] = []


class GridPanel(AbstractPanel):

    classname = 'float_core.grid_panel_item'

    def __init__(self, tooltip = '', title = ''):
        super().__init__(tooltip)
        self.fields['items'] = []
        self.fields['border_style'] = 1
        self.fields['title'] = title
        self.fields['show_title'] = title != ''
        self.fields['title_color'] = 6
        self.fields['brightness'] = 0

    def add_item(self, atom):
        self.fields['items'].append(atom)
        return self


class MappingSourcePanelItem(AbstractPanelItem):

    classname = 'float_core.mapping_source_panel_item'

    def __init__(self, tooltip = '', x = 0, y = 0, width = 17, height = 4,
            model = None):
        super().__init__(tooltip, x, y, width, height)
        self.fields['data_model'] = model
        self.fields['title'] = ''
        self.fields['filename'] = ''


class PopupChooserPanelItem(AbstractPanelItem):

    classname = 'float_core.popup_chooser_panel_item'

    def __init__(self, tooltip = '', x = 0, y = 0, width = 7, height = 4,
            model = None):
        super().__init__(tooltip, x, y, width, height)
        self.fields['data_model'] = model
        self.fields['label_style'] = 0
        self.fields['style'] = 1


class KnobPanelItem(AbstractPanelItem):

    classname = 'float_core.knob_panel_item'

    def __init__(self, tooltip = '', x = 0, y = 0, width = 9, height = 7,
            model = None, size = 1, style = 0):
        super().__init__(tooltip, x, y, width, height)
        self.fields['data_model'] = model
        self.fields['title'] = ''
        self.fields['knob_size'] = size
        self.fields['knob_style'] = style
        self.fields['label_color'] = 999
        self.fields['pie_color'] = 999


class NumberFieldPanelItem(AbstractPanelItem):

    classname = 'float_core.number_field_panel_item'

    def __init__(self, tooltip = '', x = 0, y = 0, width = 13, height = 4,
            model = None, style = 0, show_value_bar = False):
        super().__init__(tooltip, x, y, width, height)
        self.fields['data_model'] = model
        self.fields['title'] = ''
        self.fields['style'] = style
        self.fields['show_value_bar'] = show_value_bar

    def with_value_bar(self):
        self.fields['show_value_bar'] = True
        return self


class ProxyInPort(Atom):

    classname = 'float_core.proxy_in_port_component'

    def __init__(self, atom):
        self.fields = OrderedDict([
            ('settings', Settings()),
            ('port', atom)
        ])


class AudioPort(Atom):

    classname = 'float_core.audio_port'

    def __init__(self):
        self.fields = OrderedDict([
            ('name', ''),
            ('description', ''),
            ('decorated_name', ' Audio out (PARENT)'),
            ('is_inport', False),
            ('is_optional', False),
            ('exclude_from_graph', False),
            ('channel_count', 3)
        ])


class NotePort(Atom):

    classname = 'float_core.note_port'

    def __init__(self):
        self.fields = OrderedDict([
            ('name', ''),
            ('description', ''),
            ('decorated_name', ' Note out'),
            ('is_inport', False),
            ('is_optional', False),
            ('exclude_from_graph', False)
        ])
