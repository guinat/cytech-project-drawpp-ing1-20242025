#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdio.h>
#include <math.h>

// Constants
#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600
#define PI 3.14159265358979323846
#define MAX_CURSORS 10

// Structure to define a cursor
typedef struct {
    double x;
    double y;
    double angle;
    int thickness;
    SDL_Color color;
    bool visible;
    bool active;
} Cursor;

// Function declarations
bool initialize_SDL(void);
void cleanup_SDL(void);
SDL_Color custom_color(Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Drawing functions
void draw_line(int x1, int y1, int x2, int y2, SDL_Color color);
void draw_rectangle(int x, int y, int width, int height, bool filled, SDL_Color color);
void draw_circle(int centerX, int centerY, int radius, bool filled, SDL_Color color);
void draw_triangle(int x1, int y1, int x2, int y2, int x3, int y3, bool filled, SDL_Color color);
void draw_ellipse(int centerX, int centerY, int radiusX, int radiusY, bool filled, SDL_Color color);

// Cursor functions
Cursor* create_cursor(double x, double y);
void move_cursor(Cursor* cursor, double distance);
void rotate_cursor(Cursor* cursor, double angle);
void set_cursor_color(Cursor* cursor, SDL_Color color);
void set_cursor_visibility(Cursor* cursor, bool visible);

// External variables
extern SDL_Window* window;
extern SDL_Renderer* renderer;
extern Cursor cursors[MAX_CURSORS];
extern int active_cursors;

// Predefined colors
extern SDL_Color black;
extern SDL_Color white;
extern SDL_Color red;
extern SDL_Color green;
extern SDL_Color blue;
extern SDL_Color gray;
extern SDL_Color orange;
extern SDL_Color purple;

int main(int argc, char* argv[]) {
    if (!initialize_SDL()) {
        printf("Failed to initialize SDL\n");
        return 1;
    }
    
    int width = 800;
    
    double angle = 45.0;
    
    char* message = "Hello Draw++";
    
    bool isDrawing = true;
    
    Cursor* main = create_cursor(400, 300);
    
    set_cursor_color(main, red);
    
    main->thickness = 2;
    
    if ((isDrawing == true)) {
        set_cursor_visibility(main, true);
        cursor_draw_rectangle(main, 60, 40, true);
    } else if ((width > 500)) {
        cursor_draw_circle(main, 30, false);
    } else {
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        SDL_RenderClear(renderer);
    }
    
    int i = 0;
    i = (i + 1);
    for (int i = 0; (i < 4); i = (i + 1)) {
        rotate_cursor(main, 90);
        move_cursor(main, 100);
    }
    
    double radius = ((width + angle) / 4);
    
    cursor_draw_circle(main, radius, true);
    
    set_cursor_color(main, custom_color(255, 0, 0, 255));
    
    cursor_draw_triangle(main, 50, 40, true);
    
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);
    cleanup_SDL();
    return 0;
}