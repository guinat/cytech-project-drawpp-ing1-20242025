#include "../lib/DPP/include/drawpp.h"
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

int main(int argc, char* argv[]) {
    printf("Initializing SDL...\n");
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
    Cursor* cWhite = create_cursor((startX + bandWidth), startY);
    set_cursor_color(cWhite, white);
    cursor_draw_rectangle(cWhite, bandWidth, flagHeight, true);
    Cursor* cRed = create_cursor((startX + (bandWidth * 2)), startY);
    set_cursor_color(cRed, red);
    cursor_draw_rectangle(cRed, bandWidth, flagHeight, true);
    SDL_RenderPresent(renderer);
    
    SDL_Delay(100);
    printf("Presenting renderer...\n");
    SDL_RenderPresent(renderer);
    
    printf("Saving output image...\n");
    SDL_Surface* surface = SDL_CreateRGBSurfaceWithFormat(
        0, windowWidth, windowHeight, 32, SDL_PIXELFORMAT_RGBA8888);
    
    if (!surface) {
        printf("Failed to create surface\n");
        cleanup_SDL();
        return 1;
    }
    
    if (SDL_RenderReadPixels(renderer, NULL, surface->format->format, surface->pixels, surface->pitch) != 0) {
        printf("Failed to read pixels: %s\n", SDL_GetError());
    }
    else if (SDL_SaveBMP(surface, "output.bmp") != 0) {
        printf("Failed to save BMP: %s\n", SDL_GetError());
    } else {
        printf("Image saved as output.bmp\n");
    }
    
    SDL_FreeSurface(surface);
    
    printf("Cleaning up...\n");
    cleanup_SDL();
    
    printf("Done!\n");
    return 0;
}