#include "../include/shapes.h"
#include "../include/drawpp.h"
#include <math.h>

/**
 * @brief Draws a straight line between two points.
 *
 * @param x1 The x-coordinate of the starting point.
 * @param y1 The y-coordinate of the starting point.
 * @param x2 The x-coordinate of the ending point.
 * @param y2 The y-coordinate of the ending point.
 * @param color The color of the line.
 */
void draw_line(int x1, int y1, int x2, int y2, SDL_Color color, int thickness) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    for (int i = -thickness / 2; i <= thickness / 2; i++) {
        SDL_RenderDrawLine(renderer, x1, y1 + i, x2, y2 + i);
    }
}

/**
 * @brief Draws a rectangle at a given position.
 *
 * @param x The x-coordinate of the rectangle's top-left corner.
 * @param y The y-coordinate of the rectangle's top-left corner.
 * @param width The width of the rectangle.
 * @param height The height of the rectangle.
 * @param filled If true, the rectangle is filled; otherwise, only the outline is drawn.
 * @param color The color of the rectangle.
 */
void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color, int thickness) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    SDL_Rect rect = { .x = x, .y = y, .w = width, .h = height };

    if (filled) {
        SDL_RenderFillRect(renderer, &rect);
    } else {
        for (int i = 0; i < thickness; i++) {
            SDL_Rect border = {x - i, y - i, width + 2 * i, height + 2 * i};
            SDL_RenderDrawRect(renderer, &border);
        }
    }
}


/**
 * @brief Draws a circle centered at a given position.
 *
 * @param centerX The x-coordinate of the circle's center.
 * @param centerY The y-coordinate of the circle's center.
 * @param radius The radius of the circle.
 * @param filled If true, the circle is filled; otherwise, only the outline is drawn.
 * @param color The color of the circle.
 */
void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color, int thickness) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        for (int dx = -radius; dx <= radius; dx++) {
            int height = (int)sqrt(radius * radius - dx * dx);
            SDL_RenderDrawLine(renderer, centerX + dx, centerY - height, centerX + dx, centerY + height);
        }
    } else {
        for (int t = 0; t < thickness; t++) {
            for (float angle = 0; angle < 2 * PI; angle += 0.01) {
                int x = centerX + (int)((radius + t) * cos(angle));
                int y = centerY + (int)((radius + t) * sin(angle));
                SDL_RenderDrawPoint(renderer, x, y);
            }
        }
    }
}



/**
 * @brief Draws a triangle connecting three points.
 *
 * @param x1 The x-coordinate of the first vertex.
 * @param y1 The y-coordinate of the first vertex.
 * @param x2 The x-coordinate of the second vertex.
 * @param y2 The y-coordinate of the second vertex.
 * @param x3 The x-coordinate of the third vertex.
 * @param y3 The y-coordinate of the third vertex.
 * @param filled If true, the triangle is filled; otherwise, only the outline is drawn.
 * @param color The color of the triangle.
 */
void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color, int thickness) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    if (filled) {
        int minY = fmin(y1, fmin(y2, y3));
        int maxY = fmax(y1, fmax(y2, y3));
        for (int y = minY; y <= maxY; y++) {
            float intersections[2];
            int intersectCount = 0;
            if ((y1 <= y && y2 > y) || (y2 <= y && y1 > y)) {
                intersections[intersectCount++] = x1 + (float)(y - y1) * (x2 - x1) / (y2 - y1);
            }
            if ((y2 <= y && y3 > y) || (y3 <= y && y2 > y)) {
                intersections[intersectCount++] = x2 + (float)(y - y2) * (x3 - x2) / (y3 - y2);
            }
            if ((y3 <= y && y1 > y) || (y1 <= y && y3 > y)) {
                if (intersectCount < 2) {
                    intersections[intersectCount++] = x3 + (float)(y - y3) * (x1 - x3) / (y1 - y3);
                }
            }
            if (intersectCount >= 2) {
                int x_start = (int)fmin(intersections[0], intersections[1]);
                int x_end = (int)fmax(intersections[0], intersections[1]);
                SDL_RenderDrawLine(renderer, x_start, y, x_end, y);
            }
        }
    } else {
        for (int i = -thickness / 2; i <= thickness / 2; i++) {
            SDL_RenderDrawLine(renderer, x1, y1 + i, x2, y2 + i);
            SDL_RenderDrawLine(renderer, x2, y2 + i, x3, y3 + i);
            SDL_RenderDrawLine(renderer, x3, y3 + i, x1, y1 + i);
        }
    }
}

/**
 * @brief Draws an ellipse centered at a given position.
 *
 * @param centerX The x-coordinate of the ellipse's center.
 * @param centerY The y-coordinate of the ellipse's center.
 * @param radiusX The horizontal radius of the ellipse.
 * @param radiusY The vertical radius of the ellipse.
 * @param filled If true, the ellipse is filled; otherwise, only the outline is drawn.
 * @param color The color of the ellipse.
 */
void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color, int thickness) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        for (int dx = -radiusX; dx <= radiusX; dx++) {
            float h = (float)radiusY * sqrt(1 - (dx * dx) / (float)(radiusX * radiusX));
            SDL_RenderDrawLine(renderer, centerX + dx, centerY - h, centerX + dx, centerY + h);
        }
    } else {
        for (int t = 0; t < thickness; t++) {
            for (float angle = 0; angle < 2 * PI; angle += 0.01) {
                int x = centerX + (int)((radiusX + t) * cos(angle));
                int y = centerY + (int)((radiusY + t) * sin(angle));
                SDL_RenderDrawPoint(renderer, x, y);
            }
        }
    }
}

