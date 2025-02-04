from DocxHelper import DocxHelper
from SocioLinker import SocioLinker
import numpy as np
import pandas as pd
import plotly.graph_objects as go


from constants import CATEGORY_NAME_DICT, OUTPUT_PATH, PROFESSIONAL_CATEGORIES, PERSONAL_CATEGORIES


class SocioDemographicReport:
    def __init__(self, title: str, sociometric_path: str, sociogram_path: str, sociogram_name_column: int,
                 last_year_socio_path: str = None):
        self.docx_helper = DocxHelper(title)
        self.title = title
        self.socio_linker = SocioLinker(sociometric_path, sociogram_path, sociogram_name_column)
        if last_year_socio_path is not None:
            print(f"loading last year's data from {last_year_socio_path}")
            self.last_year_socio_linker = SocioLinker(last_year_socio_path, sociogram_path, sociogram_name_column)
        else:
            self.last_year_socio_linker = None

    def do_bar_graph(self, info_column, categories=None, save_name="", axis_range=(2, 6)):
        fig_data = []
        new_info_column = self.socio_linker.sociogram_df.columns[info_column]
        _groups = self.socio_linker.sociogram_df[new_info_column].unique().tolist()

        if categories is None:
            _x_values = self.socio_linker.sociometric_df['category'].unique().tolist()
        else:
            _x_values = categories
        for _group in _groups:
            group_cadet_names = self.socio_linker.get_names_from_info(info_column=info_column, info_value=_group)
            all_stats = self.socio_linker.get_stats_of_cadets(group_cadet_names.tolist())
            _y_vals = [np.mean(all_stats[all_stats['category'] == cat]['mean'].astype(float).tolist()) for cat in _x_values]
            # set the name of this group to be the group + (N=number of cadets in this group)
            _group_name = _group + f" (N={len(group_cadet_names)})"
            # add the bar to the figure with big text on the x axis
            fig_data.append(go.Bar(
                name=_group_name,
                x=[CATEGORY_NAME_DICT[cat] for cat in _x_values],
                y=_y_vals,
                text=[round(a, 2) for a in _y_vals],
                textposition='auto',
                textfont=dict(
                    family="Arial",
                    size=14,
                    color="black"
                )
            ))
        _fig = go.Figure(data=fig_data)
        # set the size of x axis text to be big
        _fig.update_layout(barmode='group', xaxis_tickfont=dict(size=18), yaxis_tickfont=dict(size=18))
        _fig.update_yaxes(range=axis_range)
        # set the labels of the different categories to be big
        _fig.update_layout(yaxis_title="ממוצע", font=dict(
            family="Arial",
            size=18,
            color="black"
        ))
        return _fig

    def do_bar_graph_old(self, info_column, categories=None, save_name="", axis_range=(2, 5)):
        fig_data = []
        new_info_column = self.socio_linker.sociogram_df.columns[info_column]
        _groups = self.socio_linker.sociogram_df[new_info_column].unique().tolist()

        if categories is None:
            _x_values = self.socio_linker.sociometric_df['category'].unique().tolist()
        else:
            _x_values = categories
        for _group in _groups:
            group_cadet_names = self.socio_linker.get_names_from_info(info_column=info_column, info_value=_group)
            all_stats = self.last_year_socio_linker.get_stats_of_cadets(group_cadet_names.tolist())
            _y_vals = [np.mean(all_stats[all_stats['category'] == cat]['mean'].astype(float).tolist()) for cat in _x_values]
            # set the name of this group to be the group + (N=number of cadets in this group)
            _group_name = _group + f" (N={len(group_cadet_names)})"
            # add the bar to the figure with big text on the x axis
            fig_data.append(go.Bar(
                name=_group_name,
                x=[CATEGORY_NAME_DICT[cat] for cat in _x_values],
                y=_y_vals,
                text=[round(a, 2) for a in _y_vals],
                textposition='auto',
                textfont=dict(
                    family="Arial",
                    size=14,
                    color="black"
                )
            ))
        _fig = go.Figure(data=fig_data)
        # set the size of x axis text to be big
        _fig.update_layout(barmode='group', xaxis_tickfont=dict(size=18), yaxis_tickfont=dict(size=18))
        _fig.update_yaxes(range=axis_range)
        # set the labels of the different categories to be big
        _fig.update_layout(yaxis_title="ממוצע", font=dict(
            family="Arial",
            size=18,
            color="black"
        ))
        _fig.update_traces(marker_color='rgba(0,0,0,0)', marker_line_color='black')
        return _fig


    def do_pie_chart(self, info_column, cadet_names=None):
        if cadet_names is None:
            # Take all of the cadets
            cadet_names = self.socio_linker.get_all_cadets_names()
        print(f"doing pie chart for {info_column}")
        counts = self.socio_linker.get_value_count_of_column(cadet_names, info_column)

        # Define a color map for the values 0 to 6
        color_map = {
            0: 'gray',  # Example color
            1: 'purple',
            2: 'blue',
            3: 'green',
            4: 'yellow',
            5: 'orange',
            6: 'red'
        }

        # Create a list of colors in the order of counts.index
        colors = [color_map[i] for i in counts.index]

        # Create the pie chart using the color list
        fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts.values,
                                     marker=dict(colors=colors, line=dict(color='#000000', width=2)))])
        fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20)
        img = fig.to_image(format="png", width=1500, height=500)
        return img


    def filter_sociogram(self, column, value):
        column = self.socio_linker.sociogram_df.columns[column]
        self.socio_linker.sociogram_df = self.socio_linker.sociogram_df[self.socio_linker.sociogram_df[column] == value]
        self.socio_linker.combined_data_df = self.socio_linker.combined_data_df[self.socio_linker.combined_data_df['name'].apply(lambda x: x in self.socio_linker.sociogram_df[self.socio_linker.sociogram_df.columns[self.socio_linker.sociogram_name_column]].tolist())]

    def get_filter_values_sociogram(self, column):
        column = self.socio_linker.sociogram_df.columns[column]
        return self.socio_linker.sociogram_df[column].unique()

    def make_report(self, info_columns):
        images = []
        # add the pie charts of the diversity of the cadets
        for category in CATEGORY_NAME_DICT.keys():
            images.append(self.do_pie_chart(category))
        print(f'created a total of {len(images)} images')
        self.docx_helper.add_histograms_to_table(images, 2)

        images = []
        for category in info_columns:
            pro = self.do_bar_graph(category, categories=PROFESSIONAL_CATEGORIES,
                                    save_name="proffeccional", axis_range=(3, 6))
            per = self.do_bar_graph(category, categories=PERSONAL_CATEGORIES,
                                    save_name='personal', axis_range=(1,3))
            if not (self.last_year_socio_linker is None):
                pro_last = self.do_bar_graph_old(category, categories=PROFESSIONAL_CATEGORIES,
                                    save_name="proffeccional", axis_range=(2, 5))
                per_last = self.do_bar_graph_old(category, categories=PERSONAL_CATEGORIES,
                                    save_name='personal', axis_range=(1,3))
                pro_last.for_each_trace(lambda t: t.update(name=t.name + ' סמסטר שעבר '))
                per_last.for_each_trace(lambda t: t.update(name=t.name + ' סמסטר שעבר '))
                # unify the data
                new_pro = go.Figure(data=pro.data)
                new_per = go.Figure(data=per.data)
                new_pro.add_traces(pro_last.data)
                new_per.add_traces(per_last.data)

                pro = new_pro
                per = new_per
            images.append(pro.to_image(format="png", width=1500, height=500))
            images.append(per.to_image(format="png", width=1500, height=500))

        self.docx_helper.add_histograms(images)

        self.docx_helper.save(OUTPUT_PATH+f"demographic_report_{self.title}.docx")




