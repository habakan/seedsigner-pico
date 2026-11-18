# Frozen, so it runs in place of any main.py on the filesystem; with no USB there is no REPL to fall back to
import machine
try:
    import pico_boot
    from seedsigner.controller import Controller
    Controller.get_instance().start()
finally:
    machine.reset()
