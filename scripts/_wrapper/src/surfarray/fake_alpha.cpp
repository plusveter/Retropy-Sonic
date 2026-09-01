#include <cstdint>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <emmintrin.h>
#include <unordered_set>
// OpenMP header



extern "C" {

    void fake_alpha(uint8_t* input, uint8_t alpha, uint8_t colorkey,
                    int width, int height, uint8_t* output) {
        // 8x8 Bayer matrix (values 0–63)
        static const uint8_t bayer[8][8] = {
            {0,32,8,40,2,34,10,42},
            {48,16,56,24,50,18,58,26},
            {12,44,4,36,14,46,6,38},
            {60,28,52,20,62,30,54,22},
            {3,35,11,43,1,33,9,41},
            {51,19,59,27,49,17,57,25},
            {15,47,7,39,13,45,5,37},
            {63,31,55,23,61,29,53,21}
        };

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                int idx = y * width + x;
                uint8_t val = input[idx];
                if (val == colorkey) {
                    output[idx] = colorkey;
                } else {
                    // scale Bayer value to alpha
                    uint8_t threshold = alpha * 64 / 256; // map 0–255 to 0–63
                    uint8_t bval = bayer[y % 8][x % 8];
                    output[idx] = (bval < threshold) ? colorkey : val;
                }
            }
        }
    }
        
}