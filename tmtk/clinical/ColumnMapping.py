import os
import pandas as pd

from ..arborist import call_boris
from ..utils import FileBase, Exceptions, Mappings, path_converter, path_join, CPrint
from ..params import ClinicalParams
from .DataFile import DataFile


class ColumnMapping(FileBase):
    """
    Class with utilities for the column mapping file for clinical data.
    Can be initiated with either a path to column mapping file, or a clinical params file object.
    """
    def __init__(self, params=None):

        self.params = params

        if not isinstance(params, ClinicalParams):
            raise Exceptions.ClassError(type(params))
        elif params.__dict__.get('COLUMN_MAP_FILE'):
            self.path = os.path.join(params.dirname, params.COLUMN_MAP_FILE)
        else:
            self.path = os.path.join(params.dirname, 'column_mapping_file.txt')
            self.params.__dict__['COLUMN_MAP_FILE'] = os.path.basename(self.path)
        super().__init__()

    @property
    def included_datafiles(self):
        """
        List of datafiles included in column mapping file.
        :return: list.
        """
        return list(self.df.ix[:, 0].unique())

    @property
    def ids(self):
        self.build_index()
        return self.df.index

    @staticmethod
    def create_df():
        df = pd.DataFrame(dtype=str, columns=Mappings.column_mapping_header)
        return df

    def call_boris(self):
        self.df = call_boris(self.df)

    def validate(self, verbosity=2):
        pass

    def select_row(self, var_id):
        """
        Select row based on var_id
        :param var_id:
        :param kwargs:
        :return:
        """

        rows = self.df.loc[var_id]

        if isinstance(rows, pd.Series):
            return list(rows)
        elif isinstance(rows, pd.DataFrame):
            raise Exceptions.TooManyValues(rows.shape[0], 1, var_id)

    def get_concept_path(self, var_id):
        row = self.select_row(var_id)
        cp = path_join(row[1], row[3])
        return path_converter(cp)

    @staticmethod
    def _df_mods(df):
        """
        df_mods applies modifications to the dataframe before it is cached.
        :return:
        """
        df.fillna("", inplace=True)
        df.ix[:, 2] = df.ix[:, 2].astype(int)
        return df

    def build_index(self, df=None):
        if not isinstance(df, pd.DataFrame):
            df = self.df
        df.set_index(list(df.columns[[0, 2]]), drop=False, inplace=True)
        df.sortlevel(inplace=True)
        return df

    def append_from_datafile(self, datafile):
        """
        Appends the column mapping file with rows based on datafile column names.
        :param datafile: tmtk.clinical.Datafile object.
        """

        if not isinstance(datafile, DataFile):
            raise TypeError(datafile)

        cols_min_four = [""] * (self.df.shape[1] - 4)
        for i, name in enumerate(datafile.df.columns, 1):
            var_id = (datafile.name, i)
            if self.select_row(var_id):
                CPrint.warn("Skipping {!r}, already in column mapping file.".format(var_id))
                continue

            self.df.loc[var_id] = [datafile.name, datafile.name, i, name] + cols_min_four

        self.build_index()
