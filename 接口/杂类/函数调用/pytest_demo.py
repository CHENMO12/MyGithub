import pytest
import os

class Test():
    def test_01(self):
        assert 3 == 4
    def test_02(self):
        assert 4 == 4

if __name__ == "__main__":
  pytest.main(["-q","pytest_demo.py"])
  cmd = "pytest --html=./report.html"
  os.popen(cmd)
