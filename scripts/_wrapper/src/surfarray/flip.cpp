#include <cstdint>
#include <algorithm>
#include <utility>


extern "C" {

    void flip(
        uint8_t* array,
        int width,
        int height,
        bool flip_x,
        bool flip_y
    ) {
        // Nothing to do
        if (!flip_x && !flip_y)
            return;


        // ---------------- Flip X ----------------
        //
        // [0 1 2 3 4]
        //       ↓
        // [4 3 2 1 0]

        if (flip_y) {

            const int half_width = width / 2;

            for (int y = 0; y < height; ++y) {

                uint8_t* row =
                    array + y * width;

                for (int x = 0; x < half_width; ++x) {

                    const int opposite =
                        width - 1 - x;

                    std::swap(
                        row[x],
                        row[opposite]
                    );
                }
            }
        }


        // ---------------- Flip Y ----------------
        //
        // [row 0]
        // [row 1]
        // [row 2]
        //
        //       ↓
        //
        // [row 2]
        // [row 1]
        // [row 0]

        if (flip_x) {

            const int row_size = width;
            const int half_height = height / 2;

            for (int y = 0; y < half_height; ++y) {

                uint8_t* row_a =
                    array + y * row_size;

                uint8_t* row_b =
                    array + (height - 1 - y) * row_size;

                for (int x = 0; x < width; ++x) {

                    std::swap(
                        row_a[x],
                        row_b[x]
                    );
                }
            }
        }
    }

}