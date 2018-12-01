import contextlib
import io


class HandConstants:
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    NO_HAND = 1


class StdoutCapture:

    def __init__(self, func):
        """
        Captures the output written to STDOUT when func is invoked.
        """
        self.func = func

    def capture(self):
        """
        :return: a tuple (func return, String) containing the function output and the output written to STDOUT.
        """
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            result = self.func()

        return result, capture.getvalue()
