import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from common import common_tools as ct


def load_data(file_info: dict[str, str]) -> pd.DataFrame:
    """Load data from an Excel file and return a DataFrame."""
    df = pd.read_excel(file_info['file_path'],
                       file_info['sheet_name'],
                       header = 0)
    return df


def melt_df(df: pd.DataFrame ) -> pd.DataFrame:
    m_df = df.melt(id_vars = ['rep', 'pH'],     # keep the columns as an id variable
                   var_name = 'lipid',
                   value_name = 'Fluorescence')
    return m_df


def boltzmann(x, A1, A2, x0, dx):
    return A2 + (A1 - A2)/(1 + np.exp((x - x0)/dx))

    

#%% fitting and plot for each lipid with error bars 

def plot_curve_ErrorBar(m_df: pd.DataFrame, file_info: dict[str, str], lipid_list: dict[str, str]) -> None:
    for lipid in lipid_list:
        print(lipid)
        df = m_df[m_df.lipid == lipid].dropna(axis=0, how='any')
        print(df)
        
        grouped_df = df.groupby('pH').agg(Fluorescence_mean=('Fluorescence', 'mean'),
                                          Fluorescence_std=('Fluorescence', 'std')
                                          ).reset_index()
        
        x_data = grouped_df['pH']
        y_data = grouped_df['Fluorescence_mean']
        y_error = grouped_df['Fluorescence_std']
        
        
        # perform curve fitting
        popt, pcov = curve_fit(boltzmann, x_data, y_data)
        A1, A2, x0, dx = popt
        
        # calculate the standard deviation of the fitted parameters
        perr = np.sqrt(np.diag(pcov))
        A1_std, A2_std, x0_std, dx_std = perr
        
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = boltzmann(x_fit, A1, A2, x0, dx)
        
        # Calculate R-squared
        ss_res = np.sum((y_data - boltzmann(x_data, *popt))**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate Adjusted R-squared
        n = len(y_data)
        k = 4  # number of predictors in the Boltzmann model
        r_squared_adj = 1 - (1 - r_squared) * (n - 1) / (n - k - 1)
        
        
        results = (f'A1 = {A1:.1f} ± {A1_std:.1f} \n'
                   f'A2 = {A2:.1f} ± {A2_std:.1f} \n'
                   f'x0 = {x0:.2f} ± {x0_std:.2f} \n'
                   f'dx = {dx:.2f} ± {dx_std:.2f} \n'
                   f'R^2 = {r_squared:.4f}\n'
                   f'adj. R^2 = {r_squared_adj:.4f}'
                   )
        
        
        print(results)                          # print the result
        plt.figure()                            # create a new plot
        plt.title(f'Lipid = {lipid}', size = 15)    # put title on the top of plot
        sns.scatterplot(x=x_data, y=y_data) # scatter plot of the measured values
        sns.lineplot(x=x_fit, y=y_fit)      # plot the line plot of the fitting
        plt.errorbar(x_data, y_data, yerr=y_error, 
                     fmt='o', color='gray', ecolor='gray', elinewidth=1, capsize=4) # error bars
        plt.text(x=2, y=1000, s=results)  # insert the fitting data in each plot
        save_path = os.path.join(file_info["directory"], f'pKa_{lipid}.png')
        print(f'fig saved as: {save_path}')
        plt.savefig(save_path, dpi=200, transparent=False)
        plt.savefig(f'pKa_{lipid}.png', dpi=200)  # save figures with title as .png file



#%% melt each DataFrame and conbined into one dataframe
def visualize_pKa() -> None :
    file_info = ct.process_excel_file(allow_sheet_selection = True)
    df = load_data(file_info)
    m_df = melt_df(df)
    lipid_list = m_df['lipid'].unique().tolist()   # store the lipid names in lipid_list as a list 
    plot_curve_ErrorBar(m_df=m_df, lipid_list=lipid_list, file_info=file_info)

#%%
if __name__ == '__main__':
    visualize_pKa()



