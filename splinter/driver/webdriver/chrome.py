# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Chrome
from selenium.webdriver.chrome import options as chrome_options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class Options(chrome_options.Options):

    def __init__(self):
        super(Options, self).__init__()
        self._prefs = {}

    def add_pref(self, key, value):
        self._prefs[key] = value

    def to_capabilities(self):
        capabilities = super(Options, self).to_capabilities()
        if self._prefs:
            capabilities['chromeOptions']['prefs'] = self._prefs
        return capabilities


class WebDriver(BaseWebDriver):

    driver_name = "Chrome"

    def __init__(self, options=None, user_agent=None, wait_time=2, fullscreen=False, incognito=False,
                 *args, **kwargs):

        options = Options() if options is None else options
        options.add_argument("--disable-translate")
        options.add_argument("--disable-notifications")

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if 'accepted_languages' in kwargs:
            options.add_pref('intl.accept_languages', kwargs['accepted_languages'])
            del kwargs['accepted_languages']

        if incognito:
            options.add_argument("--incognito")

        if fullscreen:
            options.add_argument('--kiosk')

        self.driver = Chrome(chrome_options=options, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time, *args, **kwargs)
