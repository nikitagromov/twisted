"""
Interfaces for Trial.
"""

# Copyright (c) 2001-2007 Twisted Matrix Laboratories.
# See LICENSE for details.
# Maintainer: Jonathan Lange <jml@twistedmatrix.com>

import zope.interface as zi
from zope.interface import Attribute


class ITestCase(zi.Interface):
    """
    DEPRECATED in Twisted 2.5.

    This interface will be removed in the next release.  Implementing it has no
    impact.
    """


    def setUp():
        """I am run before each method is run"""


    def tearDown():
        """I am run after each method is run"""



class IReporter(zi.Interface):
    """
    I report results from a run of a test suite.
    """

    stream = zi.Attribute("The io-stream that this reporter will write to")
    tbformat = zi.Attribute("Either 'default', 'brief', or 'verbose'")
    args = zi.Attribute(
        "Additional string argument passed from the command line")
    shouldStop = zi.Attribute(
        """
        A boolean indicating that this reporter would like the test run to stop.
        """)
    separator = Attribute(
        """A value which will occasionally be passed to the L{write} method.""")
    testsRun = Attribute(
        """
        The number of tests that seem to have been run according to this
        reporter.
        """)


    def startTest(method):
        """
        Report the beginning of a run of a single test method.

        @param method: an object that is adaptable to ITestMethod
        """


    def stopTest(method):
        """
        Report the status of a single test method

        @param method: an object that is adaptable to ITestMethod
        """


    def startSuite(name):
        """
        DEPRECATED in Twisted 2.6.

        Suites which wish to appear in reporter output should call this
        before running their tests.
        """


    def endSuite(name):
        """
        DEPRECATED in Twisted 2.6.

        Called at the end of a suite, if and only if that suite has called
        C{startSuite}.
        """


    def cleanupErrors(errs):
        """
        DEPRECATED in Twisted 2.6.

        Called when the reactor has been left in a 'dirty' state

        @param errs: a list of L{twisted.python.failure.Failure}s
        """


    def upDownError(userMeth, warn=True, printStatus=True):
        """
        Called when an error occurs in a setUp* or tearDown* method

        @param warn: indicates whether or not the reporter should emit a
                     warning about the error
        @type warn: Boolean
        @param printStatus: indicates whether or not the reporter should
                            print the name of the method and the status
                            message appropriate for the type of error
        @type printStatus: Boolean
        """


    def addSuccess(test):
        """
        Record that test passed.
        """


    def addError(test, error):
        """
        Record that a test has raised an unexpected exception.

        @param test: The test that has raised an error.
        @param error: The error that the test raised. It will either be a
            three-tuple in the style of C{sys.exc_info()} or a
            L{Failure<twisted.python.failure.Failure>} object.
        """


    def addFailure(test, failure):
        """
        Record that a test has failed with the given failure.

        @param test: The test that has failed.
        @param failure: The failure that the test failed with. It will
            either be a three-tuple in the style of C{sys.exc_info()}
            or a L{Failure<twisted.python.failure.Failure>} object.
        """


    def addExpectedFailure(test, failure, todo):
        """
        Record that the given test failed, and was expected to do so.

        @type test: L{pyunit.TestCase}
        @param test: The test which this is about.
        @type error: L{failure.Failure}
        @param error: The error which this test failed with.
        @type todo: L{unittest.Todo}
        @param todo: The reason for the test's TODO status.
        """


    def addUnexpectedSuccess(test, todo):
        """
        Record that the given test failed, and was expected to do so.

        @type test: L{pyunit.TestCase}
        @param test: The test which this is about.
        @type todo: L{unittest.Todo}
        @param todo: The reason for the test's TODO status.
        """


    def addSkip(test, reason):
        """
        Record that a test has been skipped for the given reason.

        @param test: The test that has been skipped.
        @param reason: An object that the test case has specified as the reason
            for skipping the test.
        """


    def printSummary():
        """
        Present a summary of the test results.
        """


    def printErrors():
        """
        Present the errors that have occured during the test run. This method
        will be called after all tests have been run.
        """


    def write(string):
        """
        Display a string to the user, without appending a new line.
        """


    def writeln(string):
        """
        Display a string to the user, appending a new line.
        """

    def wasSuccessful():
        """
        Return a boolean indicating whether all test results that were reported
        to this reporter were successful or not.
        """
