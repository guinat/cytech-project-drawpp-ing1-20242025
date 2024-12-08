#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdio.h>
#include <math.h>

// Constants for the window size and mathematical calculations
#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600
#define PI 3.14159265358979323846
#define MAX_CURSORS 10 // Maximum number of cursors supported

// Structure to define a cursor
typedef struct {
    double x;            // X position
    double y;            // Y position
    double angle;        // Angle of direction in degrees
    int thickness;       // Line thickness
    SDL_Color color;     // Color of the cursor
    bool visible;        // Whether the cursor is visible
    bool active;         // Whether the cursor is active
} Cursor;

// Predefined color
SDL_Color black = {0, 0, 0, 255};
SDL_Color white = {255, 255, 255, 255};
SDL_Color red = {255, 0, 0, 255};
SDL_Color green = {0, 255, 0, 255};
SDL_Color blue = {0, 0, 255, 255};

// Shades of gray
SDL_Color gray = {128, 128, 128, 255};
SDL_Color light_gray = {192, 192, 192, 255};
SDL_Color dark_gray = {64, 64, 64, 255};

// Warm colors
SDL_Color orange = {255, 165, 0, 255};
SDL_Color brown = {165, 42, 42, 255};
SDL_Color pink = {255, 192, 203, 255};
SDL_Color coral = {255, 127, 80, 255};
SDL_Color gold = {255, 215, 0, 255};

// Cool colors
SDL_Color purple = {128, 0, 128, 255};
SDL_Color indigo = {75, 0, 130, 255};
SDL_Color turquoise = {64, 224, 208, 255};
SDL_Color navy = {0, 0, 128, 255};
SDL_Color teal = {0, 128, 128, 255};

// Nature-inspired colors
SDL_Color forest_green = {34, 139, 34, 255};
SDL_Color sky_blue = {135, 206, 235, 255};
SDL_Color olive = {128, 128, 0, 255};
SDL_Color salmon = {250, 128, 114, 255};
SDL_Color beige = {245, 245, 220, 255};

// Global variables for SDL
SDL_Window* window = NULL;     // Pointer to the SDL window
SDL_Renderer* renderer = NULL; // Pointer to the SDL renderer
Cursor cursors[MAX_CURSORS];   // Array to hold cursors
int active_cursors = 0;        // Counter for the number of active cursors


/////////////////////////////////////////////////////////////////////////////
//                  SDL
/////////////////////////////////////////////////////////////////////////////


// Function to create a custom SDL_Color
SDL_Color custom_color(Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    SDL_Color color = {r, g, b, a};
    return color;
}

// Function to initialize SDL and set up the window and renderer
bool initialize_SDL(void) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return false;
    }
    // Create an SDL window
    window = SDL_CreateWindow("draw++",
                            SDL_WINDOWPOS_CENTERED,
                            SDL_WINDOWPOS_CENTERED,
                            WINDOW_WIDTH,
                            WINDOW_HEIGHT,
                            SDL_WINDOW_SHOWN);

    if (window == NULL) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return false;
    }

    // Create a renderer for the window
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        return false;
    }

    // Initialize the array of cursors
    for (int i = 0; i < MAX_CURSORS; i++) {
        cursors[i].active = false;
    }
    active_cursors = 0;

    return true;
}

// Function to clean up SDL resources
void cleanup_SDL(void) {
    // Deactivate all cursors
    for (int i = 0; i < MAX_CURSORS; i++) {
        if (cursors[i].active) {
            cursors[i].active = false;
            active_cursors--;
        }
    }

    if (renderer) {
        SDL_DestroyRenderer(renderer);
    }
    if (window) {
        SDL_DestroyWindow(window);
    }
    SDL_Quit();
}



/////////////////////////////////////////////////////////////////////////////
//                  Shape
/////////////////////////////////////////////////////////////////////////////

