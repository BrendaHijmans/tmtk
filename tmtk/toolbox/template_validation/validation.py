import logging

logger = logging.getLogger(' validator')


class Validator:

    def __init__(self, df):
        """
        Creates object Validator that runs common validation steps for the loaded sheet or file.

        :param self.df: one of the sheets (or files referred to) in the template in a pandas data frame
        :param self.is_valid: boolean tracking if data passes validation steps
        :param self.can_continue: boolean tracking if validation steps can continue without issues in next tests
        :param self.n_comment_lines: stores index of first line in data sheet that is not a comment
        :param self.tests_to_run: list containing function calls for data validation tests
        """
        self.df = df
        self.n_comment_lines = 0
        self.is_valid = True
        self.can_continue = True
        self.mandatory_columns = {}

    def after_comments(self):
        """Determines where initial text with comments (instructions for data owner) ends, saves tree_df without
        these comments to continue checking and assigns column names.
        """
        while str(self.df.iloc[self.n_comment_lines, 0]).startswith('#'):
            self.n_comment_lines += 1

        header = self.df.iloc[self.n_comment_lines]
        self.df = self.df[self.n_comment_lines + 1:]
        self.df = self.df.rename(columns=header)

    def no_hashtag_or_backslash(self):
        """Iterate through df and check for # and \ within data. When one of these characters is detected
        set self.is_valid = False and give error message with their location column name and row number.
        """
        forbidden_chars = ('#', '\\')

        for col_name, series in self.df.iteritems():
            for idx, value in series.iteritems():
                if any((c in forbidden_chars) for c in str(value)):
                    self.is_valid = False
                    logger.error(" Detected '#' or '\\' at column: '{}', row: {}.".format(col_name, idx + 1))

    def mandatory_columns(self):
        """ Checks whether mandatory columns are present. If one or more mandatory columns are absent self.can_continue
        is set to False and validation of this sheet cannot go on.
        """
        missing_columns = [col_name for col_name in self.mandatory_columns if col_name not in
                           self.df.columns]

        if missing_columns:
            self.can_continue = False
            self.is_valid = False
            logger.error(' Missing the following mandatory columns:\n\t' + '\n\t'.join(missing_columns))
