import argparse
import demographic_report
import os

"""
This code was written by Ben hillel from mahzor 44, and its purpose is to create a demographic report 
from the sociometry products using the sociogram as a base for the demografic groups.

Before running this code:
    make sure that you have the sociometry products and the sociogram of the same mahzor. and 
    update the DATA_COLUMNS and NAME_COLUMN to match the columns in the sociogram that contain the demographic data and the 
    names of the cadets respectively.

Example for input parameters:
    --title "רמה מחזורית" --sociometry-path "C:/Work/Haaraha/Sociometry/44_Semester_E/output/stats_excel.xlsx" 
    --sociogram-path "dat/sociogram_md_sheet.xlsx" --filter-column 5 --filter-name 'רמה מחלקתית'
"""

DATA_COLUMNS = [4, 5, 6, 7, 8, 9]  # column numbers in the sociogram that contain the demographic data
NAME_COLUMN = 10  # column number in the sociogram that contains the names (name - number) of the cadets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, default="רמה מחזורית", help="the title of the main report")
    parser.add_argument('--sociometry-path', type=str, help="path to the stats.xlsx from the sociometry products")
    parser.add_argument('--sociogram-path', type=str, help="path to the sociogram excel of same mahzor")
    parser.add_argument('--filter-column', type=int, default=None, help="the column number in the sociogram that we want to create unique reports for each value in it. for example mahlaka")
    parser.add_argument('--filter-name', type=str, default="רמת מחלקה", help="the name that we want the title of the sub report's to be")
    parser.add_argument('--old-socio-path', type=str, default=None, help="path to the last year's stats.xlsx from the sociometry products")
    parser.add_argument('--relative-paths', action='store_true', default=False, help="consider all of the paths provided as relative to this location")
    args = parser.parse_args()

    # check that we have the required arguments
    if not args.sociometry_path or not args.sociogram_path:
        raise ValueError("sociometry-path and sociogram-path are required arguments. please provide them (you can use --help for more information)")

    relative_path = os.getcwd()
    if args.relative_paths:
        sociometry_path = os.path.join(relative_path, args.sociometry_path)
        sociogram_path = os.path.join(relative_path, args.sociogram_path)
        old_socio_path = os.path.join(relative_path, args.old_socio_path)
    else:
        sociometry_path = args.sociometry_path
        sociogram_path = args.sociogram_path
        old_socio_path = args.old_socio_path

    demographic_report.create_report(args.title, sociometry_path, sociogram_path,
                                     NAME_COLUMN, DATA_COLUMNS, old_socio_path,
                                     args.filter_column, args.filter_name)



