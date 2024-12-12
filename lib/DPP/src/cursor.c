#include "../include/cursor.h"
#include "../include/drawpp.h"
#include "../include/shapes.h"
#include "../include/colors.h"
#include <math.h>
#include <stdio.h>

// Global variables
SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;
Cursor cursors[MAX_CURSORS];
int active_cursors = 0;

// Cursor creation
Cursor* create_cursor(double x, double y) {
    if (active_cursors >= MAX_CURSORS) {
        printf("Error: Maximum number of cursors reached\n");
        return NULL;
    }

    // Find first available slot
    int index = 0;
    while (index < MAX_CURSORS && cursors[index].active) {
        index++;
    }

    // Initialize the cursor
    cursors[index] = (Cursor){
        .x = x,
        .y = y,
        .angle = 0.0,
        .thickness = 1,
        .color = black,  // Default color is black
        .visible = true,
        .active = true
    };

    active_cursors++;
    return &cursors[index];
}

// Cursor movement
void move_cursor(Cursor* cursor, double distance) {
    if (!cursor || !cursor->active || !cursor->visible) return;

    // Convert angle to radians for trigonometric calculations
    double radians = cursor->angle * PI / 180.0;

    // Update position using trigonometry
    cursor->x += distance * cos(radians);
    cursor->y += distance * sin(radians);
}

// Cursor rotation
void rotate_cursor(Cursor* cursor, double angle) {
    if (!cursor || !cursor->active) return;

    cursor->angle += angle;

    // Normalize angle to [0, 360)
    while (cursor->angle >= 360.0) {
        cursor->angle -= 360.0;
    }
    while (cursor->angle < 0.0) {
        cursor->angle += 360.0;
    }
}

// Cursor color setting
void set_cursor_color(Cursor* cursor, SDL_Color color) {
    if (!cursor || !cursor->active) return;
    cursor->color = color;
}

// Cursor visibility setting
void set_cursor_visibility(Cursor* cursor, bool visible) {
    if (!cursor || !cursor->active) return;
    cursor->visible = visible;
}

// Drawing functions
void cursor_draw_line(Cursor* cursor, double length) {
    if (!cursor || !cursor->active || !cursor->visible) return;

    // Calculate end point using trigonometry
    double radians = cursor->angle * PI / 180.0;
    double endX = cursor->x + length * cos(radians);
    double endY = cursor->y + length * sin(radians);

    // Draw the line
    draw_line(cursor->x, cursor->y, endX, endY, cursor->color);
}

void cursor_draw_rectangle(Cursor* cursor, double width, double height, bool filled) {
    if (!cursor || !cursor->active || !cursor->visible) return;
    draw_rectangle(cursor->x, cursor->y, width, height, filled, cursor->color);
}

void cursor_draw_circle(Cursor* cursor, double radius, bool filled) {
    if (!cursor || !cursor->active || !cursor->visible) return;
    draw_circle(cursor->x, cursor->y, radius, filled, cursor->color);
}

void cursor_draw_triangle(Cursor* cursor, double base, double height, bool filled) {
    if (!cursor || !cursor->active || !cursor->visible) return;

    // Calculate triangle vertices based on cursor position and angle
    double radians = cursor->angle * PI / 180.0;

    double x1 = cursor->x;
    double y1 = cursor->y;

    // Second point: base length away at current angle
    double x2 = x1 + base * cos(radians);
    double y2 = y1 + base * sin(radians);

    // Third point: perpendicular to angle, height away
    double perpRadians = radians + PI/2.0;  // Add 90 degrees
    double x3 = x1 + height * cos(perpRadians);
    double y3 = y1 + height * sin(perpRadians);

    draw_triangle(x1, y1, x2, y2, x3, y3, filled, cursor->color);
}

void cursor_draw_ellipse(Cursor* cursor, double radiusX, double radiusY, bool filled) {
    if (!cursor || !cursor->active || !cursor->visible) return;
    draw_ellipse(cursor->x, cursor->y, radiusX, radiusY, filled, cursor->color);
}