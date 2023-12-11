import json
import logging
import re
from typing import List

import bpy

log = logging.getLogger(__name__)

VISEMES_LIST = ["ah", "ch", "u", "e", "oh"]
VISEME_PREFIX_REGEX = re.compile(f"^(.*[._-])?(?:{'|'.join(VISEMES_LIST)})$", re.IGNORECASE)

# (PropertyName , DisplayText)
SHAPEKEY_LIST = [("blink", None),
                ("blink_2", "blink 2"),
                ("wink", None),
                ("wink_right", None),
                ("wink_2", None),
                ("wink_2_right", None),
                ("kirieye", None),
                ("close_X", "> <"),
                ("open_o", None),
                ("howawa", None),
                ("ha", None),
                ("jitoeye", None),
                ("bottomlid_up", None),
                ("anger_eye", None),
                ("eyestar", None),
                ("eyestar2", None),
                ("eyeheart", None),
                ("starlight", None),
                ("eye_small", None),
                ("eye_funky", None),
                ("round_eye", None),
                ("eye_small_h", None),
                ("eye_invert", None),
                ("eye_hi_off", None)]


def determine_prefix(shapekeys: List[bpy.types.ShapeKey]) -> str:
    for sk in shapekeys:
        matches = re.match(VISEME_PREFIX_REGEX, sk.name)
        if matches:
            return matches.group(1) or ""

    # prefix could not be determined
    return ""


def show_message_box(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class CopyAsMMDSettings(bpy.types.PropertyGroup):
    # Visemes
    # @formatter:off
    ah: bpy.props.StringProperty()
    ch: bpy.props.StringProperty()
    u:  bpy.props.StringProperty()
    e:  bpy.props.StringProperty()
    oh: bpy.props.StringProperty()

    # Shapekeys
    blink:           bpy.props.StringProperty()
    blink_2:         bpy.props.StringProperty()
    wink:            bpy.props.StringProperty()
    wink_right:      bpy.props.StringProperty()
    wink_2:          bpy.props.StringProperty()
    wink_2_right:    bpy.props.StringProperty()
    kirieye:         bpy.props.StringProperty()
    close_X:         bpy.props.StringProperty(description="Close Eyes, >.< shaped")
    open_o:          bpy.props.StringProperty()
    howawa:          bpy.props.StringProperty()
    ha:              bpy.props.StringProperty()
    jitoeye:         bpy.props.StringProperty()
    bottomlid_up:    bpy.props.StringProperty()
    anger_eye:       bpy.props.StringProperty()
    eyestar:         bpy.props.StringProperty()
    eyestar2:        bpy.props.StringProperty()
    eyeheart:        bpy.props.StringProperty()
    starlight:       bpy.props.StringProperty()
    eye_small:       bpy.props.StringProperty()
    eye_funky:       bpy.props.StringProperty()
    round_eye:       bpy.props.StringProperty()
    eye_small_h:     bpy.props.StringProperty()
    eye_invert:      bpy.props.StringProperty()
    eye_hi_off:      bpy.props.StringProperty()
    # @formatter:on

    prefill_existing_JP_shapekeys: bpy.props.BoolProperty(
        default=True,
        description="Prefill with existing Japanese shape keys? \n"
                    "(Those shape keys will not be duplicated, only act as a placeholder)")

    def set_attribute(self, attribute: str, value: str) -> None:
        if not attribute:
            return

        attribute = attribute.lower().replace(" ", "_")
        # Set variable if empty
        if hasattr(self, attribute):
            if not getattr(self, attribute):
                setattr(self, attribute, value)
            return

        # common variations
        if attribute == "aa":
            self.set_attribute("ah", value)
        elif attribute == "ee":
            self.set_attribute("e", value)
        elif attribute.startswith("wink2"):
            self.set_attribute(attribute.replace("wink2", "wink_2"), value)

    def import_from_json(self, json_string: str, shapekeys: List[bpy.types.ShapeKey]) -> None:
        try:
            json_data = json.loads(json_string)
            shapekey_names = [sk.name.lower() for sk in shapekeys]
            for (key, value) in json_data.items():
                print(key, value)
                # ignore references to shapekeys that do not exist on the model
                if hasattr(self, key) and value.lower() in shapekey_names:
                    setattr(self, key, value)
        except json.JSONDecodeError:
            show_message_box("Data is not a valid JSON", "Import Error", "ERROR")

    def export_to_json(self) -> str:
        data = {
            "ah": self.ah,
            "ch": self.ch,
            "u": self.u,
            "e": self.e,
            "oh": self.oh,
            "blink_happy": self.blink_happy,
            "blink": self.blink,
            "close_X": self.close_X,
            "calm": self.calm,
            "stare": self.stare,
            "wink": self.wink,
            "wink_right": self.wink_right,
            "wink_2": self.wink_2,
            "wink_2_right": self.wink_2_right,
            "cheerful": self.cheerful,
            "serious": self.serious,
            "upper": self.upper,
            "lower": self.lower,
            "anger": self.anger,
            "sadness": self.sadness,
        }
        # Remove empty values
        data = {k: v for k, v in data.items() if v}
        return json.dumps(data, indent=2)
