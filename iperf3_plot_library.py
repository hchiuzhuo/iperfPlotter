import os.path
import subprocess
import sys
from robot.api import logger
from iperf3_plot import iperf3_dataParser

class iperf3_plot_library(object):
  def __init__(self):
    self._iperf3_dataParser_path = os.path.join(os.path.dirname(__file__),'iperf3_plot.py')
    self._parser = iperf3_dataParser()
    self._result = ''
    self._message = ''

  def parse_options(self, *args):
    self._result = self._parser.parseOptions(list(args))
    self._message = 'foldername {}\nplotFiles {}\nnoPlotFiles {}\noutput {}\nupperLimit {}\nlowerLimit {}\nbound {}'.format(
      self._result[0], str(self._result[1]), str(self._result[2]), self._result[3], self._result[4], self._result[5],
      str(self._result[6]))

  def parse_option_from_cmd(self, *args):
    self._message = self._run_command(args).strip()

  def print_message(self, msg):
    if self._message != msg:
      raise AssertionError("Expected message to be '%s' but was '%s'."% (msg, self._message))

  def result_should_be(self, *expected):
    val=list(str(x) for x in self._result)
    same = all(i == j for i, j in zip(val, expected))
    if (len(val) != len(expected)):
      raise AssertionError('Size different')
    if (not same):
      raise AssertionError('Expected message to be %s but was %s' % (expected,val))

  def _run_command(self, args):
    command = [sys.executable, self._iperf3_dataParser_path] + list(args)
    process = subprocess.Popen(command,universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return process.communicate()[0]