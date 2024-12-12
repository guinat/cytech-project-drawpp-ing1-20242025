#ifndef DRAWPP_COLORS_H
#define DRAWPP_COLORS_H

#include <SDL2/SDL.h>

/**
 * Creates a custom color
 * @param r Red component (0-255)
 * @param g Green component (0-255)
 * @param b Blue component (0-255)
 * @param a Alpha component (0-255, where 255 is fully opaque)
 * @return SDL_Color structure containing the specified color
 */
SDL_Color custom_color(Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Basic Colors
extern SDL_Color black;  // RGB(0, 0, 0)
extern SDL_Color white;  // RGB(255, 255, 255)
extern SDL_Color red;    // RGB(255, 0, 0)
extern SDL_Color green;  // RGB(0, 255, 0)
extern SDL_Color blue;   // RGB(0, 0, 255)

// Shades of Gray
extern SDL_Color gray;       // RGB(128, 128, 128)
extern SDL_Color light_gray; // RGB(192, 192, 192)
extern SDL_Color dark_gray;  // RGB(64, 64, 64)

// Warm Colors
extern SDL_Color orange;  // RGB(255, 165, 0)
extern SDL_Color brown;   // RGB(165, 42, 42)
extern SDL_Color pink;    // RGB(255, 192, 203)
extern SDL_Color coral;   // RGB(255, 127, 80)
extern SDL_Color gold;    // RGB(255, 215, 0)

// Cool Colors
extern SDL_Color purple;    // RGB(128, 0, 128)
extern SDL_Color indigo;    // RGB(75, 0, 130)
extern SDL_Color turquoise; // RGB(64, 224, 208)
extern SDL_Color navy;      // RGB(0, 0, 128)
extern SDL_Color teal;      // RGB(0, 128, 128)

// Nature-inspired Colors
extern SDL_Color forest_green; // RGB(34, 139, 34)
extern SDL_Color sky_blue;     // RGB(135, 206, 235)
extern SDL_Color olive;        // RGB(128, 128, 0)
extern SDL_Color salmon;       // RGB(250, 128, 114)
extern SDL_Color beige;        // RGB(245, 245, 220)

#endif /* DRAWPP_COLORS_H */