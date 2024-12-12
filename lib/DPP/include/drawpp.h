#ifndef DRAWPP_H
#define DRAWPP_H

#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdio.h>
#include <math.h>

// Include all sub-components
#include "cursor.h"
#include "shapes.h"
#include "colors.h"

// Constants
#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600
#define PI 3.14159265358979323846
#define MAX_CURSORS 10

// SDL Window and Renderer
extern SDL_Window* window;
extern SDL_Renderer* renderer;

// Global cursor array
extern Cursor cursors[MAX_CURSORS];
extern int active_cursors;

// SDL initialization and cleanup
bool initialize_SDL(void);
void cleanup_SDL(void);

#endif /* DRAWPP_H */