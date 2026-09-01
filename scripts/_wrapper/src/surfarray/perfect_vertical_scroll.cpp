#include <cstdint>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <emmintrin.h>
#include <unordered_set>
// OpenMP header


extern "C" {

    inline int wrap_index(int i, int max)
    {
        i %= max;
        return i < 0 ? i + max : i;
    }

    int perfect_vertical_scroll(
        const uint8_t* input,
        const double* array1D,
        int array_len,
        int roll,
        int width,
        int height,
        uint8_t* output)
    {
        if (!input || !output || width <= 0 || height <= 0)
            return -2;

        if (!array1D || array_len != width)
            return -1;

        const int base = wrap_index(roll, height);

        for (int x = 0; x < width; ++x)
        {
            const int per = static_cast<int>(std::llround(array1D[x]));
            const int shift = wrap_index(base + per, height);

            // Premier pixel source.
            int src_y = shift ? height - shift : 0;

            const uint8_t* src = input + src_y * width + x;
            uint8_t* dst = output + x;

            // Première partie : src_y -> height-1
            int count = height - src_y;

            for (int y = 0; y < count; ++y)
            {
                *dst = *src;

                src += width;
                dst += width;
            }

            // Deuxième partie : retour au début.
            src = input + x;
            dst = output + count * width + x;

            for (int y = count; y < height; ++y)
            {
                *dst = *src;

                src += width;
                dst += width;
            }
        }

        return 0;
    }
}