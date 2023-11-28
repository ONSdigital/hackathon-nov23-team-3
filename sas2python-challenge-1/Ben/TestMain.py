import unittest
import tkinter as tk
import test_main
import io
import sys

class TestMain(unittest.TestCase):
    def test_end_to_end(self):
        result = test_main.test_remove_incomplete_periods()
        self.assertEqual(result, expected_result)

root = tk.Tk()
text = tk.Text(root)
text.pack()

class IORedirector(object):
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    def write(self,string):
        self.text_area.insert(tk.END,string)
        self.text_area.see(tk.END)
    def flush(self):
        pass

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(stream=StdoutRedirector(text)).run(suite)

button = tk.Button(root, text="Run tests", command=run_tests)
button.pack()

root.mainloop()