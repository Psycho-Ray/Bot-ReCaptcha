import os

from botcity.web import WebBot, Browser

from botcity.plugins.captcha import BotAntiCaptchaPlugin
from botcity.plugins.http import BotHttpPlugin


class Bot(WebBot):
    def action(self, execution=None):
        # Init
        self.headless = False
        self.driver_path = "./chromedriver.exe"

        # Disable these comments to use Firefox instead
        # self.driver_path = "./geckodriver.exe"
        # self.browser = Browser.FIREFOX

        # Opens the BotCity website.
        self.browse("https://www.google.com/recaptcha/api2/demo")

        # Anti-Captcha - ReCaptcha
        captcha_id = self.find_element('.g-recaptcha').get_attribute('data-sitekey')
        anti_captcha = BotAntiCaptchaPlugin(os.getenv("ANTICAPTCHA_KEY"))
        response = anti_captcha.solve_re("https://www.google.com/recaptcha/api2/demo", captcha_id)

        # Injects the response into the webpage
        self.execute_javascript('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)

        # Clicks submit
        submit = self.find_element("#recaptcha-demo-submit")
        submit.click()

        # Checks if it worked
        assert self.find_element(".recaptcha-success")
        print("Success!")

        # Stop the browser and clean up
        self.wait(3000)
        self.stop_browser()


if __name__ == '__main__':
    Bot.main()
