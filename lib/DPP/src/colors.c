#include "../include/colors.h"

// Custom color creation function
SDL_Color custom_color(Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    SDL_Color color = {
        .r = r,
        .g = g,
        .b = b,
        .a = a
    };
    return color;
}

// Basic Colors
SDL_Color black = {0, 0, 0, 255};
SDL_Color white = {255, 255, 255, 255};
SDL_Color red = {255, 0, 0, 255};
SDL_Color green = {0, 255, 0, 255};
SDL_Color blue = {0, 0, 255, 255};

// Shades of Gray
SDL_Color gray = {128, 128, 128, 255};
SDL_Color light_gray = {192, 192, 192, 255};
SDL_Color dark_gray = {64, 64, 64, 255};

// Warm Colors
SDL_Color orange = {255, 165, 0, 255};
SDL_Color brown = {165, 42, 42, 255};
SDL_Color pink = {255, 192, 203, 255};
SDL_Color coral = {255, 127, 80, 255};
SDL_Color gold = {255, 215, 0, 255};

// Cool Colors
SDL_Color purple = {128, 0, 128, 255};
SDL_Color indigo = {75, 0, 130, 255};
SDL_Color turquoise = {64, 224, 208, 255};
SDL_Color navy = {0, 0, 128, 255};
SDL_Color teal = {0, 128, 128, 255};

// Nature-inspired Colors
SDL_Color forest_green = {34, 139, 34, 255};
SDL_Color sky_blue = {135, 206, 235, 255};
SDL_Color olive = {128, 128, 0, 255};
SDL_Color salmon = {250, 128, 114, 255};
SDL_Color beige = {245, 245, 220, 255};