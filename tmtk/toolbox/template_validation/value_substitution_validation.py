import logging
import os
import pandas as pd

from .validation import Validator

logger = logging.getLogger(" Value substitution sheet")
logger.setLevel(logging.DEBUG)


class ValueSubstitutionValidator(Validator):

    def __init__(self, df, source_dir, template):
        """Creates object ValueSubstitutionValidator that runs validation tests on value substitution sheet and
        gives user-friendly error messages.

        :param self.source_dir: directory containing the template and possible other source files
        :param self.template: the loaded template
        :param self.tests_to_run: list containing function calls for data validation tests
        """
        Validator.__init__(self, df)
        self.source_dir = source_dir
        self.template = template
        self.tests_to_run = (test for test in
                             [self.after_comments,
                              self.mandatory_columns,
                              self.data_in_columns,  # maybe delete this method
                              self.no_hashtag_or_backslash
                              ])

        self.mandatory_columns = {'Sheet name/File name', 'Column name', 'From value', 'To value'}

        self.validate_sheet()

    def validate_sheet(self):
        """ Iterates over tests_to_run while no issues are encountered that would interfere with following
        validation steps
        """
        while self.can_continue:
            next_test = next(self.tests_to_run, None)
            if next_test:
                next_test()
            else:
                return

    def data_in_columns(self):
        """ Checks whether there is data in the columns. If there is no data, the next validation steps are not
        executed.
        """
        print(1)
        if len(self.df) == 0:
            self.can_continue = False