def main45():
    input_params = {
        'title': f'רמה מחזורית מה',
        'sociometric_path': "C:/Work/Haaraha/Sociometry/45_Semester_C/output/stats_excel.xlsx",
        'sociogram_path': "dat/sociogram_mh_sheet.xlsx",
        'sociogram_name_column': 10,
        'last_year_socio_path': "C:/Work/Haaraha/Sociometry/45_Semester_C/last_year_Excels/stats_excel.xlsx"
    }
    info_columns = [4, 5, 6, 7, 8, 9]
    sd = SocioDemographicReport(**input_params)
    sd.make_report(info_columns)
    for mahlaka in ["עיט", "זאב", "לביא"]:
        input_params = {
            'title': f'רמה מחלקתית – {mahlaka}',
            'sociometric_path' : "C:/Work/Haaraha/Sociometry/45_Semester_C/output/stats_excel.xlsx",
            'sociogram_path' : "dat/sociogram_mh_sheet.xlsx",
            'sociogram_name_column' : 10,
            'last_year_socio_path': "C:/Work/Haaraha/Sociometry/45_Semester_C/last_year_Excels/stats_excel.xlsx"
        }
        info_columns = [4, 5, 6, 7, 8, 9]
        sd = SocioDemographicReport(**input_params)
        sd.filter_sociogram(5, mahlaka)
        sd.make_report(info_columns)

