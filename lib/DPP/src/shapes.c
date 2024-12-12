#include "../include/shapes.h"
#include "../include/drawpp.h"
#include <math.h>

// External reference to the SDL renderer
extern SDL_Renderer* renderer;

void draw_line(int x1, int y1, int x2, int y2, SDL_Color color) {
    // Set the render color
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    // Draw the line
    SDL_RenderDrawLine(renderer, x1, y1, x2, y2);
}

void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color) {
    // Set the render color
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    // Create the rectangle
    SDL_Rect rect = {
        .x = x,
        .y = y,
        .w = width,
        .h = height
    };

    // Draw filled or outlined rectangle
    if (filled) {
        SDL_RenderFillRect(renderer, &rect);
    } else {
        SDL_RenderDrawRect(renderer, &rect);
    }
}

void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color) {
    // Set the render color
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        // Draw filled circle using scanline
        for (int dx = -radius; dx <= radius; dx++) {
            int height = (int)sqrt(radius * radius - dx * dx);

            // Draw vertical line for each x position
            SDL_RenderDrawLine(
                renderer,
                centerX + dx,    // x position
                centerY - height, // top y
                centerX + dx,    // x position
                centerY + height  // bottom y
            );
        }
    } else {
        // Draw circle outline using parametric equation
        for (float angle = 0; angle < 2 * PI; angle += 0.01) {
            int x = centerX + (int)(radius * cos(angle));
            int y = centerY + (int)(radius * sin(angle));
            SDL_RenderDrawPoint(renderer, x, y);
        }
    }
}

void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color) {
    // Set the render color
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        // Find bounding box
        int minY = fmin(y1, fmin(y2, y3));
        int maxY = fmax(y1, fmax(y2, y3));

        // Scan each line
        for (int y = minY; y <= maxY; y++) {
            float intersections[2];
            int intersectCount = 0;

            // Check intersection with all three sides
            // Side 1: (x1,y1) to (x2,y2)
            if ((y1 <= y && y2 > y) || (y2 <= y && y1 > y)) {
                intersections[intersectCount++] = x1 + (float)(y - y1) * (x2 - x1) / (y2 - y1);
            }

            // Side 2: (x2,y2) to (x3,y3)
            if ((y2 <= y && y3 > y) || (y3 <= y && y2 > y)) {
                intersections[intersectCount++] = x2 + (float)(y - y2) * (x3 - x2) / (y3 - y2);
            }

            // Side 3: (x3,y3) to (x1,y1)
            if ((y3 <= y && y1 > y) || (y1 <= y && y3 > y)) {
                if (intersectCount < 2) {
                    intersections[intersectCount++] = x3 + (float)(y - y3) * (x1 - x3) / (y1 - y3);
                }
            }

            // If we found intersections, draw the scanline
            if (intersectCount >= 2) {
                int x_start = (int)fmin(intersections[0], intersections[1]);
                int x_end = (int)fmax(intersections[0], intersections[1]);
                SDL_RenderDrawLine(renderer, x_start, y, x_end, y);
            }
        }
    } else {
        // Draw the outline
        SDL_RenderDrawLine(renderer, x1, y1, x2, y2);
        SDL_RenderDrawLine(renderer, x2, y2, x3, y3);
        SDL_RenderDrawLine(renderer, x3, y3, x1, y1);
    }
}

void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color) {
    // Set the render color
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        // Draw filled ellipse using vertical scanlines
        for (int dx = -radiusX; dx <= radiusX; dx++) {
            float h = (float)radiusY * sqrt(1 - (dx * dx) / (float)(radiusX * radiusX));
            SDL_RenderDrawLine(
                renderer,
                centerX + dx,    // x position
                centerY - h,     // top y
                centerX + dx,    // x position
                centerY + h      // bottom y
            );
        }
    } else {
        // Draw ellipse outline using parametric equations
        for (float angle = 0; angle < 2 * PI; angle += 0.01) {
            int x = centerX + (int)(radiusX * cos(angle));
            int y = centerY + (int)(radiusY * sin(angle));
            SDL_RenderDrawPoint(renderer, x, y);
        }
    }
}