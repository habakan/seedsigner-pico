# The release build: RPI_PICO2 on its Arm cores, which secure boot needs
include(${MICROPY_PORT_DIR}/boards/RPI_PICO2/mpconfigboard.cmake)
set(PICO_PLATFORM "rp2350")
