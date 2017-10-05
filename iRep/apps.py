# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class IrepConfig(AppConfig):
    name = 'iRep'

    def ready(self):
        import Signals
