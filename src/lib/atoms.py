from lib import util

class Modulator:

    meta = {
        "application_version_name": "none",
        "branch": "alex/future",
        "comment": "",
        "creator": "Bitwig",
        "device_category": "Control",
        "device_description": "",
        "device_id": "modulator:6146bcd7-f813-44c6-96e5-2e9d77093a81",
        "device_name": "",
        "device_uuid": "6146bcd7-f813-44c6-96e5-2e9d77093a81",
        "is_polyphonic": False,
        "revision_id": "b3ddbde8410232c8105778921a53ff99045bd547",
        "revision_no": 51805,
        "tags": "",
        "type": "application/bitwig-modulator",
    }

    data = {
        "settings": None,
        "child_components": [],
        "panels": [],
        "proxy_in_ports": [],
        "proxy_out_ports": [],
        "fft_order": 0,
        "context_menu_panel": None,
        "device_UUID": "6146bcd7-f813-44c6-96e5-2e9d77093a81",
        "device_name": "Math",
        "description": "Simple 2-operator math",
        "creator": "Bitwig",
        "comment": "",
        "keywords": "",
        "category": "Control",
        "has_been_modified": True,
        "detail_panel": None,
        "can_be_polyphonic": True,
        "should_be_polyphonic_by_default": False,
        "should_enable_perform_mode_by_default": False
    }

    def __init__(self, name):
        self.meta['device_name'] = name
        self.data['device_name'] = name
        self.uuid(util.uuid_from_text(name))

    def description(self, value):
        self.meta['device_description'] = value
        self.data['description'] = value
        return self

    def uuid(self, value):
        self.meta['device_uuid'] = value
        self.meta['device_id'] = 'modulator:' + value
        self.data['device_UUID'] = value
        return self

    def build_meta(self):
        return {
            "class": "meta",
            "data": self.meta,
        }

    def build(self):
        return {
            "class": "float_core.modulator_contents",
            "data": self.data,
        }