// Function to draw a rectangle on the screen
// Parameters:
//   x, y: The top-left corner coordinates of the rectangle.
//   width, height: The dimensions of the rectangle (width and height).
//   filled: A boolean indicating whether the rectangle should be filled or outlined.
//   color: An SDL_Color structure specifying the color of the rectangle.
void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color) {
    // Set the current rendering color to the specified color
    // SDL_SetRenderDrawColor sets the color used for subsequent drawing operations.
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    // Define the rectangle's dimensions and position as an SDL_Rect structure
    // x, y define the top-left corner, while width and height specify its size.
    SDL_Rect rect = {x, y, width, height};

    // Check if the rectangle should be filled or outlined
    if (filled) {
        // If filled is true, render a filled rectangle
        // SDL_RenderFillRect fills the given rectangle with the current drawing color.
        SDL_RenderFillRect(renderer, &rect);
    } else {
        // If filled is false, render an outlined rectangle
        // SDL_RenderDrawRect draws only the border of the rectangle.
        SDL_RenderDrawRect(renderer, &rect);
    }
}


// Function to draw a circle on the screen
// Parameters:
//   centerX, centerY: The coordinates of the circle's center.
//   radius: The radius of the circle.
//   filled: A boolean indicating whether the circle should be filled or just an outline.
//   color: An SDL_Color structure specifying the color of the circle.
void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color) {
    // Set the rendering color to the specified color
    // SDL_SetRenderDrawColor sets the color used for all subsequent drawing operations.
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    // Check if the circle should be filled or just an outline
    if (filled) {
        // If filled is true, fill the circle by drawing vertical lines for each x-coordinate
        // Iterate over all x-coordinates within the circle's radius
        for (int x = -radius; x <= radius; x++) {
            // Use the circle equation (x^2 + y^2 = r^2) to calculate the corresponding height
            // at each x-coordinate. This defines the range of y-values for the circle.
            int height = (int)sqrt(radius * radius - x * x);

            // Draw a vertical line for the current x-coordinate that spans the circle's height
            // SDL_RenderDrawLine is used to fill the circle by connecting top and bottom points.
            SDL_RenderDrawLine(renderer,
                               centerX + x, centerY - height, // Top point
                               centerX + x, centerY + height  // Bottom point
            );
        }
    } else {
        // If filled is false, draw only the circle's outline
        // Use trigonometric functions (cos and sin) to calculate points along the circumference.
        // Iterate over angles from 0 to 2π in small steps for a smooth circle.
        for (float angle = 0; angle < 2 * PI; angle += 0.01) {
            // Calculate the x and y coordinates of a point on the circle's perimeter
            int x = centerX + radius * cos(angle);
            int y = centerY + radius * sin(angle);

            // Draw a single point at the calculated position
            // SDL_RenderDrawPoint places a pixel at the specified coordinates.
            SDL_RenderDrawPoint(renderer, x, y);
        }
    }
}


// Function to draw a straight line on the screen
// Parameters:
//   x1, y1: The starting coordinates of the line.
//   x2, y2: The ending coordinates of the line.
//   color: An SDL_Color structure specifying the color of the line.
void draw_line(int x1, int y1, int x2, int y2, SDL_Color color) {
    // Set the rendering color to the specified color
    // SDL_SetRenderDrawColor sets the color used for all subsequent drawing operations.
    // The color is defined using RGBA (Red, Green, Blue, Alpha) values from the 'color' parameter.
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    // Draw a straight line between the specified start and end points
    // SDL_RenderDrawLine draws a line connecting (x1, y1) and (x2, y2) using the current rendering color.
    SDL_RenderDrawLine(renderer, x1, y1, x2, y2);
}


