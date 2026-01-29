# PLAXIS Data Extractor

A Python tool to automatically extract cross-section results from PLAXIS 2D models and export them to CSV format.

## Overview

This tool processes PLAXIS 2D (.p2dx) model files and extracts soil analysis data including:
- Coordinates (X, Y)
- Displacements (Total, X-direction, Y-direction)
- Stresses (SigxxE, SigyyE, Effective/Total Normal Stress, Total Shear Stress)

The data is organized by model and analysis stage, making it easy to compare results across phases.



## Installation

### Step 1: Clone or Download the Repository

```bash
# If using Git
git clone YossefEzz/Plaxis-Data-Extractor
cd Plaxis\ Data\ Extractor

# Or extract the ZIP file and open the folder
```

### Step 2: Install Python Dependencies

Open PowerShell or Command Prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

**Why this works on any computer:** The `requirements.txt` file specifies exactly which Python packages are needed and their versions. When someone runs `pip install -r requirements.txt`, Python automatically downloads and installs the correct versions from the internet, regardless of the computer.

## Usage

### Running the Script

1. **Prepare your PLAXIS model files** - Collect all `.p2dx` files you want to analyze

2. **Run the script:**
   ```bash
   python wall.py
   ```

3. **Enter the parent folder path** - When prompted, provide the path containing your `.p2dx` files:
   ```
   Enter the parent folder path containing .p2dx files: C:\Users\YourName\Documents\PLAXIS_Models
   ```

4. **Wait for processing** - The script will:
   - Find your PLAXIS installation automatically (if 2023/2024 standard locations)
   - Launch PLAXIS 2D in background mode
   - Process each model file
   - Extract cross-section data for all analysis phases
   - Save results to `soil_cross_section_results.csv`

### Output

The CSV file contains the following columns:
- **Model** - Path to the original .p2dx file
- **Stage** - Analysis phase name
- **X, Y** - Coordinate data
- **Utot** - Total displacement
- **Ux, Uy** - Displacement components
- **SigxxE, SigyyE** - Stress components
- **EffNormalStress** - Effective normal stress
- **TotNormalStress** - Total normal stress
- **TotShearStress** - Total shear stress

Each row represents a point on the cross-section, with multiple rows per stage.

## How It Works (Technical Details)

### Portability Features

1. **Automatic PLAXIS Detection**
   - Instead of hardcoding one specific path, the script searches common installation directories
   - If not found, it prompts the user to provide the path
   - This ensures it works whether PLAXIS is installed on C: or D: drive, or in custom locations

2. **Path Independence**
   - Uses `os.path.join()` for cross-platform compatibility (Windows/Linux)
   - No hardcoded folder separators (always dynamic)
   - Relative paths instead of absolute paths where possible

3. **Dependency Management**
   - `requirements.txt` lists all Python package dependencies
   - `pip` automatically handles downloads (no manual installation needed)
   - Ensures everyone uses compatible versions

### Data Processing Flow

```
PLAXIS Files (.p2dx)
        ↓
    Launch PLAXIS
        ↓
    For each file:
        - Open model
        - Create cross-section plot at (10,0) to (10,-6)
        - Extract results for each analysis phase
        ↓
    Collect data in lists
        ↓
    Create DataFrame (organized table)
        ↓
    Explode lists into rows
        ↓
    Export to CSV
```

## Troubleshooting

### "PLAXIS executable not found"
- Ensure PLAXIS 2D 2023 or 2024 is installed
- Standard paths checked:
  - `C:\Program Files\Seequent\PLAXIS 2D 2024\`
  - `C:\Program Files\Seequent\PLAXIS 2D 2023\`
  - `C:\Program Files (x86)\...` (32-bit versions)
- If installed elsewhere, provide the full path when prompted

### "No module named 'plxscripting'"
```bash
# Ensure PLAXIS Scripting is installed:
pip install plxscripting
```

### "FileNotFoundError: No .p2dx files found"
- Check that .p2dx files exist in the specified folder
- The script searches recursively in all subfolders
- Verify file extension is exactly `.p2dx` (case-sensitive)

### PLAXIS server connection timeout
- Ensure no other PLAXIS instances are running on ports 10000-10001
- Windows Firewall may need to allow Python execution
- Try running PowerShell as Administrator

## Configuration (Advanced)

### Custom Cross-Section Coordinates

Edit line in `wall.py`:
```python
cs_soil_plot = g_o.linecrosssectionplot(plot_o, (10, 0), (10, -6))
```

Change `(10, 0)` and `(10, -6)` to your desired coordinates.

### Custom Password

The server password is set to `"1234567890"` - this can be changed (must match between server and client calls).

## File Structure

```
Plaxis Data Extractor/
├── wall.py                          # Main script
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
└── soil_cross_section_results.csv   # Output (generated after running)
```

## License

Specify your license (MIT, GPL, etc.) or note if proprietary.

## Support

For issues related to:
- **Script errors** - Check troubleshooting section above
- **PLAXIS integration** - Ensure PLAXIS Scripting is installed
- **Python environment** - Run `pip --version` and `python --version` to verify installation
