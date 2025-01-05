#include "../include/cursor.h"
#include "../include/drawpp.h"
#include "../include/shapes.h"
#include "../include/colors.h"
#include <math.h>
#include <stdio.h>

// Global variables
SDL_Window* window = NULL; ///< The SDL window used for rendering.
SDL_Renderer* renderer = NULL; ///< The SDL renderer used for drawing.
Cursor cursors[MAX_CURSORS]; ///< Array of cursors available in the application.
int active_cursors = 0; ///< Number of currently active cursors.

/**
 * @brief Creates a new cursor at the specified position.
 *
 * @param x The initial x-coordinate of the cursor.
 * @param y The initial y-coordinate of the cursor.
 * @return A pointer to the newly created cursor, or NULL if the maximum number of cursors is reached.
 */
Cursor* create_cursor(double x, double y) {
    if (active_cursors >= MAX_CURSORS) {
        printf("Error: Maximum number of cursors reached\n");
        return NULL;
    }

    int index = 0;
    while (index < MAX_CURSORS && cursors[index].active) {
        index++;
    }

    cursors[index] = (Cursor){
        .x = x,
        .y = y,
        .angle = 0.0,
        .thickness = 1,
        .color = blue, ///< Default color
        .visible = true,
        .active = true
    };

    active_cursors++;
    return &cursors[index];
}

/**
 * @brief Moves the cursor forward by a specified distance in its current direction.
 *
 * @param cursor A pointer to the cursor to move.
 * @param distance The distance to move the cursor.
 */
void move_cursor(Cursor* cursor, double distance) {
    if (!cursor || !cursor->active) return;

    double radians = cursor->angle * PI / 180.0;
    cursor->x += distance * cos(radians);
    cursor->y += distance * sin(radians);
}

/**
 * @brief Rotates the cursor by a specified angle.
 *
 * @param cursor A pointer to the cursor to rotate.
 * @param angle The angle to rotate the cursor, in degrees.
 */
void rotate_cursor(Cursor* cursor, double angle) {
    if (!cursor || !cursor->active) return;

    cursor->angle += angle;

    while (cursor->angle >= 360.0) {
        cursor->angle -= 360.0;
    }
    while (cursor->angle < 0.0) {
        cursor->angle += 360.0;
    }
}

/**
 * @brief Sets the color of the cursor.
 *
 * @param cursor A pointer to the cursor to modify.
 * @param color The new color to set for the cursor.
 */
void set_cursor_color(Cursor* cursor, SDL_Color color) {
    if (!cursor || !cursor->active) return;
    cursor->color = color;
}

/**
 * @brief Sets the visibility of the cursor.
 *
 * @param cursor A pointer to the cursor to modify.
 * @param visible A boolean indicating whether the cursor should be visible.
 */
void set_cursor_visibility(Cursor* cursor, bool visible) {
    if (!cursor || !cursor->active) return;

    cursor->visible = visible;

    if (visible) {
        int cursorX = (int)cursor->x;
        int cursorY = (int)cursor->y;

        SDL_Color cursorColor = {0, 0, 0, 255}; // black
        draw_rectangle(cursorX - 5, cursorY - 5, 10, 10, true, cursorColor, 1);
    } else {
        clear_area((int)cursor->x - 5, (int)cursor->y - 5, 10, 10);
    }
}





/**
 * @brief Sets the thickness of the cursor's drawing.
 *
 * @param cursor A pointer to the cursor to modify.
 * @param thickness The new thickness value. Must be greater than 0.
 */
void set_cursor_thickness(Cursor* cursor, int thickness) {
    if (!cursor || !cursor->active) {
        printf("Error: Cursor is not valid or active\n");
        return;
    }

    if (thickness <= 0) {
        printf("Error: Thickness must be greater than 0\n");
        return;
    }

    cursor->thickness = thickness;
    printf("Cursor thickness set to %d\n", thickness);
}

