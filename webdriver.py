from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Driver:
    """Uses Selenium to scrape YouTube video captions"""
    WAIT_TIME = 10 # Response waiting threshold

    def __init__(self):
        """Runs the web driver in headless mode"""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(self.options)

    def open_url(self, url):
        """Loads the given url"""
        self.driver.get(url)

    def find_captions(self) -> dict:
        """
        Opens video captions on YouTube and saves all of them in a dict of {time : text} pairs.
        :return: the resulting dictionary
        """
        show_text_btn_xpath = ("/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/"
                               "ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/div[2]/"
                               "ytd-structured-description-content-renderer/div/"
                               "ytd-video-description-transcript-section-renderer/"
                               "div[3]/div/ytd-button-renderer/yt-button-shape/button")

        WebDriverWait(self.driver, self.WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "expand"))).click()
        WebDriverWait(self.driver, self.WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, show_text_btn_xpath))).click()
        transcript = WebDriverWait(self.driver, self.WAIT_TIME).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ytd-transcript-segment-renderer")))

        return {line.find_element(By.CSS_SELECTOR, ".segment-timestamp").text:
                line.find_element(By.CSS_SELECTOR, ".segment-text").text for line in transcript}


if __name__ == "__main__":
    ...

