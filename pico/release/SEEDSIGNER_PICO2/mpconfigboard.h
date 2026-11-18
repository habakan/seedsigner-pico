// The release build: no USB at all, so no REPL, raw REPL or file copy can run code beside the frozen main.py
#define MICROPY_HW_BOARD_NAME "SeedSigner Pico 2"
#define MICROPY_HW_ENABLE_USBDEV (0)
