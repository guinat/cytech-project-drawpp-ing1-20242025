#include "../lib/DPP/include/drawpp.h"
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

int main(int argc, char* argv[]) {
    if (!initialize_SDL()) {
        printf("Failed to initialize SDL\n");
        return 1;
    }
    
    int windowWidth = 800;
    int windowHeight = 600;
    int flagWidth = 300;
    int flagHeight = 200;
    int bandWidth = (flagWidth / 3);
    int startX = ((windowWidth - flagWidth) / 2);
    int startY = ((windowHeight - flagHeight) / 2);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);
    Cursor* cBlue = create_cursor(startX, startY);
    set_cursor_color(cBlue, blue);
    cursor_draw_rectangle(cBlue, bandWidth, flagHeight, true);
    SDL_RenderPresent(renderer);
    SDL_Delay(1000);
    Cursor* cWhite = create_cursor((startX + bandWidth), startY);
    set_cursor_color(cWhite, white);
    cursor_draw_rectangle(cWhite, bandWidth, flagHeight, true);
    SDL_RenderPresent(renderer);
    SDL_Delay(1000);
    Cursor* cRed = create_cursor((startX + (bandWidth * 2)), startY);
    set_cursor_color(cRed, red);
    cursor_draw_rectangle(cRed, bandWidth, flagHeight, true);
    SDL_RenderPresent(renderer);
    SDL_Delay(1000);
    SDL_RenderPresent(renderer);
    
    // Event loop waiting for window closure
    bool running = true;
    SDL_Event event;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }
    }
    cleanup_SDL();
    return 0;
}