import os
import tmtk.utils as utils
import tmtk


class ColumnMapping:
    """
    Class with utilities for the column mapping file for clinical data.
    Can be initiated with either a path to column mapping file, or a clinical params file object.
    """
    def __init__(self, params=None):
        if params and params.is_viable() and params.datatype == 'clinical':
            self.path = os.path.join(params.dirname, params.COLUMN_MAP_FILE)
        else:
            raise utils.Exceptions.ClassError(type(params), tmtk.ClinicalParams)

    @utils.cached_property
    def df(self):
        return utils.file2df(self.path)

    @property
    def included_datafiles(self):
        """
        List of datafiles included in column mapping file.
        :return: list.
        """
        return list(self.df.ix[:, 0].unique())

    @property
    def concept_paths(self):
        return self.df.apply(lambda x: '{}/{}'.format(x[1], x[3]), axis=1)

    @property
    def ids(self):
        return self.df.apply(lambda x: '{}__{}'.format(x[0], x[2]), axis=1)

    def call_boris(self):
        self.df = utils.call_boris(self.df)

    def write_to(self):
        utils.df2file(self)

    def validate(self, verbosity=2):
        pass

    def get_data_args(self, var_id):
        row = self.df.ix[self.ids == var_id]
        return list(row.values[0, :])  # Returns single row as list.
