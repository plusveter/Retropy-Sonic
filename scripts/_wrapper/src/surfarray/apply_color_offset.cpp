#include <cstdint>
#include <algorithm>


extern "C" {

    void apply_color_offset(
        uint8_t* surf,
        int surf_x,
        int surf_y,

        uint8_t* mask,
        int mask_x,
        int mask_y,

        int surf_width,
        int surf_height,

        int mask_width,
        int mask_height
    ) {
        // Calculate mask position relative to the surface
        const int dx = mask_x - surf_x;
        const int dy = mask_y - surf_y;


        // Calculate overlapping region

        const int y0 = std::max(0, dy);
        const int x0 = std::max(0, dx);

        const int y1 = std::min(
            surf_height,
            dy + mask_height
        );

        const int x1 = std::min(
            surf_width,
            dx + mask_width
        );


        // No overlap
        if (x0 >= x1 || y0 >= y1) {
            return;
        }


        // Corresponding starting position inside mask

        const int mask_y0 = y0 - dy;
        const int mask_x0 = x0 - dx;


        // Process overlapping region

        for (int x = x0; x < x1; ++x) {

            const int mask_x = mask_x0 + (x - x0);

            for (int y = y0; y < y1; ++y) {

                const int mask_y = mask_y0 + (y - y0);

                // X first, then Y
                const int mask_idx =
                    mask_x * mask_height + mask_y;

                const int surf_idx =
                    x * surf_height + y;

                if (mask[mask_idx] > 0) {

                    if (surf[surf_idx] != 0) {
                        surf[surf_idx] =
                            static_cast<uint8_t>(
                                (static_cast<int>(surf[surf_idx]) + mask[mask_idx]) % 256
                            );
                    }
                }
            }
        }
    }

}