from ..params import ParamsBase


class TagsParams(ParamsBase):

    @property
    def mandatory(self):
        return ['TAGS_FILE']

    @property
    def optional(self):
        return []

    def is_viable(self):
        """

        :return: True if both the column mapping file is located, else returns False.
        """
        if self.__dict__.get('TAGS_FILE', None):
            return True
        else:
            return False