/**
 * @brief Clears a rectangular area on the rendering surface.
 *
 * @param x The x-coordinate of the top-left corner of the area to clear.
 * @param y The y-coordinate of the top-left corner of the area to clear.
 * @param width The width of the area to clear.
 * @param height The height of the area to clear.
 */
void clear_area(int x, int y, int width, int height) {
    if (!renderer) {
        printf("Error: Renderer is not initialized\n");
        return;
    }

    Uint8 r, g, b, a;
    SDL_GetRenderDrawColor(renderer, &r, &g, &b, &a);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_Rect clearRect = {x, y, width, height};
    SDL_RenderFillRect(renderer, &clearRect);
    SDL_SetRenderDrawColor(renderer, r, g, b, a);
}

/**
 * @brief Draws a straight line from the cursor's position in its current direction.
 *
 * @param cursor A pointer to the cursor to use for drawing.
 * @param length The length of the line to draw.
 */
void cursor_draw_line(Cursor* cursor, double length) {
    if (!cursor || !cursor->active) return;

    double radians = cursor->angle * PI / 180.0;
    int endX = (int)(cursor->x + length * cos(radians));
    int endY = (int)(cursor->y + length * sin(radians));

    draw_line((int)cursor->x, (int)cursor->y, endX, endY, cursor->color, cursor->thickness);
}

/**
 * @brief Draws a rectangle centered at the cursor's position.
 *
 * @param cursor A pointer to the cursor to use for drawing.
 * @param width The width of the rectangle.
 * @param height The height of the rectangle.
 * @param filled A boolean indicating whether the rectangle should be filled.
 */
void cursor_draw_rectangle(Cursor* cursor, double width, double height, bool filled) {
    if (!cursor || !cursor->active) return;
    draw_rectangle((int)cursor->x, (int)cursor->y, (int)width, (int)height, filled, cursor->color, cursor->thickness);
}
/**
 * @brief Draws a circle centered at the cursor's position.
 *
 * @param cursor A pointer to the cursor to use for drawing.
 * @param radius The radius of the circle.
 * @param filled A boolean indicating whether the circle should be filled.
 */
void cursor_draw_circle(Cursor* cursor, double radius, bool filled) {
    if (!cursor || !cursor->active) return;
    draw_circle((int)cursor->x, (int)cursor->y, (int)radius, filled, cursor->color, cursor->thickness);
}


/**
 * @brief Draws a triangle based on the cursor's position and direction.
 *
 * @param cursor A pointer to the cursor to use for drawing.
 * @param base The base length of the triangle.
 * @param height The height of the triangle.
 * @param filled A boolean indicating whether the triangle should be filled.
 */
void cursor_draw_triangle(Cursor* cursor, double base, double height, bool filled) {
    if (!cursor || !cursor->active) return;

    double radians = cursor->angle * PI / 180.0;

    int x1 = (int)cursor->x;
    int y1 = (int)cursor->y;

    int x2 = (int)(x1 + base * cos(radians));
    int y2 = (int)(y1 + base * sin(radians));

    double perpRadians = radians + PI / 2.0;
    int x3 = (int)(x1 + height * cos(perpRadians));
    int y3 = (int)(y1 + height * sin(perpRadians));

    draw_triangle(x1, y1, x2, y2, x3, y3, filled, cursor->color, cursor->thickness);
}

/**
 * @brief Draws an ellipse centered at the cursor's position.
 *
 * @param cursor A pointer to the cursor to use for drawing.
 * @param radiusX The horizontal radius of the ellipse.
 * @param radiusY The vertical radius of the ellipse.
 * @param filled A boolean indicating whether the ellipse should be filled.
 */
void cursor_draw_ellipse(Cursor* cursor, double radiusX, double radiusY, bool filled) {
    if (!cursor || !cursor->active) return;
    draw_ellipse((int)cursor->x, (int)cursor->y, (int)radiusX, (int)radiusY, filled, cursor->color, cursor->thickness);
}