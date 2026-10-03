import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import firefox_relay as relay


class Element:
    def __init__(self):
        self.value = ''
        self.keys = []

    def click(self): pass
    def send_keys(self, value): self.keys.append(value)
    def get_property(self, name): return self.value


class Driver:
    def __init__(self, mismatch=False, changing=False):
        self.element = Element()
        self.mismatch = mismatch
        self.changing = changing
        self.reads = 0
        self.script_input = None

    def get(self, url): pass
    def find_element(self, *args): return self.element
    def execute_script(self, script, element, prompt):
        self.script_input = prompt
        element.value = prompt[:-1] if self.mismatch else prompt
        return element.value
    def find_elements(self, *args):
        self.reads += 1
        if self.reads == 1: return []
        return [SimpleNamespace(text=str(self.reads) if self.changing else 'complete answer')]


class Wait:
    def __init__(self, driver, timeout): self.driver = driver
    def until(self, predicate): return predicate(self.driver)


class Clock:
    def __init__(self): self.tick = 0
    def __call__(self):
        self.tick += 1
        return self.tick


class TransportRegression(unittest.TestCase):
    def browser(self, driver):
        browser = relay.Browser.__new__(relay.Browser)
        browser.driver = driver
        browser.Keys = SimpleNamespace(ENTER='<ENTER>')
        browser.Wait = Wait
        browser.lock = threading.Lock()
        return browser

    def test_complete_large_multiline_input_is_inserted_without_typing(self):
        prompt = ('# reference\nA+ B− C+\n`$()` \\"\n' * 2000)
        driver = Driver()
        with patch('firefox_relay.time.monotonic', Clock()), patch('firefox_relay.time.sleep'):
            answer = self.browser(driver).ask(prompt, timeout=20)
        self.assertEqual(driver.script_input, prompt)
        self.assertEqual(driver.element.value, prompt)
        self.assertEqual(driver.element.keys, ['<ENTER>'])
        self.assertEqual(answer, 'complete answer')

    def test_input_mismatch_is_never_submitted(self):
        driver = Driver(mismatch=True)
        with self.assertRaisesRegex(RuntimeError, 'nothing submitted'):
            self.browser(driver).ask('full reference')
        self.assertEqual(driver.element.keys, [])

    def test_timeout_does_not_return_partial_stream(self):
        driver = Driver(changing=True)
        with patch('firefox_relay.time.monotonic', Clock()), patch('firefox_relay.time.sleep'):
            with self.assertRaisesRegex(RuntimeError, 'Timed out'):
                self.browser(driver).ask('reference', timeout=4)


if __name__ == '__main__': unittest.main()
