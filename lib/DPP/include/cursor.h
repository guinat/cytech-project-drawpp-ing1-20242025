#ifndef DRAWPP_CURSOR_H
#define DRAWPP_CURSOR_H

#include <SDL2/SDL.h>
#include <stdbool.h>
#include <math.h>

// Cursor structure definition
typedef struct {
    double x;            // X position
    double y;            // Y position
    double angle;        // Angle of direction in degrees
    int thickness;       // Line thickness
    SDL_Color color;     // Color of the cursor
    bool visible;        // Whether the cursor is visible
    bool active;         // Whether the cursor is active
} Cursor;

// Cursor management functions
/**
 * @brief Creates a new cursor at the specified position
 *
 * @param x The initial x coordinate
 * @param y The initial y coordinate
 * @return Pointer to the created cursor, or NULL if no cursors available
 */
Cursor* create_cursor(double x, double y);

/**
 * @brief Moves a cursor in its current direction
 *
 * @param cursor The cursor to move
 * @param distance The distance to move
 */
void move_cursor(Cursor* cursor, double distance);

/**
 * @brief Rotates a cursor by a specified angle
 *
 * @param cursor The cursor to rotate
 * @param angle The angle to rotate by (in degrees)
 */
void rotate_cursor(Cursor* cursor, double angle);

/**
 * @brief Sets the color of a cursor
 *
 * @param cursor The cursor to modify
 * @param color The new color
 */
void set_cursor_color(Cursor* cursor, SDL_Color color);

/**
 * @brief Sets the visibility of a cursor
 *
 * @param cursor The cursor to modify
 * @param visible The visibility state
 */
void set_cursor_visibility(Cursor* cursor, bool visible);

/**
 * @brief Sets the thickness of a cursor's drawing
 *
 * @param cursor The cursor to modify
 * @param thickness The new thickness value
 */
void set_cursor_thickness(Cursor* cursor, int thickness);

/**
 * @brief Clears a rectangular area on the screen
 *
 * @param x The x-coordinate of the top-left corner
 * @param y The y-coordinate of the top-left corner
 * @param width The width of the area
 * @param height The height of the area
 */
void clear_area(int x, int y, int width, int height);

// Cursor drawing functions
/**
 * @brief Draws a line from the cursor's position
 *
 * @param cursor The cursor to draw with
 * @param length The length of the line
 */
void cursor_draw_line(Cursor* cursor, double length);

/**
 * @brief Draws a rectangle from the cursor's position
 *
 * @param cursor The cursor to draw with
 * @param width The width of the rectangle
 * @param height The height of the rectangle
 * @param filled Whether to fill the rectangle
 */
void cursor_draw_rectangle(Cursor* cursor, double width, double height, bool filled);

/**
 * @brief Draws a circle at the cursor's position
 *
 * @param cursor The cursor to draw with
 * @param radius The radius of the circle
 * @param filled Whether to fill the circle
 */
void cursor_draw_circle(Cursor* cursor, double radius, bool filled);

/**
 * @brief Draws a triangle from the cursor's position
 *
 * @param cursor The cursor to draw with
 * @param base The base length of the triangle
 * @param height The height of the triangle
 * @param filled Whether to fill the triangle
 */
void cursor_draw_triangle(Cursor* cursor, double base, double height, bool filled);

/**
 * @brief Draws an ellipse at the cursor's position
 *
 * @param cursor The cursor to draw with
 * @param radiusX The horizontal radius
 * @param radiusY The vertical radius
 * @param filled Whether to fill the ellipse
 */
void cursor_draw_ellipse(Cursor* cursor, double radiusX, double radiusY, bool filled);

/**
 * @brief Prints the current position of the cursor
 *
 * @param cursor The cursor whose position is to be printed
 */
void print_cursor_position(Cursor* cursor);

#endif /* DRAWPP_CURSOR_H */
