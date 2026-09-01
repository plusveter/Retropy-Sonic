vec2 crtUV = crtCurve(scaledUV);

// Black outside the curved screen
if ( crtUV.x < 0.0 || crtUV.x > 1.0 || crtUV.y < 0.0 || crtUV.y > 1.0) { vec4 fgColor = vec4(0.0); return; }

// -------------------------
// Chromatic aberration
// -------------------------
float separation = 0.0015;

// Color
float r = texture2D( uScreen, crtUV + vec2(separation, 0.0) ).r;
float g = texture2D( uScreen, crtUV ).g;
float b = texture2D( uScreen, crtUV - vec2(separation, 0.0) ).b;
vec3 color = vec3(r, g, b);

// -------------------------
// Scanlines
// -------------------------

float scanline = sin(crtUV.y * uRes.y * 1.0 * 3.14159);

// Make dark lines
float scan = mix(0.82, 1.0, scanline * 0.5 + 0.5);
color *= scan;

// -------------------------
// Horizontal pixel/RGB structure
// -------------------------
float subpixel = sin(crtUV.x * uRes.x * 3.14159);
color *= 1.0 - subpixel * 0.025;

// -------------------------
// Vignette
// -------------------------
vec2 vignetteUV = crtUV * 2.0 - 1.0;

float vignette = 1.0 - dot(vignetteUV, vignetteUV) * 0.18;
vignette = clamp(vignette, 0.0, 1.0);
color *= vignette;

// -------------------------
// Slight CRT glow
// -------------------------
color += color * color * 0.12;

// -------------------------
// Subtle noise
// -------------------------
float noise = fract(
    sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233)))
    * 43758.5453
);

color += (noise - 0.5) * 0.015;

fgColor = vec4(color, 1.0);