import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go

class SocioLinker:
    def __init__(self, sociometric_path: str, sociogram_path: str, sociogram_name_column: int):
        """
        :param sociometric_path: path to the stats.xlsx file of the sociometric data
        :param sociogram_path: path to the sociogram excel file
        :param sociogram_name_column: the column number of the names in the sociogram file
        :param last_year_socio_path: path to the last year sociogram excel file
        """
        # load the stats.xlsx file of the sociometric data
        print(f"loading sociometric data from {sociometric_path}")
        self.sociometric_df = pd.read_excel(sociometric_path)

        # assume that the combined_data.xlsx is in the same folder as the sociometric data
        self.combined_data_df = pd.read_excel(os.path.join(os.path.dirname(sociometric_path), "combined_data.xlsx"))
        # drop all rows with name == "ממוצע"
        self.combined_data_df = self.combined_data_df[self.combined_data_df['name'] != "ממוצע"]
        # drop the "points to conserve" and "points to improve" columns
        self.combined_data_df = self.combined_data_df.drop(columns=["points to conserve", "points to improve"])
        # drop nans
        self.combined_data_df = self.combined_data_df.dropna()

        # load the sociogram data
        self.sociogram_name_column = sociogram_name_column
        self._open_sociogram_data(sociogram_path)


    def _open_sociogram_data(self, sociogram_path: str):
        # 1) Open the sociogram data
        self.sociogram_df = pd.read_excel(sociogram_path)
        name_column = self.sociogram_df.columns[self.sociogram_name_column]
        self.sociogram_df[name_column] = self.sociogram_df[name_column].apply(lambda x: x.split(' - ')[0]).apply(str.strip)

        # 2) check that we have all of the names from the sociogram in the sociometry
        all_names_found = True
        for name in self.sociogram_df[name_column].tolist():
            name = name.strip()
            if not (name in self.sociometric_df["name"].tolist()):
                print(f"the name {name} from sociogram does not appear in sociometry")
                all_names_found = False
        if not all_names_found:
            raise Exception("Not all names found in both files!, its probebly a typo in some of the names between the files (fix it manually)")
        else:
            print("all names found! we can continue")

        # 3) PREPROCCESS
        # remove columns that include the word "בחירה" in them
        self.sociometric_df = self.sociometric_df[self.sociometric_df.columns[~self.sociometric_df.columns.str.contains('בחירה')]]
        # remove columns that include the word "זמן" in them
        self.sociometric_df = self.sociometric_df[self.sociometric_df.columns[~self.sociometric_df.columns.str.contains('זמן')]]

    def get_names_from_info(self, info_column, info_value):
        """
        get the names of the cadets that have a specific value in the info column given
        :param info_column:
        :param info_value:
        :return:
        """
        name_column = self.sociogram_df.columns[self.sociogram_name_column]
        info_column = self.sociogram_df.columns[info_column]
        return self.sociogram_df[self.sociogram_df[info_column] == info_value][name_column].apply(lambda x: x.split(' - ')[0])

    def get_stats_of_cadets(self, cadet_names_ls, category=None):
        all_stats = self.sociometric_df[self.sociometric_df['name'].apply(lambda x: x in cadet_names_ls)]
        if category is None:
            return all_stats
        else:
            return all_stats[all_stats['category'] == category]

    def get_combined_data_of_cadets(self, cadet_names_ls):
        return self.combined_data_df[self.combined_data_df['name'].apply(lambda x: x in cadet_names_ls)]

    def get_value_count_of_column(self, cadet_name_ls, column):
        """
        Returns counts of the values in the specified column for the given list of cadet names.
        :param cadet_name_ls: List of cadet names to filter by
        :param column: Column name for which to count values
        :return: Series containing counts of each value in the column
        """

        # Filter the DataFrame for rows where 'name' is in cadet_name_ls
        filtered_df = self.combined_data_df[self.combined_data_df['name'].isin(cadet_name_ls)]

        # Return the value counts for the specified column
        return filtered_df[column].apply(round).value_counts()


    def get_all_cadets_names(self):
        return self.sociogram_df[self.sociogram_df.columns[self.sociogram_name_column]].tolist()