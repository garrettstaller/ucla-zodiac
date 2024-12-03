**UCLA Zodiac Scripts**
-

*For research focus, methodologies and discussion see manuscript*

*Introduction* <br>
-
The University of California, Los Angeles Marine Operations Program is a
student-driven research group focused on physical processes in Santa
Monica Bay, all work being facilitated by observational cruises on the
'Zodiac.' The Zodiac is a 28-ft. zodiac equipped with an ADCP and Rosette
Sampler for CTD casts / Niskin bottles. Since 2015, it has operated as an
observational platform collecting measurements of the water at incredibly
high spatiotemporal resolutions across Santa Monica Bay.

The purpose of this repo is primarily to provide future undergraduates
of the Marine Operations Program with tools for the data analysis of
Zodiac cruise data. The specific purpose being the investigation of
submesoscale structures in Santa Monica Bay.

If you are looking to work with zodiac data not included in provided
file, please refer to **scripts**.

*Information* <br>
-
**Data Access:** <br>
  - Cruise Data **(LATEST: 05/2015 - 01/2024)**
  	- Stored in .pkl files: `track_data.pkl`
  - Geographical Data (OPTIONAL)
    **For plotting bathymetry and land features**
  	- U.S. Coastal Relief Model - Southern California Version 2
  	- https://www.geoplatform.gov/metadata/1f9d35ae-ef0b-43c8-8657-e0de4c55a7e8
  - Satellite Data (OPTIONAL)
    **If using satellite viewer script, please download http://wimsoft.com/CAL/files/**
  	- Temporarily accessed via scripts, no local save functionality
  	- https://spg-satdata.ucsd.edu/
   	 
**Dependencies:** <br>
*There may be a few libraries needed by scripts that are not native to python*
- requests
- pyhdf
- pickle
- cartopy

**Zodiac Functions** <br>
Individual rotuines that are frequently called from `functions.py` file. Routines include
data processing, loading and general graphing functionality. 

*Scripts* <br>
- 
**Uploading Data - Only for users looking for cruise data after 01/2024** <br>
- `GoogleDriveUpload`: Getting data on local machine
  - MUST have access to UCLA Zodiac google drive
  - List folder ID for year of data <br>
- `DataDownload(2024)`: Creating new local .pkl file
  - Need local directory with data
 
**Submesoscale Features** <br>
- `ensembles`: Creates a dictionary of all detected fronts and filaments
  - Dictionary MUST be saved for following script
- `probability_distribution`: Generates pdf of detected submesoscale features

**Satellite Viewer** <br>
- `satellite_viewer`: A tool to view satellite data provided by a website of compiled satellite imagery for SST and chlorophyll
  - See README and data for site: https://spg-satdata.ucsd.edu/
