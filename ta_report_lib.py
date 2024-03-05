Python Reporting Library.
Reports test results and score to General.log.
"""


import ta_rtl_lib as rtl_lib


logger = rtl_lib.get_logger(__name__)


# Globals:
GENERAL_LOG = 'General.log'


def add_result(strStatus, strDescription='', strStepName='', strTestName='', strExpected='', strActual=''):
    """Updates General.log file with test result."""

    strResult = '[Result]Status=' + strStatus + '$Description=' + strDescription + '$Step_Name=' + strStepName + '$Test=' + strTestName + '$Expected=' + strExpected + '$Actual=' + strActual +'\n'
    logger.debug(strResult.rstrip('\n'))
    with open(GENERAL_LOG, 'a') as genLog:
        genLog.write(strResult)


def add_score(strStatus, strDescription='', strStepName='', numScore='', strUnits='', strZDepth=''):
    """Updates General.log file with test score.
    Notes from http://confluence.amd.com/pages/viewpage.action?spaceKey=SQATOOLS&title=Performance+Test+Report+Usage page:
        1. In order to compare specific test cases, test steps should be filled with 'score' field with a numeric value.
        2. By default higher score is considered better when performing comparisons.
        3. For those tests which required to show lower score is better, Z-Depth field should have a keyword 'latency'.
    """

    strScore = '[Result]Status=' + strStatus + '$Description=' + strDescription + '$Step_Name=' + strStepName + '$Score=' + str(numScore) + '$Units=' + strUnits + '$ZDepth=' + strZDepth +'\n'
    logger.debug(strScore.rstrip('\n'))
    with open(GENERAL_LOG, 'a') as genLog:
        genLog.write(strScore)