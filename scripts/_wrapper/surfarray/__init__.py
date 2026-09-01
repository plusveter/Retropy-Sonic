from .fake_alpha                    import fake_alpha_wrapper
from .perfect_horizontal_scroll     import perfect_horizontal_scroll_wrapper
from .perfect_vertical_scroll       import perfect_vertical_scroll_wrapper
from .apply_color_offset            import apply_color_offset_wrapper
from .rotate                        import rotate_wrapper
from .flip                          import flip_wrapper
from .scale                         import scale_wrapper

class SurfarrayWrapper:
    fake_alpha                      = staticmethod(fake_alpha_wrapper)
    perfect_horizontal_scroll       = staticmethod(perfect_horizontal_scroll_wrapper)
    perfect_vertical_scroll         = staticmethod(perfect_vertical_scroll_wrapper)
    apply_color_offset              = staticmethod(apply_color_offset_wrapper)
    rotate                          = staticmethod(rotate_wrapper)
    flip                            = staticmethod(flip_wrapper)
    scale                           = staticmethod(scale_wrapper)

