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
        self._prefs = {}

    def add_pref(self, key, value):
        self._prefs[key] = value

    def to_capabilities(self):
        capabilities = super(Options, self).to_capabilities()
        capabilities['chromeOptions']['prefs'] = self._prefs
        return capabilities


class WebDriver(BaseWebDriver):

    def __init__(self, user_agent=None, *args, **kwargs):
        self._patch_subprocess()

        options = Options()
        options.add_argument("--disable-translate")

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if 'accepted_languages' in kwargs:
            options.add_pref('intl.accept_languages', kwargs['accepted_languages'])
            del kwargs['accepted_languages']

        self.driver = Chrome(chrome_options=options)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(*args, **kwargs)
