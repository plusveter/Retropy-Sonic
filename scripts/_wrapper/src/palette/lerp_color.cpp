#include <cstdint>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <emmintrin.h>
#include <unordered_set>
// OpenMP header



extern "C" {

    void lerp_color(const uint8_t* start, const uint8_t* final, double percentage, uint8_t* result) {
        if (percentage < 0.0) percentage = 0.0;
        if (percentage > 1.0) percentage = 1.0;

        for (int i = 0; i < 3; ++i) {
            double s = static_cast<double>(start[i]);
            double f = static_cast<double>(final[i]);
            double val = s + (f - s) * percentage;
            result[i] = static_cast<uint8_t>(std::clamp(std::round(val), 0.0, 255.0));
        }
    }
    
}