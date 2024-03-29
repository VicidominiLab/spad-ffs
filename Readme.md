# SPAD-FFS

Pyhon code for the analysis of confocal laser-scanning microscopy based fluorescence fluctuation spectroscopy (FFS) data. The code is designed to analyze FFS data obtained with a 5x5 pixel SPAD array detector, instead of the typical point-detector. Includes code for:

- reading raw data files
- calculating autocorrelations and cross-correlations
- fitting the correlation curves with various fit models

## How do I use it?

Under Examples, a Jupyter notebook is available with an example. The raw data set used here is available on [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4161418.svg)](https://doi.org/10.5281/zenodo.4161418). This data set contains the fluorescence intensity time traces for the 25 pixels for a freely diffusing antibody conjugated Alexa 488 dye. The time traces can be analyzed in various ways, such as spot-variation FCS, two-focus or pair-correlation FCS, and intensity mean-squared-displacement analysis.
