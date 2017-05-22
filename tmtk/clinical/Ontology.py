import os
import pandas as pd
import json

from ..utils import FileBase, Exceptions, Mappings, MessageCollector, word_map_diff
from ..params import ClinicalParams


class OntologyMapping(FileBase):
    """
    Class representing the ontology file.
    """

    def __init__(self, params=None):
        """
        Initialize by giving a params object.

        :param params: `tmtk.ClinicalParams`.
        """

        self.params = params

        if not isinstance(params, ClinicalParams):
            raise Exceptions.ClassError(type(params))
        elif params.get('ONTOLOGY_MAP_FILE'):
            self.path = os.path.join(params.dirname, params.ONTOLOGY_MAP_FILE)
        else:
            self.path = os.path.join(params.dirname, 'ontology_mapping_file.txt')
            self.params.__dict__['ONTOLOGY_MAP_FILE'] = os.path.basename(self.path)

        super().__init__()

    # def build_index(self, df=None):
    #     """
    #     Build and sort multi-index for dataframe based on filename and
    #     column number columns. If no df parameter is not set, build index
    #     for self.df.
    #
    #     :param df: `pd.DataFrame`.
    #     :return: `pd.DataFrame`.
    #     """
    #     # pass
    #     # if not isinstance(df, pd.DataFrame):
    #     #     df = self.df
    #     # df.set_index(list(df.columns[[0, 1]]), drop=False, inplace=True)
    #     # df.sort_index(inplace=True)
    #     return df
    #
    # def create_df(self):
    #     """
    #     Create `pd.DataFrame` with a correct header.
    #
    #     :return: `pd.DataFrame`.
    #     """
    #     pass
    #     # df = pd.DataFrame(dtype=str, columns=Mappings.word_mapping_header)
    #     # df = self.build_index(df)
    #     # return df

    def as_json(self):
        ontology_terms = self.df.apply(lambda x: OntologyTerm(x[2], x[3], x[4], str(x[5]).split(',')),
                                       axis=1)
        return OntologyTree(ontology_terms).json()


class OntologyTerm:
    def __init__(self, code, label, uri, parents=None):
        self.code = code
        self.label = label
        self.uri = uri
        self.parents = parents
        self.children = []

    def json(self):
        return {'text': self.label,
                'data':
                    {'uri': self.uri,
                     'code': self.code,
                     },
                'children': [child.json() for child in self.children]
                }

    def __repr__(self):
        return "{}: {}".format(self.label,
                               self.children)


class OntologyTree:
    def __init__(self, ontology_list=None):
        self.anchors = list(ontology_list)
        self.create_hierarchy()

    def _recurse_children(self, children, code):
        for term in children:
            if term.code == code:
                return term
            in_children = self._recurse_children(term.children, code)
            if in_children:
                return in_children

    def _find_code(self, code):
        term = self._recurse_children(self.anchors, code)
        return term

    def _iterate_hierarchy(self):
        changed = False
        for branch in self.anchors:
            for parent_code in branch.parents:

                parent = self._find_code(parent_code)

                if not parent:
                    continue

                changed = True
                try:
                    self.anchors.remove(branch)
                except ValueError:
                    # Double parents
                    pass
                parent.children.append(branch)
        return changed

    def create_hierarchy(self):
        while self._iterate_hierarchy():
            pass

    def json(self):
        return json.dumps([node.json() for node in self.anchors])