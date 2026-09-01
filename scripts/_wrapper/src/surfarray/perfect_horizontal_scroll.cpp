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

    int perfect_horizontal_scroll(
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

        if (!array1D || array_len != height)
            return -1;

        const int base = wrap_index(roll, width);

        for (int y = 0; y < height; ++y)
        {
            const int per = static_cast<int>(std::llround(array1D[y]));
            const int shift = wrap_index(base + per, width);

            const int row = y * width;

            // output[x] = input[x - shift]
            //
            // Premier morceau :
            // input[width - shift ... width - 1]
            // -> output[0 ... shift - 1]

            if (shift > 0)
            {
                std::memcpy(
                    output + row,
                    input + row + width - shift,
                    shift
                );

                // Deuxième morceau :
                // input[0 ... width-shift-1]
                // -> output[shift ... width-1]

                std::memcpy(
                    output + row + shift,
                    input + row,
                    width - shift
                );
            }
            else
            {
                // Aucun déplacement.
                std::memcpy(
                    output + row,
                    input + row,
                    width
                );
            }
        }

        return 0;
    }
}