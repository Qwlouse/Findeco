#!/usr/bin/env python

import sys, os, logging, pdb
###
from selenium import webdriver
from parse_sel import SeleniumParser
from selenium_driver import SeleniumDriver
from cmdargs import DEFAULT_FIXTURES_FILE


class SelexeError(Exception):
    """Custom Selexe error class"""
    pass


class SelexeRunner(object):
    """
    Selenium file execution class
    """
    def __init__(self, filename, baseuri=None, fixtures=None, pmd=False):
        self.filename = filename
        self.baseuri= baseuri
        self.setUpFunc, self.tearDownFunc = findFixtureFunctions(fixtures)
        self.pmd = pmd

    def run(self):
        """Start execution of selenium tests (within setUp and tearDown wrappers)"""
        logging.info('Selexe working on file %s' % self.filename)
        fp = open(self.filename)
        seleniumParser = SeleniumParser(fp)
        driver = webdriver.Firefox()
        baseURI = self.baseuri or seleniumParser.baseuri
        if baseURI.endswith('/'):
            baseURI = baseURI[:-1]
        logging.info('baseURI: %s' % baseURI)
        try:
            sd = SeleniumDriver(driver, baseURI)
            return self._wrapExecution(seleniumParser, sd)
        finally:
            driver.quit()

    def _wrapExecution(self, seleniumParser, sd):
        """Wrap execution of selenium tests in setUp and tearDown functions if available"""
        if self.setUpFunc:
            logging.info("Calling setUp()")
            self.setUpFunc(sd)
            logging.info("setUp() finished")
            # remove all verification errors possibly generated during setUpFunc()
            sd.initVerificationErrors()

        try:
            return self._executeSelenium(seleniumParser, sd)
        except:
            if self.pmd:
                exc = sys.exc_info()
                pdb.post_mortem(exc[2])
            else:
                raise
        finally:
            if self.tearDownFunc:
                logging.info("Calling tearDown()")
                self.tearDownFunc(sd)
                logging.info("tearDown() finished")

    def _executeSelenium(self, seleniumParser, sd):
        """Execute the actual selenium statements found in *sel file"""
        for command, target, value in seleniumParser:
            try:
                sd(command, target, value)
            except:
                logging.error('Command %s(%r, %r) failed.' % (command, target, value))
                raise
        return sd.getVerificationErrors()


def findFixtureFunctions(modulePath=None):
    if modulePath == DEFAULT_FIXTURES_FILE and not os.path.exists(DEFAULT_FIXTURES_FILE):
        # The default fixtures file could be missing, then just no fixtures will be used
        modulePath = None
    elif modulePath and not os.path.exists(modulePath):
        # non-default fixtures files must exist, else raise an exception!
        raise SelexeError('Cannot find selexe fixture module "%s"')

    if modulePath:
        path, moduleWithExt = os.path.split(os.path.realpath(modulePath))
        module = os.path.splitext(moduleWithExt)[0]
        if path and not path in sys.path:
            sys.path.append(path)
        mod = __import__(os.path.basename(module))
        setUpFunc = getattr(mod, 'setUp', None)
        tearDownFunc = getattr(mod, 'tearDown', None)
        if setUpFunc or tearDownFunc:
            logging.info('Using fixtures module %s (setUp: %s, tearDown: %s)' %
                        (modulePath, setUpFunc is not None, tearDownFunc is not None))
        else:
            logging.warning('Successfully imported fixtures module %s, but found no setUp or tearDown functions' %
                            modulePath)
    else:
        logging.info('Using no fixtures')
        setUpFunc, tearDownFunc = None, None
    return setUpFunc, tearDownFunc


if __name__ == '__main__':
    from cmdargs import parse_cmd_args
    (options, args) = parse_cmd_args()
    logging.basicConfig(level=options.logging)
    for selFilename in args:
        s = SelexeRunner(selFilename, baseuri=options.baseuri, pmd=options.pmd, fixtures=options.fixtures)
        res = s.run()
        if res:
            sys.stderr.write("\nVerification errors in %s: %s\n" % (selFilename, res))
    sys.exit(1)
