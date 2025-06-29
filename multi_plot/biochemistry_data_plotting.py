import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
from common import common_tools as ct

#%%
def load_data(file_info: Dict[str, str]) -> pd.DataFrame:
    """Load data from an Excel file and return a DataFrame."""
    try:
        df = pd.read_excel(file_info['file_path'],
                        sheet_name = file_info['sheet_name'],
                        header = 0).dropna(axis = 0, thresh = 5).dropna(subset = ['Animal ID'])  # drop rows that doesn't contain non-NAN data more than 5 columns
                                                                                                 # drop rows that doesn't contain any data in the 'Animal ID' column(I want to drow the unit row specifically)
        return df
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")


def transform_data(df: pd.DataFrame, att_dict: Dict[str, str]) -> pd.DataFrame:
    """Transform the DataFrame by melting it and mapping units."""
    # melt the dataframe (without unit information)
    m_df = df.melt(id_vars=['Group'],         # keep the columns as an id variable
                   value_vars=att_dict.keys(),
                   var_name='attribution',
                   value_name='value')
    m_df['unit'] = m_df['attribution'].map(att_dict)
    return m_df


def plot_data(m_df: pd.DataFrame, file_info: Dict[str, str], att_dict: Dict[str, str]) -> None:
    """Generate and save plots."""
    grid = sns.FacetGrid(m_df, col='attribution', col_wrap=4, sharey=False, sharex=False, aspect=1.5)
    grid.map(sns.stripplot, 'Group', 'value', marker='o')   # plot each sample point with dots
    grid.map_dataframe(sns.pointplot, x='Group', y='value', estimator='mean', errorbar='sd', color='gray', markers='_', capsize=0.1, linestyle='none')
    # tried to write unit on each y axis but not successful    
    for ax, col_name in zip(grid.axes.flatten(), grid.col_names):
        unit = att_dict[col_name] # Get the unit for the current attribution

        ax.tick_params(axis='x', rotation=45) # rotate each x labels to 45 degree
        ax.set_ylabel(f'{unit}', fontsize=12)   # Set Y-axis label with unit  

    grid.set_titles(row_template ='', col_template='{col_name}', size=15)
    plt.tight_layout()
    ct.savefig_and_show(file_info, show_message = True)


def visualize_biochemistry_data() -> None:
    # get the unit information
    file_info = ct.process_excel_file(allow_sheet_selection=True)
    att_dict = ct.load_config(file_path=os.path.join(os.path.dirname(__file__), 'attribution_dict.yaml'))   # fix this line and delete the hard coded att_dict in the top of this file
    df = load_data(file_info=file_info)
    m_df = transform_data(df=df, att_dict=att_dict)
    plot_data(m_df=m_df, file_info=file_info, att_dict=att_dict)

#%%
if __name__ == '__main__':
    visualize_biochemistry_data()

