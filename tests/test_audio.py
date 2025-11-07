
from playwright.sync_api import Page, expect, sync_playwright
import os

def test_audio_play_once(page: Page):
    """
    This test verifies that the audio 'play' method is called only once,
    even if the 'Yes' or 'No' buttons are clicked multiple times.
    """
    # 1. Arrange: Go to the index.html page.
    path = os.path.abspath('index.html')
    page.goto(f'file://{path}')

    # Inject a script to spy on the 'play' method of HTMLAudioElement.
    page.evaluate("""() => {
        window.playCallCount = 0;
        const originalPlay = window.HTMLAudioElement.prototype.play;
        window.HTMLAudioElement.prototype.play = function() {
            window.playCallCount++;
            // We need to return the result of the original play method.
            // In a real scenario, this would be a Promise.
            // For this test, we can return a resolved Promise.
            return Promise.resolve();
        };
    }""")

    # 2. Act & Assert for "No" button
    no_button = page.locator("#noButton")
    no_button.click()
    play_count = page.evaluate("window.playCallCount")
    assert play_count == 1, f"Expected play count to be 1, but it was {play_count}"

    no_button.click()
    play_count = page.evaluate("window.playCallCount")
    assert play_count == 1, f"Expected play count to be 1 after second click, but it was {play_count}"

    # Reset for the "Yes" button test
    page.reload()
    page.evaluate("""() => {
        window.playCallCount = 0;
        const originalPlay = window.HTMLAudioElement.prototype.play;
        window.HTMLAudioElement.prototype.play = function() {
            window.playCallCount++;
            return Promise.resolve();
        };
    }""")

    # 3. Act & Assert for "Yes" button
    yes_button = page.locator("#yesButton")
    yes_button.click()
    play_count = page.evaluate("window.playCallCount")
    assert play_count == 1, f"Expected play count to be 1, but it was {play_count}"

    # The "Yes" button disappears after one click, so we can't click it again.
    # The test for the "Yes" button is complete.

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_audio_play_once(page)
            print("Test passed!")
        finally:
            browser.close()
