# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -I./SDL2/include -I./DPP/include -fPIC
AR = ar
ARFLAGS = rcs

# Directories
SRC_DIR = DPP/src
INCLUDE_DIR = DPP/include
BUILD_DIR = build

# Source files and objects
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Library name
STATIC_LIB = libdrawpp.a

# Default target
all: directories $(STATIC_LIB)

# Create build directory
directories:
	mkdir -p $(BUILD_DIR)

# Static library
$(STATIC_LIB): $(OBJECTS)
	$(AR) $(ARFLAGS) $@ $^

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build files
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(STATIC_LIB)

.PHONY: all directories clean