// Function to draw a triangle on the screen
// Parameters:
//   x1, y1: Coordinates of the first vertex of the triangle.
//   x2, y2: Coordinates of the second vertex of the triangle.
//   x3, y3: Coordinates of the third vertex of the triangle.
//   filled: A boolean indicating whether the triangle should be filled or just outlined.
//   color: An SDL_Color structure specifying the color of the triangle.
void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color) {
    // Set the rendering color to the specified color
    // SDL_SetRenderDrawColor sets the color used for all subsequent drawing operations.
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        // If the triangle should be filled, compute the fill using scanlines

        // Find the minimum and maximum Y values among the three vertices
        int minY = fmin(y1, fmin(y2, y3));
        int maxY = fmax(y1, fmax(y2, y3));

        // Iterate through each scanline (horizontal line) between minY and maxY
        for (int y = minY; y <= maxY; y++) {
            // Array to store intersections of the triangle's edges with the current scanline
            float intersections[2];
            int intersectCount = 0;

            // Check for intersection with the edge between the first and second vertices
            if ((y1 <= y && y2 > y) || (y2 <= y && y1 > y)) {
                intersections[intersectCount++] = x1 + (float)(y - y1) * (x2 - x1) / (y2 - y1);
            }

            // Check for intersection with the edge between the second and third vertices
            if ((y2 <= y && y3 > y) || (y3 <= y && y2 > y)) {
                intersections[intersectCount++] = x2 + (float)(y - y2) * (x3 - x2) / (y3 - y2);
            }

            // Check for intersection with the edge between the third and first vertices
            if ((y3 <= y && y1 > y) || (y1 <= y && y3 > y)) {
                if (intersectCount < 2) { // Ensure only two intersections are recorded
                    intersections[intersectCount++] = x3 + (float)(y - y3) * (x1 - x3) / (y1 - y3);
                }
            }

            // If there are two intersections on this scanline, draw a horizontal line
            if (intersectCount >= 2) {
                // Find the start and end X-coordinates of the scanline
                int x_start = (int)fmin(intersections[0], intersections[1]);
                int x_end = (int)fmax(intersections[0], intersections[1]);

                // Draw the horizontal line on the current scanline
                SDL_RenderDrawLine(renderer, x_start, y, x_end, y);
            }
        }
    } else {
        // If the triangle is not filled, draw its outline
        // Use SDL_RenderDrawLine to connect each pair of vertices
        SDL_RenderDrawLine(renderer, x1, y1, x2, y2); // Edge from vertex 1 to vertex 2
        SDL_RenderDrawLine(renderer, x2, y2, x3, y3); // Edge from vertex 2 to vertex 3
        SDL_RenderDrawLine(renderer, x3, y3, x1, y1); // Edge from vertex 3 to vertex 1
    }
}


// Function to draw an ellipse on the screen
// Parameters:
//   centerX, centerY: The coordinates of the center of the ellipse.
//   radiusX: The horizontal radius of the ellipse.
//   radiusY: The vertical radius of the ellipse.
//   filled: A boolean indicating whether the ellipse should be filled or just an outline.
//   color: An SDL_Color structure specifying the color of the ellipse.
void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color) {
    // Set the rendering color to the specified color
    // SDL_SetRenderDrawColor sets the color used for all subsequent drawing operations.
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);

    if (filled) {
        // If the ellipse should be filled, use vertical lines for filling
        // Iterate over all x-coordinates within the horizontal radius of the ellipse
        for (int x = -radiusX; x <= radiusX; x++) {
            // Compute the vertical distance (height) of the ellipse at the current x-coordinate
            // using the ellipse equation: x^2 / radiusX^2 + y^2 / radiusY^2 = 1
            float h = (float)radiusY * sqrt(1 - (x * x) / (float)(radiusX * radiusX));

            // Draw a vertical line at the current x-coordinate that spans the ellipse's height
            // SDL_RenderDrawLine connects the top and bottom points of the ellipse.
            SDL_RenderDrawLine(renderer,
                               centerX + x, centerY - h, // Top point
                               centerX + x, centerY + h  // Bottom point
            );
        }
    } else {
        // If the ellipse is not filled, draw only its outline
        // Use trigonometric functions (cos and sin) to calculate points along the perimeter.
        // Iterate over angles from 0 to 2π in small steps for smooth rendering.
        for (float angle = 0; angle < 2 * PI; angle += 0.01) {
            // Calculate the x and y coordinates of a point on the ellipse
            // Use the parametric equations of an ellipse:
            // x = centerX + radiusX * cos(angle)
            // y = centerY + radiusY * sin(angle)
            int x = centerX + radiusX * cos(angle);
            int y = centerY + radiusY * sin(angle);

            // Draw a single point at the calculated position
            // SDL_RenderDrawPoint places a pixel at the specified coordinates.
            SDL_RenderDrawPoint(renderer, x, y);
        }
    }
}

/////////////////////////////////////////////////////////////////////////////
//                  Cursor
/////////////////////////////////////////////////////////////////////////////

