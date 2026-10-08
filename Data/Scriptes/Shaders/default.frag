#version 330 core

in vec2 uvs;
out vec4 f_color;

// Uniforms
uniform sampler2D uScreen; // In-game screen texture 
uniform sampler2D uFilter; // Visual Filter

uniform vec2 uWin; // Window size (e.g., 800 x 600) 
uniform vec2 uRes; // In-game screen resolution (e.g., 512 x 512)

uniform float frames;


vec4 applyCRT(
    vec2 uv,
    vec2 resolution,
    sampler2D screenTexture
)
{
    // =====================================================
    // CRT CURVE
    // =====================================================

    vec2 crtUV = uv * 2.0 - 1.0;

    float r2 = dot(crtUV, crtUV);

    crtUV *= 1.0 + r2 * 0.08;

    crtUV = crtUV * 0.5 + 0.5;

    float offsetx = sin((uv.y*1000) + (frames*2))/1000;
    float offsety = (sin(uv.x*1000000)+2)/2;


    // =====================================================
    // OUTSIDE SCREEN
    // =====================================================

    if (crtUV.x < 0.0 ||
        crtUV.x > 1.0 ||
        crtUV.y < 0.0 ||
        crtUV.y > 1.0)
    {
        return vec4(0.0);
    }


    // =====================================================
    // CHROMATIC ABERRATION
    // =====================================================

    float separation = 0.0015 + offsetx;

    float r = texture2D(
        screenTexture,
        crtUV + vec2(separation, 0.0) 
    ).r;

    float g = texture2D(
        screenTexture,
        crtUV
    ).g;

    float b = texture2D(
        screenTexture,
        crtUV - vec2(separation, 0.0)
    ).b;

    vec3 color = vec3(r, g, b)*offsety;


    // =====================================================
    // SCANLINES
    // =====================================================

    float scanY = crtUV.y * resolution.y;

    float linePos = fract(scanY);

    float lineEdge = min(
        linePos,
        1.0 - linePos
    );

    // Largeur des zones sombres
    float darkWidth = 0.22;

    float darkLine = 1.0 - smoothstep(
        0.0,
        darkWidth,
        lineEdge
    );

    // Intensité globale
    float scanlineStrength = 0.52;

    float scanline =
        1.0 - darkLine * scanlineStrength;

    color *= scanline;


    // =====================================================
    // PHOSPHOR GLOW
    // =====================================================

    float centerDist =
        abs(linePos - 0.5) * 2.0;

    float phosphorGlow =
        1.0 - smoothstep(
            0.0,
            0.85,
            centerDist
        );

    color += color * phosphorGlow * 0.045;


    // =====================================================
    // SCANLINE VARIATION
    // =====================================================

    float lineNumber = floor(scanY);

    float lineNoise = fract(
        sin(lineNumber * 12.9898) *
        43758.5453
    );

    float lineVariation =
        mix(0.94, 1.06, lineNoise);

    color *= lineVariation;


    // =====================================================
    // RGB PHOSPHOR
    // =====================================================

    float pixelX = crtUV.x * resolution.x;

    float redMask =
        sin(pixelX * 3.14159 * 2.0);

    float greenMask =
        sin(
            pixelX * 3.14159 * 2.0 +
            2.094
        );

    float blueMask =
        sin(
            pixelX * 3.14159 * 2.0 +
            4.188
        );

    vec3 phosphorMask = vec3(
        redMask,
        greenMask,
        blueMask
    );

    color *=
        1.0 + phosphorMask * 0.035;


    // =====================================================
    // VIGNETTE
    // =====================================================

    vec2 vignetteUV =
        crtUV * 2.0 - 1.0;

    float vignette =
        1.0 -
        dot(vignetteUV, vignetteUV) *
        0.18;

    vignette = clamp(
        vignette,
        0.0,
        1.0
    );

    color *= vignette;


    // =====================================================
    // CRT GLOW
    // =====================================================

    color += color * color * 0.12;


    // =====================================================
    // NOISE
    // =====================================================

    float noise = fract(
        sin(
            dot(
                gl_FragCoord.xy,
                vec2(12.9898, 78.233)
            )
        ) *
        43758.5453
    );

    color += (noise - 0.5) * 0.015;


    return vec4(color, 1.0);
}

void main()
{
    float windowAspect = uWin.x / uWin.y;
    float textureAspect = uRes.x / uRes.y;

    vec2 scaledUV = uvs;
    bool is_screen = true;

    if (windowAspect > textureAspect)
    {
        float scale = textureAspect / windowAspect;
        float xOffset = (1.0 - scale) / 2.0;

        scaledUV.x =
            (uvs.x - xOffset) / scale;

        is_screen =
            uvs.x >= xOffset &&
            uvs.x <= (1.0 - xOffset);
    }
    else
    {
        float scale = windowAspect / textureAspect;
        float yOffset = (1.0 - scale) / 2.0;

        scaledUV.y =
            (uvs.y - yOffset) / scale;

        is_screen =
            uvs.y >= yOffset &&
            uvs.y <= (1.0 - yOffset);
    }


    vec4 bgColor = vec4(0.0);

    vec4 fgColor;

    bool does_crtScreen_enable = bool(0); 
    texture2D(uFilter, uvs);


    if (does_crtScreen_enable)
    {
        fgColor = applyCRT(
            scaledUV,
            uRes,
            uScreen
        );
    }
    else
    {
        fgColor = texture2D(
            uScreen,
            scaledUV
        );
    }


    f_color =
        is_screen
        ? fgColor
        : bgColor;
}