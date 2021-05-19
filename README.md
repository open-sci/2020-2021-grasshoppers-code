# 2020-2021-grasshoppers-code
This is the repository of the software used for cleaning and classifying invalid DOI names collected by the [OpenCitations Index Of Crossref Open DOI-To-DOI References (COCI)](https://opencitations.net/index/coci) while processing data provided by [Crossref](https://www.crossref.org/).<br/>
Zenodo link for the paper: [Cleaning different types of DOI errors found in cited references on Crossref using automated methods](http://doi.org/10.5281/zenodo.4734513).<br/>
## Disclaimer 
This projec has been realized during the University of Bologna course in [Open Science](https://www.unibo.it/en/teaching/course-unit-catalogue/course-unit/2020/443753) held by Professor Silvio Peroni in the y.a. 2020-2021.
## Getting started
Before starting, you need to make sure you have Python3.x installed on your computer, in addition, in order to correctly execute the Python-based scripts indicated in the methodology, you must install the required libraries defined in requirements.txt. Please follow the official Python guidelines at [https://wiki.python.org/moin/BeginnersGuide/](https://wiki.python.org/moin/BeginnersGuide/) to check and eventually install python and the required libraries locally on your machine.
## Reproduce the paper's experiment
To reproduce the paper experiments clone the github repository on your machine and launch the following command in a prompt inside the repository:
```
python tutorial.py
```
This command will launch our cleaning procedure on the dataset "invalid_dois.csv" in the dataset folder. This dataset is provided on public license in Peroni, Silvio. (2021). Citations to invalid DOI-identified entities obtained from processing DOI-to-DOI citations to add in COCI (Version 1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4625300.<br/>
If you want to apply our cleaning procedure on another dataset first verify that your dataset is a CSV file compliant with the fields used in our data and then modify the following line in the tutorial.py file
```
data = Support.process_csv_input(path=path_to_data)
```
Beware that our algorithm will require days for huge amount of data, like in our research (e.g. > 1M rows).<br/>
If you want to speed up the process you can add the following line after importing your data in tutorial.py
```
crossref_dois = Support.process_csv_input(path="./dataset/crossref_dois.csv")
```
**Note:** This line will allow to perform the DOI validation through a list of DOI registered by Crossref available in the dataset folder. It is recommended to perform the following step having at least 64GB of RAM, as over 200 million DOIs need to be stored in a set and kept on RAM throughout the execution of our software.<br/>
## Results
A visualization of the results of our experiment on the paper's dataset as well as a comparison with the results obtained by applying a procedure derived from Xu, S., Hao, L., An, X. et al. Types of DOI errors of cited references in Web of Science with a cleaning method. Scientometrics 120, 1427–1437 (2019). [https://doi.org/10.1007/s11192-019-03162-4](https://doi.org/10.1007/s11192-019-03162-4) on the same data are available in [https://open-sci.github.io/2020-2021-grasshoppers-code/](https://open-sci.github.io/2020-2021-grasshoppers-code/)
## References
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021). Classes of errors in DOI names (Data Management Plan) (Version 4). Zenodo. https://doi.org/10.5281/zenodo.4733920
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021). Classes of errors in DOI names: output dataset (Version v1.0.0-alpha) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4733647
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021, May 3). Cleaning different types of DOI errors found in cited references on Crossref using automated methods (Version 1). Zenodo. http://doi.org/10.5281/zenodo.4734513
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021, May). Presentation of "Cleaning different types of DOI errors found in cited references on Crossref using automated methods" (Version 1). Zenodo. http://doi.org/10.5281/zenodo.4738553
- Ricarda Boente, Deniz Tural, Cristian Santini, Arcangelo Massari. (2021). Protocol: Investigating DOIs classes of errors V.4. protocols.io https://dx.doi.org/10.17504/protocols.io.bunnnvde
- Peroni, Silvio. (2021). Citations to invalid DOI-identified entities obtained from processing DOI-to-DOI citations to add in COCI (Version 1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4625300
- Xu, S., Hao, L., An, X. et al. Types of DOI errors of cited references in Web of Science with a cleaning method. Scientometrics 120, 1427–1437 (2019). https://doi.org/10.1007/s11192-019-03162-4
