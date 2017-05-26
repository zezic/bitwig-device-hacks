from lib import util

object_id_counter = 0

def serialize(obj, state = {}):
    if isinstance(obj, Atom):
        if obj.object_id in state:
            return {
                "object_ref": obj.object_id,
            }
        data = serialize(obj.fields, state)
        state[obj.object_id] = True
        return {
            "class": obj.classname,
            "object_id": obj.object_id,
            "data": data,
        }
    if isinstance(obj, list):
        return [serialize(x, state) for x in obj]
    if isinstance(obj, dict):
        result = {}
        for i, value in obj.items():
            result[i] = serialize(value, state)
        return result
    return obj


class Atom:

    def __init__(self):
        global object_id_counter
        object_id_counter += 1
        self.object_id = object_id_counter

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        return None

    def serialize(self):
        return serialize(self)


class Meta(Atom):

    classname = "meta"

    def __init__(self, name):
        super().__init__()
        self.fields = {
            "application_version_name": "none",
            "branch": "alex/future",
            "comment": "",
            "creator": "Bitwig",
            "device_category": "Control",
            "device_description": "",
            "device_id": "modulator:6146bcd7-f813-44c6-96e5-2e9d77093a81",
            "device_name": name,
            "device_uuid": "6146bcd7-f813-44c6-96e5-2e9d77093a81",
            "is_polyphonic": False,
            "revision_id": "b3ddbde8410232c8105778921a53ff99045bd547",
            "revision_no": 51805,
            "tags": "",
            "type": "application/bitwig-modulator",
        }


class Modulator(Atom):

    classname = "float_core.modulator_contents"

    def __init__(self, name):
        super().__init__()
        self.fields = {
            "settings": None,
            "child_components": [],
            "panels": [],
            "proxy_in_ports": [],
            "proxy_out_ports": [],
            "fft_order": 0,
            "context_menu_panel": None,
            "device_UUID": "6146bcd7-f813-44c6-96e5-2e9d77093a81",
            "device_name": name,
            "description": "Simple 2-operator math",
            "creator": "Bitwig",
            "comment": "",
            "keywords": "",
            "category": "Control",
            "has_been_modified": True,
            "detail_panel": None,
            "can_be_polyphonic": True,
            "should_be_polyphonic_by_default": False,
            "should_enable_perform_mode_by_default": False,
        }
        self.meta = Meta(name)
        self.set_uuid(util.uuid_from_text(name))

    def add_component(self, component):
        self.fields['child_components'].append(component)
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


class DecimalValue(Atom):

    classname = "float_core.decimal_value_atom"

    def __init__(self, name, min = None, max = None, unit = None, default = None):
        super().__init__()
        self.fields = {
            "settings": Settings(),
            "channel_count": 0,
            "oversampling": 0,
            "name": name,
            "label": "",
            "tooltip_text": "Receive the input signal",
            "preset_identifier": name,
            "modulations_to_ignore": "MATH",
            "value_type": DecimalValueType(),
            "value": 0.0
        }
        if min != None:
            self.value_type.fields['min'] = min
        if max != None:
            self.value_type.fields['max'] = max
        if unit != None:
            self.value_type.fields['unit'] = unit
        if default != None:
            self.value_type.fields['default_value'] = default

    def set_range(self, min, max):
        self.value_type.fields['min'] = min
        self.value_type.fields['max'] = max
        return self


class DecimalValueType(Atom):

    classname = "float_core.decimal_value_type"

    def __init__(self):
        super().__init__()
        self.fields = {
            "min": -1.0,
            "max": 1.0,
            "default_value": 0.0,
            "domain": 0,
            "engine_domain": 0,
            "value_origin": 0,
            "pixel_step_size": -1.0,
            "unit": 1,
            "decimal_digit_count": -1,
            "edit_style": 0,
            "parameter_smoothing": True,
            "allow_automation_curves": True,
        }


class Settings(Atom):

    classname = "float_core.component_settings"

    def __init__(self):
        super().__init__()
        self.fields = {
            "desktop_settings": DesktopSettings(),
            "inport_connections": [],
            "is_polyphonic": True,
        }

    def add_connection(self, x):
        self.inport_connections.append(x)
        return self


class DesktopSettings(Atom):

    classname = "float_core.desktop_settings"

    def __init__(self):
        super().__init__()
        self.fields = {
            "x": 284,
            "y": 156,
            "color": {
                "type": "color",
                "data": [ 0.5, 0.5, 0.5 ],
            },
        }


class Nitro(Atom):

    classname = "float_common_atoms.nitro_atom"

    def __init__(self):
        super().__init__()
        self.fields = {
            "settings": Settings(),
            "channel_count": 1,
            "oversampling": 0,
            "code": None,
            "fft_order": 0,
        }

    def add_inport(self, atom):
        self.settings.add_connection(InportConnection(atom))
        return self

    def set_source_file(self, file):
        # TODO
        return self


class InportConnection(Atom):

    classname = "float_core.inport_connection"

    def __init__(self, atom = None):
        super().__init__()
        self.fields = {
            "source_component": atom,
            "outport_index": 0,
            "high_quality": True,
            "unconnected_value": 0.0
        }

    def set_source(self, atom):
        self.source_component = atom
        return self


class Panel(Atom):

    classname = "float_core.panel"

    def __init__(self, atom = None):
        super().__init__()
        self.fields = {
            "layout_settings": None,
            "is_visible": True,
            "is_enabled": True,
            "tooltip_text": "",
            "root_item": None, # TODO
            "name": "Main",
            "width": 17,
            "height": 17,
            "expressions": [],
        }
