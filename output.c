#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main() {
    int x = 10;
    float y = 20.5;
    if ((x < y)) {
        x = (x + 1);
    }
    else {
        x = (x - 1);
    }
    return 0;
}