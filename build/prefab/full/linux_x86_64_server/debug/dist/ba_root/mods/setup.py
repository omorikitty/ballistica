# ba_meta require api 9

import babase
import bascenev1 as bs
import logging
from database.test import test_stats, test_customer
from bascenev1._activitytypes import ScoreScreenActivity
from stats import mystats
from myspaz import spazeffect

# print(settings.URI)


# ba_meta export plugin
class Startup(babase.Plugin):
    def on_app_running(self):
        print("Hello World")


def score_screen_on_begin(func) -> None:
    """Runs when score screen is displayed."""

    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        mystats.update(self._stats)

        return result

    return wrapper


ScoreScreenActivity.on_begin = score_screen_on_begin(ScoreScreenActivity.on_begin)
spazeffect.apply()