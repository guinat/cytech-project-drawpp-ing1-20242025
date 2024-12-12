#ifndef DRAWPP_SHAPES_H
#define DRAWPP_SHAPES_H

#include <SDL2/SDL.h>
#include <stdbool.h>

/**
 * Draws a straight line between two points
 * @param x1 Starting x coordinate
 * @param y1 Starting y coordinate
 * @param x2 Ending x coordinate
 * @param y2 Ending y coordinate
 * @param color Color of the line
 */
void draw_line(int x1, int y1, int x2, int y2, SDL_Color color);

/**
 * Draws a rectangle
 * @param x Top-left corner x coordinate
 * @param y Top-left corner y coordinate
 * @param width Width of the rectangle
 * @param height Height of the rectangle
 * @param filled If true, fills the rectangle; if false, draws only the outline
 * @param color Color of the rectangle
 */
void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color);

/**
 * Draws a circle
 * @param centerX Center x coordinate
 * @param centerY Center y coordinate
 * @param radius Radius of the circle
 * @param filled If true, fills the circle; if false, draws only the outline
 * @param color Color of the circle
 */
void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color);

/**
 * Draws a triangle
 * @param x1 First vertex x coordinate
 * @param y1 First vertex y coordinate
 * @param x2 Second vertex x coordinate
 * @param y2 Second vertex y coordinate
 * @param x3 Third vertex x coordinate
 * @param y3 Third vertex y coordinate
 * @param filled If true, fills the triangle; if false, draws only the outline
 * @param color Color of the triangle
 */
void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color);

/**
 * Draws an ellipse
 * @param centerX Center x coordinate
 * @param centerY Center y coordinate
 * @param radiusX Horizontal radius
 * @param radiusY Vertical radius
 * @param filled If true, fills the ellipse; if false, draws only the outline
 * @param color Color of the ellipse
 */
void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color);

#endif /* DRAWPP_SHAPES_H */