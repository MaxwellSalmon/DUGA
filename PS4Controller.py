# Support for PlayStation DualShock 4 Controllers

import pygame


class PS4Controller(object):
    """Represent and initialize a PS4 Controller device, called "joystick" in pygame.
    If we find more than one, only the first one will be initialized.
    """
    joystick = None

    def init(self):
        """Initialize the joystick module."""

        # Initialize pygame and the joystick module; both functions are safe to call multiple times
        pygame.init()
        pygame.joystick.init()

        # Do we have any controllers plugged in?
        nof_joysticks = pygame.joystick.get_count()
        if 0 == nof_joysticks:
            raise Exception("Could not find any joystick controllers")

        # Print out the names of all joysticks; this can be done before initializing them
        for i in range(nof_joysticks):
            js = pygame.joystick.Joystick(i)
            print("Joystick #%d is called '%s'" % (js.get_id(), js.get_name()))

        # Pick the first one
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Print out some more details; this can only be done after initializing
        print("Using joystick #%d with %d buttons, %d axes and %d hats" % (
            self.joystick.get_id(),
            self.joystick.get_numbuttons(),
            self.joystick.get_numaxes(),
            self.joystick.get_numhats()))
