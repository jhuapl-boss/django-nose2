import sys

from contextlib import contextmanager
import logging

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from django.test import simple as DiscoverRunner

from nose2.main import discover
from django.test.utils import override_settings
from spdb.spatialdb.test.setup import get_test_configuration

log = logging.getLogger(__name__)

KVIO_SETTINGS, STATEIO_CONFIG, OBJECTIO_CONFIG, _ = get_test_configuration()


class TestRunner(DiscoverRunner):

    err_count = 0
    _hooks = ('startTestRun', 'reportFailure', 'reportError', 'startTest')

    def hooks(self):
        return [(hook, self) for hook in self._hooks]

    # Must do override settings here for it to effect the class
    @override_settings(KVIO_SETTINGS=KVIO_SETTINGS)
    @override_settings(STATEIO_CONFIG=STATEIO_CONFIG)
    @override_settings(OBJECTIO_CONFIG=OBJECTIO_CONFIG)
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        print("####RUN_TESTS")
        log.debug('Running tests with nose2')
        self.extra_tests = extra_tests
        with self.test_environment():
            argv = self.make_argv(test_labels)
            discover(argv=argv, exit=False, extraHooks=self.hooks())
            return self.err_count

    def make_argv(self, test_labels):
        argv = ['nose2']
        argv.extend(['-v'] * (self.verbosity - 1))

        if self.failfast:
            argv.append('-F')

        # keep nose2 args separate from django/manage args
        if '--' in sys.argv:
            argv.extend(sys.argv[sys.argv.index('--')+1:])

        # DMK - assuming all test discovery is defined in the nose2 config file
        #if test_labels:
        #    argv.extend([t for t in test_labels if not t.startswith('-')])

        return argv

    @contextmanager
    def test_environment(self):
        self.setup_test_environment()
        old_config = self.setup_databases()
        log.debug("Django test environment set up")
        try:
            yield
        finally:
            self.teardown_databases(old_config)
            self.teardown_test_environment()
            log.debug("Django test environment torn down")

    # plugin hooks the runner handles
    def startTestRun(self, event):
        if self.extra_tests is None:
            return
        for test in self.extra_tests:
            event.suite.addTest(test)

    def startTest(self, event):
        print("**** decorating test")
        event.test = override_settings(event.test, OBJECTIO_CONFIG=get_test_configuration()[2])

    def reportFailure(self, event):
        self.err_count += 1

    def reportError(self, event):
        self.reportFailure(event)

