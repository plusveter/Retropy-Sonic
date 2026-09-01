#include <cstdint>
#include <algorithm>

extern "C" {

    void scale(
        uint8_t* src,
        uint8_t* dst,
        int width,
        int height,
        int new_width,
        int new_height
    ) {
        const double scale_x =
            static_cast<double>(width) / new_width;

        const double scale_y =
            static_cast<double>(height) / new_height;

        for (int x = 0; x < new_width; ++x) {

            int src_x = static_cast<int>(x * scale_x);

            if (src_x >= width)
                src_x = width - 1;

            for (int y = 0; y < new_height; ++y) {

                int src_y = static_cast<int>(y * scale_y);

                if (src_y >= height)
                    src_y = height - 1;

                // Array is [width, height]
                dst[x * new_height + y] =
                    src[src_x * height + src_y];
            }
        }
    }

}