from scripts.base import *


class CameraTool(TiledObjectEntity):
        camera_sides = {
            "boundary_up": CAMERA_BOUND_TOP,
            "boundary_down": CAMERA_BOUND_BOTTOM,
            "boundary_left": CAMERA_BOUND_LEFT,
            "boundary_right": CAMERA_BOUND_RIGHT,
        }

        def update(self):
            super().update()
            if camera.mode == -1:
                return

            camera_side = self.camera_sides.get(self.tiled_name)
            if camera_side is None:
                return

            camera.set_bound(
                self.bound,
                camera_side,
                set_speed=self.tiled_properties.get("set_speed"),
                disable_screen_focus=self.tiled_properties.get("disable_screen_focus"),
                disable_player_focus=self.tiled_properties.get("disable_player_focus"),
                enable_decrease=self.tiled_properties.get("enable_decrease"),
            )