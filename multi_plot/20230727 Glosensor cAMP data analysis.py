import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from common import common_tools as ct


def position_to_treatment(row):
    """Define treatment according to the position."""

    if row['position'].endswith('03') :
        return 'OCN'
    elif row['position'].endswith('04') :
        return 'IN-568'
    elif row['position'].endswith('05') :
        return 'IN-569'
    elif row['position'].endswith('06') :
        return 'IN-570'
    elif row['position'].endswith('07') :
        return 'IN-579'
    elif row['position'].endswith('08') :
        return 'IN-580'
    elif row['position'].endswith('09') :
        return 'IN-582'
    elif row['position'].endswith('10') :
        return 'IN-600'
    elif row['position'].endswith('11') :
        return 'IN-629'
    elif row['position'].endswith('12') :
        return 'IN-630'    
    elif row['position'].endswith('13') :
        return 'HBSS'
    elif row['position'].endswith('14') :
        return 'GLP-1'
    elif row['position'].endswith('15') :
        return 'forskolin'
    elif row['position'].endswith('16') :
        return 'glucose'    
    elif row['position'].endswith('17') :
        return 'indoxyl sulfate'

                                
def position_to_conc(row):
    """Define concentration according to the position."""
    if row['position'].startswith('D') or row['position'].startswith('H') or row['position'].startswith('L'):
        return '20 uM'
    elif row['position'].startswith('E') or row['position'].startswith('I') or row['position'].startswith('M'):
        return '2 uM'
    elif row['position'].startswith('F') or row['position'].startswith('J') or row['position'].startswith('N'):
        return '0.2 uM'
    
    elif row['position'] == 'C03' or row['position'] =='G03' or row['position'] == 'K03' :
        return '28 uM'
    elif row['position'] == 'C04' or row['position'] =='G04' or row['position'] == 'K04' :
        return '170 uM'
    elif row['position'] == 'C05' or row['position'] =='G05' or row['position'] == 'K05' :
        return '290 uM'
    elif row['position'] == 'C06' or row['position'] =='G06' or row['position'] == 'K06' :
        return '257 uM'
    elif row['position'] == 'C07' or row['position'] =='G07' or row['position'] == 'K07' :
        return '363 uM'    
    elif row['position'] == 'C08' or row['position'] =='G08' or row['position'] == 'K08' :
        return '248 uM'
    elif row['position'] == 'C09' or row['position'] =='G09' or row['position'] == 'K09' :
        return '200 uM'
    elif row['position'] == 'C10' or row['position'] =='G10' or row['position'] == 'K10' :
        return '312 uM'
    elif row['position'] == 'C11' or row['position'] =='G11' or row['position'] == 'K11' :
        return '156 uM'
    elif row['position'] == 'C12' or row['position'] =='G12' or row['position'] == 'K12' :
        return '38.2 uM'
    
    elif row['position'].endswith('13') :
        pass
    
    elif row['position'] == 'C14' or row['position'] =='G14' or row['position'] == 'K14' :
        return '2 uM'
    elif row['position'] == 'C15' or row['position'] =='G15' or row['position'] == 'K15' :
        return '20 uM'
    elif row['position'] == 'C16' or row['position'] =='G16' or row['position'] == 'K16' :
        return '200 uM'
    elif row['position'] == 'C17' or row['position'] =='G17' or row['position'] == 'K17' :
        return '200 uM'
#%%

# create DataFrame as df
def load_and_process_data(file_info) -> pd.DataFrame:
    """load data from Excel file and inport as a DataFrame, then output as a melted DataFrame"""
    
    df = pd.read_excel(file_info['file_path'],
                    file_info['sheet_name'],
                    header = 38,
                    skipfooter = 7)

    df = df.drop(['Time [s]', 'Temp. [°C]'], axis=1)
    m_df = df.melt(id_vars = ['Cycle No'],     # keep the columns as an id variable
                var_name = 'position',      # variable's name
                value_name ='luminescence') # value's name

    m_df['treatment'] = m_df.apply(position_to_treatment, axis=1)
    m_df['concentration'] = m_df.apply(position_to_conc, axis=1)
    return m_df

def plot_facetgrid(m_df: pd.DataFrame, file_info):
    """Plot FacetGrid and save the figure."""
    grid = sns.FacetGrid(m_df,                      # data based on the dataframe 'm_df'
                        col = 'treatment',          # determine the index 'treatment' to separate the plotting
                        col_wrap = 3,               # wrap the column variable at this width
                        aspect = 1.3,               # aspect to determine the width
                        hue = 'concentration',      # determine the index to plot separately
                        sharey = False,             # not to share the same y axis, but independently determine the y axis
                        )

    grid.map(sns.lineplot, 'Cycle No', 'luminescence')
    ct.savefig_and_show(file_info, transparent=False, show_message=True, dpi=500)


def main():
    """This is the main fanction to plot the multiplot to visualize the cAMP assay based on the treatment"""
    file_info = ct.process_excel_file(initialdir=None,             # TODO:  initialdirの変更  
                                  allow_sheet_selection=True)
    m_df = load_and_process_data(file_info)
    plot_facetgrid(m_df, file_info)


if __name__ == '__main__':
    main()

