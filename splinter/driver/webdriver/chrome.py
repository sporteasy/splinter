# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    def __init__(self, user_agent=None, *args, **kwargs):
        self._patch_subprocess()
        options = Options()

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        options.add_argument("--disable-translate")

        self.driver = Chrome(chrome_options=options)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(*args, **kwargs)
