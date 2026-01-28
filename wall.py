"""
PLAXIS Data Extractor
Extracts cross-section results from PLAXIS 2D models and exports to Excel
"""

import os
import sys
import subprocess
import pandas as pd
import plxscripting.easy as plx
from pathlib import Path


def find_plaxis_executable():
    """
    Dynamically find PLAXIS 2D installation path.
    Searches common installation directories for different versions.
    """
    common_paths = [
        r"C:\Program Files\Seequent\PLAXIS 2D 2024\Plaxis2DXInput.exe",
        r"C:\Program Files\Seequent\PLAXIS 2D 2023\Plaxis2DXInput.exe",
        r"C:\Program Files (x86)\Seequent\PLAXIS 2D 2024\Plaxis2DXInput.exe",
        r"C:\Program Files (x86)\Seequent\PLAXIS 2D 2023\Plaxis2DXInput.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # If not found in common locations, ask user
    print("PLAXIS 2D installation not found in standard locations.")
    print("Please enter the full path to Plaxis2DXInput.exe:")
    user_path = input("> ").strip().strip('"')
    
    if os.path.exists(user_path):
        return user_path
    else:
        raise FileNotFoundError(f"PLAXIS executable not found at: {user_path}")


def main():
    """Main function to run the PLAXIS data extraction"""
    
    # Get user inputs
    parent_folder = input("Enter the parent folder path containing .p2dx files: ").strip()
    
    if not os.path.isdir(parent_folder):
        print(f"Error: Directory not found: {parent_folder}")
        sys.exit(1)
    
    password = "1234567890"
    
    # Find PLAXIS executable
    plaxis_exe = find_plaxis_executable()
    print(f"Using PLAXIS installation: {plaxis_exe}")
    
    # Start PLAXIS process
    plaxis_proc = subprocess.Popen([
        plaxis_exe,
        "--AppServerPort=10000", 
        f"--AppServerPassword={password}"
    ])
    
    # Initialize servers
    s_i, g_i = plx.new_server('localhost', 10000, password=password)
    s_o, g_o = plx.new_server('localhost', 10001, password=password)
    
    # Initialize data columns
    model = ['modelname']
    stage = ['stage']
    col_x = ['x']
    col_y = ['y']
    col_utot = ['utot']
    col_ux = ['ux']
    col_uy = ['uy']
    col_sigxxe = ['sigxxe']
    col_sigyye = ['sigyye']
    col_effnormalstress = ['eff_normal_stress']
    col_totnormalstress = ['tot_normal_stress']
    col_totshearstress = ['tot_shear_stress']
    
    # Process all .p2dx files
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith('.p2dx') and not file.endswith('data.p2dx'):
                p2d_file_path = os.path.join(root, file)
                
                print(f"Processing file: {p2d_file_path}")
                
                try:
                    s_i.open(p2d_file_path)
                    g_i.gotostages()
                    g_i.view(g_i.Phases[0])
                    plot_o = g_o.Plots[-1]
                    cs_soil_plot = g_o.linecrosssectionplot(plot_o, (10, 0), (10, -6))
                    
                    for idx, phase in enumerate(g_o.Phases):
                        values_soil_X = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.X)
                        values_soil_Y = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.Y)
                        values_soil_Utot = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.Utot)
                        values_soil_Ux = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.Ux)
                        values_soil_Uy = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.Uy)
                        values_soil_SigxxE = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.SigxxE)
                        values_soil_SigyyE = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.Soil.SigyyE)
                        values_soil_EffNormalStress = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.CrossSection.EffNormalStress)
                        values_soil_TotNormalStress = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.CrossSection.TotNormalStress)
                        values_soil_TotShearStress = g_o.getcrosssectionresults(cs_soil_plot, phase, g_o.ResultTypes.CrossSection.TotShearStress)
                        
                        name = getattr(phase.Identification, "value", str(phase.Identification))
                        
                        model.append(p2d_file_path)
                        stage.append(name)
                        col_x.append(list(values_soil_X))
                        col_y.append(list(values_soil_Y))
                        col_utot.append(list(values_soil_Utot))
                        col_ux.append(list(values_soil_Ux))
                        col_uy.append(list(values_soil_Uy))
                        col_sigxxe.append(list(values_soil_SigxxE))
                        col_sigyye.append(list(values_soil_SigyyE))
                        col_effnormalstress.append(list(values_soil_EffNormalStress))
                        col_totnormalstress.append(list(values_soil_TotNormalStress))
                        col_totshearstress.append(list(values_soil_TotShearStress))
                        
                except Exception as e:
                    print(f"Error processing {p2d_file_path}: {e}")
                    continue
    
    # Create DataFrame
    df = pd.DataFrame({
        'Model': model, 
        'Stage': stage,
        'X': col_x,
        'Y': col_y,
        'Utot': col_utot,
        'Ux': col_ux,
        'Uy': col_uy,
        'SigxxE': col_sigxxe,
        'SigyyE': col_sigyye,
        'EffNormalStress': col_effnormalstress,
        'TotNormalStress': col_totnormalstress,
        'TotShearStress': col_totshearstress
    })
    
    # Process and export data
    df_exploded = df.copy()
    list_cols = ['X', 'Y', 'Utot', 'Ux', 'Uy', 'SigxxE', 'SigyyE', 'EffNormalStress', 'TotNormalStress', 'TotShearStress']
    df_data = df_exploded.iloc[1:].copy()
    
    for col in list_cols:
        df_data[col] = df_data[col].apply(lambda x: x if isinstance(x, list) else [x])
    
    df_expanded = df_data.explode(list_cols).reset_index(drop=True)
    
    # Save results
    output_file = os.path.join(parent_folder, 'soil_cross_section_results.csv')
    df_expanded.to_csv(output_file, index=False)
    print(f"Results saved to: {output_file}")
    
    # Cleanup
    try:
        plaxis_proc.terminate()
    except:
        pass


if __name__ == "__main__":
    main()