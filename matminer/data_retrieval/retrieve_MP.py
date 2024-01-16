import pandas as pd

# from pymatgen.ext.matproj import MPRester, MPRestError
from mp_api.client import MPRester, MPRestError

from matminer.data_retrieval.retrieve_base import BaseDataRetrieval

__author__ = [
    "Saurabh Bajaj <sbajaj@lbl.gov>",
    "Alireza Faghaninia <alireza.faghaninia@gmail.com>",
    "Anubhav Jain <ajain@lbl.gov>",
]


class MPDataRetrieval(BaseDataRetrieval):
    """
    Retrieves data from the Materials Project database.

    If you use this data retrieval class, please additionally cite:

    Ong, S.P., Cholia, S., Jain, A., Brafman, M., Gunter, D., Ceder, G.,
    Persson, K.A., 2015. The Materials Application Programming Interface
    (API): A simple, flexible and efficient API for materials data based on
    REpresentational State Transfer (REST) principles. Computational
    Materials Science 97, 209–215.
    https://doi.org/10.1016/j.commatsci.2014.10.037

    """

    def __init__(self, api_key=None):
        """
        Args:
            api_key: (str) Your Materials Project API key, or None if you've
                set up your pymatgen config.
        """
        if api_key:
            self.mprester = MPRester(api_key=api_key)
        else:
            self.mprester = MPRester()

    def api_link(self):
        return "https://materialsproject.org/wiki/index.php/The_Materials_API"

    def get_dataframe(self, criteria, properties):
        """
        Gets data from MP in a dataframe format. See api_link for more details.

        Args:
            criteria (dict): the same as in get_data
            properties ([str]): the same properties supported as in get_data

        Returns (pandas.Dataframe):
        """
        docs = self.get_data(criteria=criteria, properties=properties)
        data = {}
        for key in properties:
            data[key] = [doc.__dict__[key] for doc in docs]
        df = pd.DataFrame(data)
        return df

    def get_data(self, criteria, properties):
        """
        Args:
            criteria: (dict) see mp_api.client.MPRester.materials.summary.search()
                for a detailed description. Example {"band_gap": [0.5, 3],
                "theoretical" : False} where key is arguement name of search() and
                value of the dictionary are the respective values.

            properties: (list) see mp_api.client.MPRester.materials.summary.search()
                for a description of this parameter. Example: ["formula",
                "formation_energy_per_atom"]. Available fields or properties include
                are listed in MPRester(MAPI_KEY).materials.summary.available_fields

        Returns ([dict]):
            a list of jsons that match the criteria and contain properties
        """

        data = self.mprester.materials.summary.search(**criteria, fields=properties, all_fields=False)
        return data

    def citations(self):
        return [
            "@article{Jain2013,"
            "doi = {10.1063/1.4812323},"
            "url = {https://doi.org/10.1063/1.4812323},"
            "year = {2013},"
            "month = jul,"
            "publisher = {{AIP} Publishing},"
            "volume = {1},"
            "number = {1},"
            "pages = {011002},"
            "author = {Anubhav Jain and Shyue Ping Ong and Geoffroy Hautier and Wei "
            "Chen and William Davidson Richards and Stephen Dacek and "
            "Shreyas Cholia and Dan Gunter and David Skinner and "
            "Gerbrand Ceder and Kristin A. Persson},"
            "title = {Commentary: The Materials Project: A materials genome "
            "approach to accelerating materials innovation},"
            "journal = {{APL} Materials}"
            "}",
            "@article{Ong2015,"
            "doi = {10.1016/j.commatsci.2014.10.037},"
            "url = {https://doi.org/10.1016/j.commatsci.2014.10.037},"
            "year = {2015},"
            "month = feb,"
            "publisher = {Elsevier {BV}},"
            "volume = {97},"
            "pages = {209--215},"
            "author = {Shyue Ping Ong and Shreyas Cholia and Anubhav Jain "
            "and Miriam Brafman and Dan Gunter and Gerbrand Ceder and Kristin A. Persson},"
            "title = {The Materials Application Programming Interface ({API}): "
            "A simple,  flexible and efficient {API} for materials data based on "
            "{REpresentational} State Transfer ({REST}) principles},"
            "journal = {Computational Materials Science}"
            "}",
        ]
