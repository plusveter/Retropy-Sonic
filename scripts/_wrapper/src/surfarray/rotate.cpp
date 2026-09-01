#include <cstdint>
#include <cmath>
#include <cstring>
#include <algorithm>

const double PI = 3.14159265358979323846;

extern "C" {

    void rotate(uint8_t* src, uint8_t* dst, int width, int height, int channels, double angle) {
        double rad = angle * PI / 180.0;

        // Precompute trig
        double cos_r = cos(rad);
        double sin_r = sin(rad);

        // New dimensions
        int new_width  = int(std::abs(width * cos_r) + std::abs(height * sin_r));
        int new_height = int(std::abs(width * sin_r) + std::abs(height * cos_r));

        double cx = width / 2.0;
        double cy = height / 2.0;
        double ncx = new_width / 2.0;
        double ncy = new_height / 2.0;

        memset(dst, 0, new_width * new_height * channels);

        for (int y = 0; y < new_height; ++y) {
            double y_offset = y - ncy;
            for (int x = 0; x < new_width; ++x) {
                double x_offset = x - ncx;

                // Map destination to source
                double sx = cos_r * x_offset + sin_r * y_offset + cx;
                double sy = -sin_r * x_offset + cos_r * y_offset + cy;

                int ix = int(sx + 0.5);
                int iy = int(sy + 0.5);

                if (ix >= 0 && ix < width && iy >= 0 && iy < height) {
                    for (int c = 0; c < channels; ++c) {
                        dst[(y*new_width + x)*channels + c] =
                            src[(iy*width + ix)*channels + c];
                    }
                }
            }
        }
    }

}