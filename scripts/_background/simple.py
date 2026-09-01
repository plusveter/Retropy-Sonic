from retropy import *

def bg_simple(data:dict[str, list[dict[str, dict]]]):

    layers = list()
    images_path = []
    for layer in data["layers"]:
        # Load image
        imagepath   = resolve_relative_path(data["pathfile"], layer["image"])
        if datapack.check_filepath(imagepath): images_path.append(imagepath)
        imagearray  = pygame.surfarray.array2d(datapack.load_8b_imagefile(imagepath))
        


        # Orientation
        orientation = str(layer.get("orientation", "n")[:1]).lower()
        # Vertical
        if orientation == "v":      _, axis_lenght  = imagearray.shape
        # Horizontal
        elif orientation == "h":    axis_lenght, _  = imagearray.shape
        # Other
        else:                       axis_lenght     = 0


        # Scroll arrays generator
        speed_1Darray       = []
        speed_params        = {"value": 0, "incre": None}

        cumul_1Darray       = []
        cumul_params        = {"value": 0, "incre": None}

        modul_1Darray       = []
        modul_params        = {"value": 0, "incre": None}

        def get_params(data:dict[str, dict]):
            return dict(value=data.get("value", 0), incre=data.get("increment", None))

        def update_params(params):
            if params["incre"] is not None:
                if   params["incre"]["type"]   == "addition":      params["value"] += params["incre"]["value"]
                elif params["incre"]["type"]   == "geometry":      params["value"] *= params["incre"]["value"]
            return params

        for axis in range(axis_lenght):
            # speed
            if layer['axis_scrolldata'].get(str(axis)):
                axis_data:dict[str, dict] = layer['axis_scrolldata'][str(axis)]
                if axis_data.get("speed"):      speed_params = get_params(axis_data["speed"])
                if axis_data.get("cumulation"): cumul_params = get_params(axis_data["cumulation"])
                if axis_data.get("modulo"): modul_params = get_params(axis_data["modulo"])

            speed_params    = update_params(speed_params)
            cumul_params    = update_params(cumul_params)
            modul_params    = update_params(modul_params)

            speed_1Darray.append(speed_params["value"])
            cumul_1Darray.append(cumul_params["value"])
            modul_1Darray.append(modul_params["value"])

        
        special_flag = str(layer.get("special_flag", "none")).lower()

        if      special_flag == "add":      special_flag = pygame.BLEND_ADD
        elif    special_flag == "mult":     special_flag = pygame.BLEND_MULT
        elif    special_flag == "min":      special_flag = pygame.BLEND_MIN
        elif    special_flag == "max":      special_flag = pygame.BLEND_MAX
        else:                               special_flag = 0


        # Combining into one layer
        offset = layer.get("offset", {})
        layers.append(
            dict( 
                offset_position  = offset.get("position"    , [0, 0]),
                offset_speed     = offset.get("speed"       , [0, 0]),
                surf_2Darray    = imagearray,
                speed_1Darray   = numpy.array(speed_1Darray),
                cumul_1Darray   = numpy.array(cumul_1Darray),
                orientation     = orientation,
                special_flag    = special_flag
            )
        )


    offset = data.get("offset", {})
    scroll = data.get("scroll", {})
    palette = data.get("palette", {})

    palfile = palette.get("palfile", -1)
    imgfile = palette.get("imgfile", -1)
    if palfile != -1: palette = load_from_palfile(resolve_relative_path(data["pathfile"], palfile))
    elif imgfile != -1: palette = load_palette_from_image(resolve_relative_path(data["pathfile"], imgfile))
    else:
        raise ProcessLookupError(
            f"[File='{data['pathfile']}']"
            +("\n"*2)+
            f"Palette hasn't been setup"
            +"\n"+
            """- example 1: "palette": {"palfile": ".\/path\/file.pal"}   """
            +"\n"+
            """- example 2: "palette": {"imgfile": ".\/path\/file.gif"}   """
            )

    return dict(
        offset_position     = offset.get("position"    , [0, 0]),
        offset_speed        = offset.get("speed"       , [0, 0]),
        scroll_position     = scroll.get("position"    , [0, 0]),
        scroll_speed        = scroll.get("speed"       , [0, 0]),

        layers              = layers,
        images_path         = images_path,

        colorpalette        = palette
    )