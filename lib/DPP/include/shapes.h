#ifndef DRAWPP_SHAPES_H
#define DRAWPP_SHAPES_H

#include <SDL2/SDL.h>
#include <stdbool.h>

/**
 * @brief Draws a straight line between two points
 *
 * @param x1 Starting x coordinate
 * @param y1 Starting y coordinate
 * @param x2 Ending x coordinate
 * @param y2 Ending y coordinate
 * @param color Color of the line
 * @param thickness Thickness of the line
 */
void draw_line(int x1, int y1, int x2, int y2, SDL_Color color, int thickness);

/**
 * @brief Draws a rectangle
 *
 * @param x Top-left corner x coordinate
 * @param y Top-left corner y coordinate
 * @param width Width of the rectangle
 * @param height Height of the rectangle
 * @param filled If true, fills the rectangle; if false, draws only the outline
 * @param color Color of the rectangle
 * @param thickness Thickness of the rectangle border (ignored if filled is true)
 */
void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color, int thickness);

/**
 * @brief Draws a circle
 *
 * @param centerX Center x coordinate
 * @param centerY Center y coordinate
 * @param radius Radius of the circle
 * @param filled If true, fills the circle; if false, draws only the outline
 * @param color Color of the circle
 * @param thickness Thickness of the circle border (ignored if filled is true)
 */
void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color, int thickness);

/**
 * @brief Draws a triangle
 *
 * @param x1 First vertex x coordinate
 * @param y1 First vertex y coordinate
 * @param x2 Second vertex x coordinate
 * @param y2 Second vertex y coordinate
 * @param x3 Third vertex x coordinate
 * @param y3 Third vertex y coordinate
 * @param filled If true, fills the triangle; if false, draws only the outline
 * @param color Color of the triangle
 * @param thickness Thickness of the triangle border (ignored if filled is true)
 */
void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color, int thickness);

/**
 * @brief Draws an ellipse
 *
 * @param centerX Center x coordinate
 * @param centerY Center y coordinate
 * @param radiusX Horizontal radius
 * @param radiusY Vertical radius
 * @param filled If true, fills the ellipse; if false, draws only the outline
 * @param color Color of the ellipse
 * @param thickness Thickness of the ellipse border (ignored if filled is true)
 */
void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color, int thickness);

#endif /* DRAWPP_SHAPES_H */
