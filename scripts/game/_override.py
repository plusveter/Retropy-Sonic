from scripts.base import *

import retropy

def render_prerender():
    """ [Retropy | Graphic | Surfarray] """
    apply_color_offset_on_prerender()
    render_surfarray(graphic.surfarray, pivot=graphic.pivot, special_flags=graphic.special_flags, offset=graphic.offset, palette_id=graphic.palette)

retropy.render_prerender = render_prerender