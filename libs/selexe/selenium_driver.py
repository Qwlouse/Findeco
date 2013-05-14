import logging, time, re, types, new
###
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from html2text import html2text




def create_get_or_is(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'is*' or 'get*' function.
    """
    def wrap_func(self, target, value=None):
        expectedResult, result = func(self, target, value=value)
        return result
    return wrap_func


def create_verify(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'verify*' function.
    """
    def wrap_func(self, target, value=None):
        try:
            expectedResult, result = func(self, target, value=value)  # can raise NoAlertPresentException
            assert self._matches(expectedResult, result)
            return True
        except NoAlertPresentException:
            verificationError = "There were no alerts or confirmations"
        except AssertionError:
            if result == False:
                # verifyTextPresent/verifyElementPresent only return True or False, so no proper comparison
                # can be made.
                verificationError = "false"
            else:
                verificationError = 'Actual value "%s" did not match "%s"' % (result, expectedResult)
        logging.error(verificationError)
        self.verificationErrors.append(verificationError)        
        return False
    return wrap_func


def create_verifyNot(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium '
    verifyNot*' function.
    """
    def wrap_func(self, target, value=None):
        try:
            expectedResult, result = func(self, target, value=value)  # can raise NoAlertPresentException
            assert not self._matches(expectedResult, result)
            return True
        except NoAlertPresentException:
            verificationError = "There were no alerts or confirmations"
        except AssertionError:
            if result == True:
                # verifyTextPresent/verifyElementPresent only return True or False, so no proper comparison
                # can be made.
                verificationError = "true"
            else:
                verificationError = 'Actual value "%s" did match "%s"' % (result, expectedResult)
        logging.error(verificationError)
        self.verificationErrors.append(verificationError)        
        return False
    return wrap_func


def create_assert(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'assert*' function.
    """
    def wrap_func(self, target, value=None):
        expectedResult, result = func(self, target, value=value)
        assert self._matches(expectedResult, result), \
                    'Actual value "%s" did not match "%s"' % (result, expectedResult)
    return wrap_func


def create_assertNot(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'assertNot*' function.
    """
    def wrap_func(self, target, value=None):
        expectedResult, result = func(self, target, value=value)
        assert not self._matches(expectedResult, result), \
                    'Actual value "%s" did match "%s"' % (result, expectedResult)
    return wrap_func


def create_waitFor(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'waitFor*' function.
    """
    def wrap_func(self, target, value=None):
        for i in range (self.num_repeats):
            try: 
                expectedResult, result = func(self, target, value=value)
                assert self._matches(expectedResult, result)
                break
            except AssertionError:
                time.sleep(self.poll)
        else:
            raise RuntimeError("Timed out after %d ms" % self.wait_for_timeout)
    return wrap_func


def create_waitForNot(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'waitForNot*' function.
    """
    def wrap_func(self, target, value=None):
        for i in range (self.num_repeats):
            try:
                expectedResult, result = func(self, target, value=value)
                assert not self._matches(expectedResult, result)
                break
            except AssertionError:
                time.sleep(self.poll)
        else:
            raise RuntimeError("Timed out after %d ms" % self.wait_for_timeout)
    return wrap_func


def create_store(func):
    """
    Decorator to convert a test method of class SeleniumCommander (starting with 'wd_SEL*') into a Selenium
    'store*' function.
    """
    def wrap_func(self, target, value=None):
        expectedResult, result = func(self, target, value=value)
        # for e.g. 'storeConfirmation' the variable name will be provided in 'target' (with 'value' being None),
        # for e.g. 'storeText' the variable name will be given in 'value' (target holds the element identifier)
        # The the heuristic is to use 'value' preferably over 'target' if available. Hope this works ;-)
        variableName = value or target
        self.storedVariables[variableName] = result
    return wrap_func


def create_selenium_methods(cls):
    """
    Class decorator to setup all available wrapping decorators to those methods in class SeleniumCommander
    starting with 'wd_SEL*'
    """
    GENERIC_METHOD_PREFIX = 'wd_SEL_'
    lstr = len(GENERIC_METHOD_PREFIX)

    def decorate_method(cls, methodName, prefix, decoratorFunc):
        """
        This method double-decorates a generic webdriver command.
        1. Decorate it with one of the create_get, create_verify... decorators.
           These decorators convert the generic methods into a real selenium commands.
        2. Decorate with the 'seleniumcommand' method decorator.
           This wrapper expands selenium variables in the 'target' and 'value' and
           does the logging.
        """
        seleniumMethodName = prefix + methodName[lstr:]
        wrappedMethod = decoratorFunc(cls.__dict__[methodName])
        wrappedMethod.__name__ = seleniumMethodName
        setattr(cls, seleniumMethodName, seleniumcommand(wrappedMethod))


    for methodName in cls.__dict__.keys():  # must loop over keys() as the dict gets modified while looping
        if methodName.startswith(GENERIC_METHOD_PREFIX):
            prefix = 'is' if methodName.endswith('Present') else 'get'
            decorate_method(cls, methodName, prefix, create_get_or_is)
            decorate_method(cls, methodName, 'verify', create_verify)
            decorate_method(cls, methodName, 'verifyNot', create_verifyNot)
            decorate_method(cls, methodName, 'assert', create_assert)
            decorate_method(cls, methodName, 'assertNot', create_assertNot)
            decorate_method(cls, methodName, 'waitFor', create_waitFor)
            decorate_method(cls, methodName, 'waitForNot', create_waitForNot)
            decorate_method(cls, methodName, 'store', create_store)
    return cls



def seleniumcommand(method):
    """
    Method decorator for selenium commands in SeleniumCommander class.
    Wraps all available selenium commands for expand selenium variables in 'target' and 'value'
    arguments.
    """
    def seleniumMethod(self, target, value=None, log=True, **kw):
        if log:
            logging.info('%s(%r, %r)' % (method.__name__, target, value))
        v_target = self._expandVariables(target)
        v_value  = self._expandVariables(value) if value else value
        return method(self, v_target, v_value, **kw)
    #
    seleniumMethod.__name__ = method.__name__
    seleniumMethod.__doc__ = method.__doc__
    return seleniumMethod


def create_aliases(cls):
    """
    Creates aliases (like the IDE) for commands with prefixes "verifyNot", "assertNot" or "waitForNot" which were generated 
    from generic commands with suffix "Present". For the aliases the "Not" is moved away from the prefix and placed 
    before "Present"(most likely to increase readability), e.g. "verifyTextNotPresent" aliases to "verifyNotTextPresent".
    """
    for methodName in cls.__dict__.keys():  # must loop over keys() as the dict gets modified while looping
        if re.match(r"(verifyNot|assertNot|waitForNot)\w+Present", methodName):
            method = getattr(cls, methodName)
            def aliasMethod(self, target, value=None):
                return method(self, target, value)
            alias = methodName.replace("Not", "").replace("Present", "NotPresent")
            setattr(cls, alias, aliasMethod)
    return cls


####################################################################################################
@create_aliases
@create_selenium_methods
class SeleniumDriver(object):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.initVerificationErrors()
        self._importUserFunctions()
        self.setTimeoutAndPoll(20000, 0.5)
        self.wait = False
        # 'storedVariables' is used through the 'create_store' decorator above to store values during a selenium run:
        self.storedVariables = {}
      
    def initVerificationErrors(self):
        """
        Reset the list of verification errors.
        """
        self.verificationErrors = []

    def getVerificationErrors(self):
        """
        Get (a copy) of all available verification errors so far.
        """
        return self.verificationErrors[:]  # return a copy!

    def __call__(self, command, target, value=None, **kw):
        """
        Make an actual call to a Selenium action method.
        Examples for methods are 'verifyText', 'assertText', 'waitForText', etc., so methods that are
        typically available in the Selenium IDE.
        Most methods are dynamically created through decorator functions (from 'wd_SEL*-methods) and hence are
        dynamically looked up in the class dictionary.
        """
        if self.wait:
            self.wait = False
        else:
            self.driver.implicitly_wait(0)
        try:
            method = getattr(self, command)
        except AttributeError:
            raise NotImplementedError('no proper function for sel command "%s" implemented' % command)
        return method(target, value, **kw)

    def _importUserFunctions(self):
        """
        Import user functions from module userfunctions. 
        Each function in module userfunction (excluding the ones starting with "_") has to take 
        3 arguments: SeleniumDriver instance, target string, value string. Wrap these function 
        by the decorator function "seleniumcommand" and add them as bound methods. 
        """
        try:
            import userfunctions
            funcNames = [key for (key, value) in userfunctions.__dict__.iteritems() \
                         if isinstance(value, types.FunctionType) and not key.startswith("_")]
            for funcName in funcNames:
                newBoundMethod = new.instancemethod(seleniumcommand(getattr(userfunctions, funcName)), self, SeleniumDriver)
                setattr(self, funcName, newBoundMethod)
            logging.info("User functions: " + ", ".join(funcNames))
        except ImportError:
            logging.info("Using no user functions")
        

    sel_var_pat = re.compile(r'\${([\w\d]+)}')
    def _expandVariables(self, s):
        """
        Expand variables contained in selenese files.
        Multiple variables can be contained in a string from a selenese file. The format is ${<VARIABLENAME}.
        Those are replaced from self.storedVariables via a re.sub() method.
        """
        return self.sel_var_pat.sub(lambda matchobj: self.storedVariables[matchobj.group(1)], s)
    
    
    def setTimeoutAndPoll(self, timeout, poll):
        """
        Set attributes for commands starting with 'waitFor'. This is done initially.
        Attribute 'wait_for_timeout' specifies the time until a waitFor command will time out in milliseconds.
        Attribute 'poll' specifies the time until the function inside a waitFor command is repeated in seconds.
        Attribute 'num_repeats' specifies the number of times the function inside a waitFor command is repeated.
        """
        self.wait_for_timeout = timeout
        self.poll = poll
        self.num_repeats = int(timeout / 1000 / poll)


    ########################################################################################################
    # The actual translations from selenium-to-webdriver commands

    ###
    # Section 1: Interactions with the browser
    ###

    @seleniumcommand
    def open(self, target, value=None):
        """
        Open a URL in the browser
        @param target: URL (string)
        @param value: <not used>
        """
        self.driver.get(self.base_url + target)

    @seleniumcommand
    def clickAndWait(self, target, value=None):
        """
        Click onto a HTML target (e.g. a button) and wait until the browser receives a new page
        @param target: a string determining an element in the HTML page
        @param value:  <not used>
        """
        self.wait = True
        self.driver.implicitly_wait(self.wait_for_timeout / 1000)
        self._find_target(target).click()
	

    @seleniumcommand
    def click(self, target, value=None):
        """
        Click onto a HTML target (e.g. a button)
        @param target: a string determining an element in the HTML page
        @param value:  <not used>
        """
	self.wait = True
        self.driver.implicitly_wait(self.wait_for_timeout / 1000)
        self._find_target(target).click()

    @seleniumcommand
    def select(self, target, value):
        """
        Select an option of a select box.
        @param target: a element locator pointing at a select element
        @param value: an option locator which points at an option of the select element
        Option locators can have the following formats:
        label=labelPattern: matches options based on their labels, i.e. the visible text. (This is the default.)
            example: "label=regexp:^[Oo]ther"
        value=valuePattern: matches options based on their values.
            example: "value=other"
        id=id: matches options based on their ids.
            example: "id=option1"
        index=index: matches an option based on its index (offset from zero).
            example: "index=2"
        """
        target_elem = self._find_target(target)
        tag, tvalue = self._tag_and_value(value)
        select = Select(target_elem)
        if tag in ['label', None]:
            tvalue = self._matchOptionText(target_elem, tvalue)
            select.select_by_visible_text(tvalue)
        elif tag == 'value':
            tvalue = self._matchOptionValue(target_elem, tvalue)
            select.select_by_value(tvalue)
        elif tag == 'id':
            option = target_elem.find_element_by_id(tvalue)
            select.select_by_visible_text(option.text)
        elif tag == 'index':
            select.select_by_index(int(tvalue))
        else:
            raise UnexpectedTagNameException("Unknown option locator tag: " + tag)

	
    def _matchOptionText(self, target, tvalue):
        for option in target.find_elements_by_xpath("*"):
            text = option.text
            if self._matches(tvalue, text):
                return text
        return tvalue
    
    def _matchOptionValue(self, target, tvalue):
        for option in target.find_elements_by_xpath("*"):
            value = option.get_attribute("value")
            if self._matches(tvalue, value):
                return value
        return tvalue
        
    @seleniumcommand
    def type(self, target, value):
        """
        Type text into an input element.
        @param target: an element locator
        @param value: the text to type
        """
        target_elem = self._find_target(target)
        target_elem.clear()
        target_elem.send_keys(value)
        
  
    @seleniumcommand
    def check(self, target, value=None):
        """
        Check a toggle-button (checkbox/radio).
        @param target: an element locator
        @param value: <not used>
        """
        target_elem = self._find_target(target)
        if not target_elem.is_selected():
            target_elem.click()

    @seleniumcommand
    def uncheck(self, target, value=None): 
        """
        Uncheck a toggle-button (checkbox/radio).
        @param target: an element locator
        @param value: <not used>
        """
        target_elem = self._find_target(target)
        if target_elem.is_selected():
            target_elem.click()


    @seleniumcommand
    def mouseOver(self, target, value=None):
        """
        Simulate a user moving the mouse over a specified element.
        @param target: an element locator
        @param value: <not used>
        """
        target_elem = self._find_target(target)
	    # Action Chains will not work with several Firefox Versions. Firefox Version 10.2 should be ok.
        ActionChains(self.driver).move_to_element(target_elem).perform()

  
    @seleniumcommand
    def mouseOut(self, target, value=None):
        """
        Simulate a user moving the mouse away from a specified element.
        @param target: an element locator
        @param value: <not used>
        """
        target_elem = self._find_target(target)
        actions = ActionChains(self.driver)
        actions.move_to_element(target_elem)
        actions.move_by_offset(target_elem.size["width"] / 2 + 1, 0).perform()
        

    @seleniumcommand
    def waitForPopUp(self, target, value):
        """
        Wait for a popup window to appear and load up.
        @param target: the JavaScript window "name" of the window that will appear (not the text of the title bar).
        A target which is unspecified or specified as "null" is not supported currently.
        @param value: the timeout in milliseconds, after which the function will raise an error. If this value 
        is not specified, the default timeout will be used. See the setTimeoutAndPoll function for the default timeout.
        """
        # value allows custom timeout
    	timeout = self.wait_for_timeout if not value else int(value)
    	num_repeats = int(timeout / 1000 / self.poll) 
    	if target in ("null", "0"):
                raise NotImplementedError('"null" or "0" are currently not available as pop up locators')
        for i in range(num_repeats):
            try:
                self.driver.switch_to_window(target)
                self.driver.switch_to_window(0)
                break
            except NoSuchWindowException:
                time.sleep(self.poll)
        else:
            raise NoSuchWindowException("Timed out after %d ms" % timeout)

    
    @seleniumcommand
    def selectWindow(self, target, value=None):
        """
        Select a popup window using a window locator. Once a popup window has been selected, all commands go to that window. 
        To select the main window again, use null as the target or leave it empty. The only locator option which is supported currently
        is 'name=' which finds the window using its internal JavaScript "name" property.
        Not yet supported are: 'title' and 'var'. The IDE has sophisticated routine for missing locator option which will most
        likely not be implemented.
        @param target: the JavaScript window ID of the window to select
        @param value: <not used>
        """
        ttype, ttarget = self._tag_and_value(target)
        if ttarget in ['null', '']:
            self.driver.switch_to_window(self.driver.window_handles[0])
        elif ttype == 'name':
            self.driver.switch_to_window(ttarget)
        elif ttype in ['title']:
            for window in self.driver.window_handles:
                self.driver.switch_to_window(window)
                if self.driver.find_element_by_xpath("//title").text == ttarget:
                    break
        else:
	    raise NotImplementedError('No way to find the window: use "name" or "title" locators of specify target as "null"')
	    
    @seleniumcommand	
    def selectPopUp(self, target, value=None):
    	"""
    	Alias for selectWindow.
    	"""
        self.selectWindow(target, value)
    
    @seleniumcommand
    def selectFrame(self, target, value=None):
        """
        Select a frame within the current window. (You may invoke this command multiple times to select nested frames.) 
        You can also select a frame by its 0-based index number; select the first frame with "0", or the third frame 
        with "2". To select the top frame, you may use "relative=top". Not yet supported is "relative=parent".
        @param target: an element locator identifying a frame or iframe.
        @param value: <not used>
        """
        if target.startswith('relative='):
            if target[9:] == 'top':
                self.driver.switch_to_default_content()
            elif target[9:] == 'parent':
                raise NotImplementedError('Parent frames can not be located')
            else:
                raise NoSuchFrameException
        else:
            try:
                frame = int(target)
            except (ValueError, TypeError):
                frame = self._find_target(target)
            self.driver.switch_to_frame(frame)
    ###
    # Section 2: All wd_SEL*-statements (from which all other methods are created dynamically via decorators)
    ###
     
    def wd_SEL_TextPresent(self, target, value=None):
        """
        Verify that the specified text pattern appears somewhere on the page shown to the user.
        @param target: a pattern to match with the text of the page 
        @param value: <not used>
        @return: true if the pattern matches the text, false otherwise
        """
        text = html2text(self.driver.page_source)
        return True, self._isContained(target, text)
   
    def wd_SEL_ElementPresent(self, target, value=None):        
        """
        Verify that the specified element is somewhere on the page. Catch a NoSuchElementException in order to return a result.
        @param target: an element locator
        @param value: <not used>
        @return: true if the element is present, false otherwise
        """
        try:
            self._find_target(target)
            return True, True
        except NoSuchElementException:
            return True, False

  
    def wd_SEL_Attribute(self, target, value):
        """
        Get the value of an element attribute.
        @param target: an element locator followed by an @ sign and then the name of the attribute, e.g. "foo@bar"
        @param value: the expected value of the specified attribute
        @return: the value of the specified attribute
        """  
        target, sep, attr = target.rpartition("@")
        attrValue = self._find_target(target).get_attribute(attr)
        if attrValue is None:
            raise NoSuchAttributeException
        return value, attrValue.strip()
    
     
    def wd_SEL_Text(self, target, value):
        """
        Get the text of an element. This works for any element that contains text.
        @param target: an element locator
        @param value: the expected text of the element
        @return: the text of the element
        """ 
        return value, self._find_target(target).text.strip()
    
    
    def wd_SEL_Value(self, target, value):
        """
        Get the value of an input field (or anything else with a value parameter).
        @param target: an element locator
        @param value: the expected element value
        @return: the element value
        """    
        return value, self._find_target(target).get_attribute("value").strip()
    

    def wd_SEL_XpathCount(self, target, value):
        """
        Get the number of nodes that match the specified xpath, e.g. "//table" would give the number of tables.
        @param target: an xpath expression to locate elements
        @param value: the number of nodes that should match the specified xpath
        @return: the number of nodes that match the specified xpath
        """      
        count = len(self.driver.find_elements_by_xpath(target))
        return int(value), count

  
    def wd_SEL_Alert(self, target, value=None):
        """
        Retrieve the message of a JavaScript alert generated during the previous action, or fail if there are no alerts. 
        Getting an alert has the same effect as manually clicking OK. If an alert is generated but you do not consume it 
        with getAlert, the next webdriver action will fail.
        @param target: the expected message of the most recent JavaScript alert
        @param value: <not used>
        @return: the message of the most recent JavaScript alert
        """
        alert = Alert(self.driver)
        text = alert.text.strip() 
        alert.accept()
        return target, text
    
    
    def wd_SEL_Confirmation(self, target, value=None):
        """
        Webdriver gives no opportunity to distinguish between alerts and confirmations.
        Thus they are handled the same way here, although this does not reflect the exact behavior of the IDE
        """
        return self.wd_SEL_Alert(target, value)
   
  
    def wd_SEL_Table(self, target, value):
        """
        Get the text from a cell of a table. The cellAddress syntax is tableLocator.row.column, where row and column start at 0.
        @param target: a cell address, e.g. "css=#myFirstTable.2.3"
        @param value: the text which is expected in the specified cell.
        @return: the text from the specified cell
        """ 
        target, row, column = target.rsplit(".", 2)
        table = self._find_target(target)
        rows = []
        # collect all rows  from the possible table elements in the needed order
        for tableElem in ['thead', 'tbody', 'tfoot']:    
            rows.extend(table.find_elements_by_xpath(tableElem + '/*'))
        # get the addressed child element of the addressed row    
        cell = rows[int(row)].find_elements_by_xpath('*')[int(column)]
        return value, cell.text.strip()
    
    ################# Some helper Functions ##################


    def _tag_and_value(self, target):
        """
    	Get the tag of an element locator to identify its type.
        @param target: an element locator
        @return: an element locator splited into its tag and value.
        # e.g. element locator -> tag, value (all locators pointing at the same node) 
        # 1 css=td.f_transfectionprotocol -> css, td.f_transfectionprotocol, 
        # 2 xpath=//td[@id='f_transfectionprotocol'] -> xpath, //td[@id='f_transfectionprotocol'] 
        # 3 //td[@id='f_transfectionprotocol'] -> xpath, //td[@id='f_transfectionprotocol']
        # 4 f_transfectionprotocol -> None, f_transfectionprotocol
        # 5 id=f_transfectionprotocol -> id, f_transfectionprotocol
        """
    	if target.startswith('//'):  # Identify an xpath locator missing a tag by looking at the leading tokens. This separate handling saves this locator variant from a split operation which may cut it in two worthless pieces (example 3). 
            tag, value = ('xpath', target) 
        else: # Perform a split for all other locator types to get the tag. If there is no tag, specify it as None. 
            s = target.split('=', 1)
            tag, value = s if len(s) == 2 else (None, target) # Older IDE Versions did not specify an "id" or "name" tag while recording (example 4). We support these non-tag locators because the IDE still does. The ambiguity is easily handled in further processing.
        return tag, value # Unknown tags raise an UnexpectedTagNameException in further processing.
    	
    
    def _find_target(self, target):
        """
        Select and execute the appropriate find_element_* method for an element locator.
        @param target: an element locator
        @return: the webelement instance found by a find_element_* method
        """
        ttype, ttarget = self._tag_and_value(target)
        if ttype == 'css':
            return self.driver.find_element_by_css_selector(ttarget)
        elif ttype == 'xpath':
            return self.driver.find_element_by_xpath(ttarget)
        elif ttype == 'id':
            return self.driver.find_element_by_id(ttarget)
        elif ttype == 'name':
            return self.driver.find_element_by_name(ttarget)
        elif ttype == 'link':
            return self._find_element_by_link_text(ttarget)
        elif ttype == None: 
            try:
                return self.driver.find_element_by_id(ttarget)
            except:
                return self.driver.find_element_by_name(ttarget) 
        else:
            raise UnexpectedTagNameException('no way to find targets "%s"' % target)
        
    
    def _find_element_by_link_text(self, target):
        # 1) exact-tag:
        if target.startswith("exact:"):
            return self.driver.find_element_by_link_text(target[6:])
        # 2) regexp:
        elif target.startswith('regexp:'):
            target = target [7:]
        # 3) glob/ wildcards
        else: 
            if target.startswith("glob:"):
                target = target[5:]
            target = self._translateWilcardToRegex(target)
        # Search by xpath for regexps and wildcards     
        for target_elem in self.driver.find_elements_by_xpath("//a"):
            try:
                text = target_elem.text
                if text == re.match(target, text).group(0):
                    return target_elem
            except:
                pass
        else:
            raise NoSuchElementException
	
	
    def _matches(self, expectedResult, result):
        """
        Try to match a result of a selenese command with its expected result.
        The function performs a plain equality comparison for non-Strings and handles all three kinds of String-match patterns which Selenium defines:
        1) plain equality comparison
        2) exact: a non-wildcard expression
        3) regexp: a regular expression
        4) glob: a (possible) wildcard expression. This is the default (fallback) method if 1), 2) and 3) don't apply
        see: http://release.seleniumhq.org/selenium-remote-control/0.9.2/doc/dotnet/Selenium.html    
        @param expectedResult: the expected result of a selenese command
        @param result: the actual result of a selenese command
        @return: true if matches, false otherwise
        """
        # 1) equality expression (works for booleans, integers, etc)
        if type(expectedResult) not in [str, unicode]:
            return expectedResult == result
        # 2) exact-tag:
        elif expectedResult.startswith("exact:"):
            return result == expectedResult[6:]
        # 3) regexp
        elif expectedResult.startswith('regexp:'):
            expectedResult = expectedResult[7:]
        # 4) glob/ wildcards
        else:
            if expectedResult.startswith("glob:"):
                expectedResult = expectedResult[5:]
            expectedResult = self._translateWilcardToRegex(expectedResult)
        try:
            return result == re.match(expectedResult, result).group(0)
        except AttributeError:
            return False
	    
    
    
    def _isContained(self, pat, text):
        """
        Verify that a string pattern can be found somewhere in a text.
        This function handles all three kinds of String-match Patterns which Selenium defines. See the _matches method for further details.
        @param pat: a string pattern
        @param text: a text in which the pattern should be found
        @return: true if found, false otherwise
        """
        pat = pat.replace("...", "")
        # 1) regexp
        if pat.startswith('regexp:'):
            return re.search(pat[7:], text) is not None
        # 2) exact-tag:
        elif pat.startswith("exact:"):
            return pat[6:] in text
        # 3) glob/ wildcards
        else:
            if pat.startswith("glob:"):
                pat = pat[5:]
            pat = self._translateWilcardToRegex(pat)
            return re.search(pat, text) is not None
        
    def _translateWilcardToRegex(self, wc):
        """
        Translate a wildcard pattern into in regular expression (in order to search with it in Python).
        Note: Since the IDE wildcard expressions do not support bracket expressions they are not handled here.
        @param wc: a wildcard pattern
        @return: the translation into a regular expression.
        """
        # escape metacharacters not used in wildcards
        metacharacters = ['.', '$','|','+','(',')', '[', ']']
        for char in metacharacters:
            wc = wc.replace(char, '\\' + char)
        # translate wildcard characters $ and *
        wc = re.sub(r"(?<!\\)\*", r".*", wc)
        wc = re.sub(r"(?<!\\)\?", r".", wc)
        return wc
    
    
