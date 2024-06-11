# smFISH mRNA-organelle Statistical Analysis Tool

The data collected concerns signals given from a specific mRNA molecule and each molecule's relative localization to a studied sub-cellular site (also called organelle). The Data also devides the organelle to two distinct areas. One of which is close to a proximity marker and another that is far away from it. The data represients each cell as a line and contains the amount of mRNA in each designation, the cellular coverage of the organelle in each cross-section imaged (in %) and data for each mRNA signal identifed. mRNA data inclueds the plane number, the intesity and the colocalization status of each mRNA signal. Each csv file contains data for a single sample.

This program will be used to perform filtering and statistical analysis for csv files containing said data. The input data will be in the following format:

![table](img/start_table.png)

- **Cell #**: The designated number for the cell represented in the row.
- **Total mRNA per Cell**: The number of mRNA signals identified in the cell.
- **Total Colocolized With Irgnalle Near/Far**: The number of mRNAs designated as colocalized near/far a proximity marker.
- **Total Not Colocolized with Organelle**: The number of mRNAs designated as not colocolized with the organelle.
- **Organelle Signal Coveraege of Cell List**: A list with the cellular coverage (in %) of the organelle in each cross-section imaged.
- **mRNAs z coords**: The z-plane location of each mRNA signal in the cell.
- **mRNAs intesities**: The intesitie value for each mRNA signal in the cell.
- **mRANAs statis**: The colocalization designation for each mRNA signal in the cell.

### The goal of the tool is as follows:
- The tool will be given a folder and will work dequntially on all files in the folder.
- Filter out cells containing 0 mRNA signals.
- Filter out specific mRNA signals using user inputed values of organelle signal coverage and mRNA intesities.
- Create a new, filtered table, withouth the signals and cells that were removed.
- Perform statistical analysis on the filtered data, including average localization ratios for each file (and error values), ttests between each file, correlations between organelle coverage and colocalizaion ratios.
- Create and output a file with the statistical analysis data between all samples.
- Output grpahs for the colocalization data (violin plots) and the correlation (scatter plots).

### Dependencies:
- Will be updated as the program is written.

### How-to:
To run the program you will need a folder containing the files described above. The program can handle any number of files. Each file will represent a single sample from the smFISH experiment.
Once you run the program ("main file name") you will be prompted to input the folder with the files, through a browse window. After that, you will need to input the number of samples in the experiment (an int) a name for each sample (will appear in the graphs and tables) and a distinct name for the file of each sample (will be used to identify the file in the folder). The file name needs to be a part of the file for that sample and must not be a part of any other file in the folder. It will be case sensitive.