// Function to create a new cursor at a specified position
// Parameters:
//   x, y: The initial coordinates of the new cursor.
// Returns:
//   A pointer to the newly created cursor, or NULL if the maximum number of cursors has been reached.
Cursor* create_cursor(double x, double y) {
    // Check if the maximum number of active cursors has been reached
    if (active_cursors >= MAX_CURSORS) {
        // Print an error message if no more cursors can be created
        printf("Error: Maximum number of cursors reached\n");
        return NULL; // Return NULL to indicate that the cursor creation failed
    }

    // Find the first available slot in the cursors array
    int index = 0;
    while (index < MAX_CURSORS && cursors[index].active) {
        // Increment the index until an inactive cursor slot is found
        index++;
    }

    // Initialize the cursor properties in the available slot
    cursors[index] = (Cursor){
        .x = x,             // Set the initial x-coordinate of the cursor
        .y = y,             // Set the initial y-coordinate of the cursor
        .angle = 0.0,       // Set the initial angle (direction) to 0 degrees
        .thickness = 1,     // Set the default thickness of lines drawn by the cursor
        .color = black,     // Set the default color of the cursor to black
        .visible = true,    // Make the cursor visible by default
        .active = true      // Mark the cursor as active
    };

    // Increment the count of active cursors
    active_cursors++;

    // Return a pointer to the newly created cursor
    return &cursors[index];
}


// Function to move a cursor by a specified distance in its current direction
// Parameters:
//   cursor: A pointer to the Cursor object to be moved.
//   distance: The distance to move the cursor along its current angle.
// Behavior:
//   Updates the cursor's x and y coordinates based on its current angle.
//   The movement is calculated using trigonometry (cosine and sine).
void move_cursor(Cursor* cursor, double distance) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Convert the cursor's angle from degrees to radians
    // SDL uses radians for trigonometric functions, so conversion is necessary.
    double radians = cursor->angle * PI / 180.0;

    // Update the x-coordinate based on the movement distance and the cosine of the angle
    cursor->x += distance * cos(radians);

    // Update the y-coordinate based on the movement distance and the sine of the angle
    cursor->y += distance * sin(radians);
}


// Function to rotate a cursor by a specified angle
// Parameters:
//   cursor: A pointer to the Cursor object to be rotated.
//   angle: The angle (in degrees) by which to rotate the cursor.
// Behavior:
//   Updates the cursor's angle, ensuring it remains within the range [0, 360).
void rotate_cursor(Cursor* cursor, double angle) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Add the specified angle to the cursor's current angle
    cursor->angle += angle;

    // Normalize the angle to ensure it stays within the range [0, 360)
    // If the angle is 360 or greater, subtract 360 repeatedly until it falls within the range.
    while (cursor->angle >= 360.0) cursor->angle -= 360.0;

    // If the angle is negative, add 360 repeatedly until it falls within the range.
    while (cursor->angle < 0.0) cursor->angle += 360.0;
}


// Function to set the color of a cursor
// Parameters:
//   cursor: A pointer to the Cursor object whose color is to be changed.
//   color: An SDL_Color structure representing the new color to be assigned to the cursor.
// Behavior:
//   Updates the cursor's `color` property with the specified color.
void set_cursor_color(Cursor* cursor, SDL_Color color) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Update the cursor's color property to the specified color
    cursor->color = color;
}


// Function to set the visibility of a cursor
// Parameters:
//   cursor: A pointer to the Cursor object whose visibility is to be changed.
//   visible: A boolean indicating whether the cursor should be visible (true) or hidden (false).
// Behavior:
//   Updates the `visible` property of the cursor to control its visibility status.
void set_cursor_visibility(Cursor* cursor, bool visible) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Update the cursor's visibility property
    // If `visible` is true, the cursor becomes visible; otherwise, it becomes hidden.
    cursor->visible = visible;
}


/////////////////////////////////////////////////////////////////////////////
//                  Cursor Shape
/////////////////////////////////////////////////////////////////////////////

// Function to draw a line starting from the cursor's current position
// Parameters:
//   cursor: A pointer to the Cursor object that will draw the line.
//   length: The length of the line to be drawn.
// Behavior:
//   The function calculates the endpoint of the line based on the cursor's current angle and position.
//   It then uses the `draw_line` function to render the line on the screen with the cursor's color.
void cursor_draw_line(Cursor* cursor, double length) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Calculate the endpoint of the line using the cursor's angle
    // Convert the angle from degrees to radians as trigonometric functions in C use radians.
    double endX = cursor->x + length * cos(cursor->angle * PI / 180.0); // Calculate the x-coordinate of the endpoint
    double endY = cursor->y + length * sin(cursor->angle * PI / 180.0); // Calculate the y-coordinate of the endpoint

    // Draw the line using the cursor's current position as the starting point
    // and the calculated endpoint. Use the cursor's color for the line.
    draw_line(cursor->x, cursor->y, endX, endY, cursor->color);
}