def main46():
    input_params = {
        'title': f'רמה מחזורית מו',
        'sociometric_path': "C:/Work/Haaraha/Sociometry/46_Semester_A/stats_excel.xlsx",
        'sociogram_path': "dat/sociogram_mv_sheet.xlsx",
        'sociogram_name_column': 1
    }
    info_columns = [5, 6, 7, 8, 9, 10]
    sd = SocioDemographicReport(**input_params)
    sd.make_report(info_columns)
    for mahlaka in ["בופור", "רעים", "סופה", "מגן"]:
        input_params = {
            'title': f'רמה מחלקתית – {mahlaka}',
            'sociometric_path' : "C:/Work/Haaraha/Sociometry/46_Semester_A/stats_excel.xlsx",
            'sociogram_path' : "dat/sociogram_mv_sheet.xlsx",
            'sociogram_name_column' : 1
        }
        sd = SocioDemographicReport(**input_params)
        sd.filter_sociogram(6, mahlaka)
        sd.make_report(info_columns)

def main44():
    input_params = {
        'title': f'רמה מחזורית מד',
        'sociometric_path': "C:/Work/Haaraha/Sociometry/44_Semester_E/output/stats_excel.xlsx",
        'sociogram_path': "dat/sociogram_md_sheet.xlsx",
        'sociogram_name_column': 10
    }
    info_columns = [4, 5, 6, 7, 8, 9]
    sd = SocioDemographicReport(**input_params)
    sd.make_report(info_columns)
    for mahlaka in [ "מטה", "סגל ב", "סגל א"]:
        input_params = {
            'title': f'רמה סגלית – {mahlaka}',
            'sociometric_path' : "C:/Work/Haaraha/Sociometry/44_Semester_E/output/stats_excel.xlsx",
            'sociogram_path' : "dat/sociogram_md_sheet.xlsx",
            'sociogram_name_column' : 10
        }
        sd = SocioDemographicReport(**input_params)
        sd.filter_sociogram(5, mahlaka)
        sd.make_report(info_columns)

def create_report(title: str, sociometric_path: str, sociogram_path: str,
                  sociogram_name_column: int, info_columns: list, last_year_socio_path=None,
                  filter_column=None, filter_title: str = None):
    # first create the report for everyone
    # set the input parameters
    input_params = {
        'title': title,
        'sociometric_path': sociometric_path,
        'sociogram_path': sociogram_path,
        'sociogram_name_column': sociogram_name_column,
    }
    if last_year_socio_path is not None:
        input_params['last_year_socio_path'] = last_year_socio_path
    print("="*33)
    print("="*5 + "Creating general report" + "="*5)
    print("="*33)
    sd = SocioDemographicReport(**input_params)
    sd.make_report(info_columns)

    # if we want to create a report for a specific group (filter_column not None), than
    # we repeat the process for each group
    if filter_column is not None:
        filter_values = sd.get_filter_values_sociogram(filter_column)
        if filter_title is not None:
            title = filter_title
        print("="*39)
        print("="*5 + "Creating report for subgroups" + "="*5)
        print(filter_values)
        print("="*39)
        for filter_value in filter_values:
            print(f"\n=== Creating report for {filter_value} ===\n")
            input_params = {
                'title': f'{title} - {filter_value}',
                'sociometric_path': sociometric_path,
                'sociogram_path': sociogram_path,
                'sociogram_name_column': sociogram_name_column,
            }
            if last_year_socio_path is not None:
                input_params['last_year_socio_path'] = last_year_socio_path
            sd = SocioDemographicReport(**input_params)
            sd.filter_sociogram(filter_column, filter_value)
            sd.make_report(info_columns)




if __name__ == "__main__":
    pass