// Function to draw a rectangle starting from the cursor's current position
// Parameters:
//   cursor: A pointer to the Cursor object that will draw the rectangle.
//   width: The width of the rectangle to be drawn.
//   height: The height of the rectangle to be drawn.
//   filled: A boolean indicating whether the rectangle should be filled (true) or outlined (false).
// Behavior:
//   The function draws a rectangle with the top-left corner at the cursor's current position
//   using the cursor's color for the rectangle.
void cursor_draw_rectangle(Cursor* cursor, double width, double height, bool filled) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Call the draw_rectangle function to render the rectangle
    // Use the cursor's current position (x, y) as the top-left corner of the rectangle.
    // Pass the specified width, height, and filled status, along with the cursor's color.
    draw_rectangle(cursor->x, cursor->y, width, height, filled, cursor->color);
}

// Function to draw a circle centered at the cursor's current position
// Parameters:
//   cursor: A pointer to the Cursor object that will draw the circle.
//   radius: The radius of the circle to be drawn.
//   filled: A boolean indicating whether the circle should be filled (true) or just outlined (false).
// Behavior:
//   The function uses the cursor's position as the center of the circle
//   and draws the circle with the specified radius and fill status, using the cursor's color.
void cursor_draw_circle(Cursor* cursor, double radius, bool filled) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Call the draw_circle function to render the circle
    // Use the cursor's current position (x, y) as the center of the circle.
    // Pass the specified radius, filled status, and the cursor's color.
    draw_circle(cursor->x, cursor->y, radius, filled, cursor->color);
}

// Function to draw a triangle starting from the cursor's current position
// Parameters:
//   cursor: A pointer to the Cursor object that will draw the triangle.
//   base: The base length of the triangle.
//   height: The height of the triangle.
//   filled: A boolean indicating whether the triangle should be filled (true) or outlined (false).
// Behavior:
//   The function calculates the coordinates of the three vertices of the triangle
//   based on the cursor's position, the specified base and height.
//   It then uses the `draw_triangle` function to render the triangle on the screen with the cursor's color.
void cursor_draw_triangle(Cursor* cursor, double base, double height, bool filled) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Calculate the coordinates of the three vertices of the triangle
    double x1 = cursor->x;
    double y1 = cursor->y;
    double x2 = cursor->x + base * cos(cursor->angle * PI / 180.0);
    double y2 = cursor->y + base * sin(cursor->angle * PI / 180.0);
    double x3 = cursor->x - base * sin(cursor->angle * PI / 180.0);
    double y3 = cursor->y + base * cos(cursor->angle * PI / 180.0);

    // Draw the triangle using the calculated vertex coordinates and the cursor's color
    draw_triangle(x1, y1, x2, y2, x3, y3, filled, cursor->color);
}

// Function to draw an ellipse centered at the cursor's current position
// Parameters:
//   cursor: A pointer to the Cursor object that will draw the ellipse.
//   radiusX: The horizontal radius of the ellipse.
//   radiusY: The vertical radius of the ellipse.
//   filled: A boolean indicating whether the ellipse should be filled (true) or just outlined (false).
// Behavior:
//   The function uses the cursor's position as the center of the ellipse
//   and draws the ellipse with the specified horizontal and vertical radii,
//   using the cursor's color.
void cursor_draw_ellipse(Cursor* cursor, double radiusX, double radiusY, bool filled) {
    // Check if the cursor is valid and active
    // If the cursor is NULL or inactive, the function does nothing and returns immediately.
    if (!cursor || !cursor->active) return;

    // Call the draw_ellipse function to render the ellipse
    // Use the cursor's current position (x, y) as the center of the ellipse.
    // Pass the specified horizontal and vertical radii, filled status, and the cursor's color.
    draw_ellipse(cursor->x, cursor->y, radiusX, radiusY, filled, cursor->color);
}

int main(int argc, char* argv[]) {
    //TODO
}