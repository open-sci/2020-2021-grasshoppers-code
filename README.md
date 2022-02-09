# Classes of errors in DOI names

This is the repository of the software used for cleaning and classifying invalid DOI names from the dataset <em>Citations to invalid DOI-identified entities obtained from processing DOI-to-DOI citations to add in COCI</em> [(Peroni, 2021)](https://doi.org/10.5281/zenodo.4625300). The invalid DOIs were collected by Silvio Peroni while processing data provided by Crossref and, since invalid, they were not added to the [OpenCitations Index Of Crossref Open DOI-To-DOI References (COCI)](https://opencitations.net/index/coci).

The paper describing this work can be found on Zenodo at the following address: [Cleaning different types of DOI errors found in cited references on Crossref using automated methods](http://doi.org/10.5281/zenodo.4734513).

## Disclaimer 

This project has been realized during the University of Bologna course in [Open Science](https://www.unibo.it/en/teaching/course-unit-catalogue/course-unit/2020/443753) held by Professor Silvio Peroni in the y.a. 2020-2021.

## Getting started

Before starting, you need to make sure you have Python3.x installed on your computer, in addition, in order to correctly execute the Python-based scripts indicated in the methodology, you must install the required libraries defined in requirements.txt. Please follow the official Python guidelines at [https://wiki.python.org/moin/BeginnersGuide/](https://wiki.python.org/moin/BeginnersGuide/) to check and eventually install Python and the required libraries locally on your machine.

## Reproduce the experiment
To reproduce the paper experiment clone the GitHub repository on your machine and launch the following command in a prompt inside the repository:
```bash
python tutorial.py
```
This command will launch the cleaning procedure on the dataset "invalid_dois.csv" in the dataset folder. The dataset is provided on public license by [Silvio Peroni (2021)](http://doi.org/10.5281/zenodo.4625300).
If you want to apply the cleaning procedure on another dataset, first verify that your dataset is a CSV file compliant with the fields used in our data and then modify the following line in the tutorial.py file
```python
data = Support.process_csv_input(path=path_to_data)
```
Beware that the algorithm will require days for huge amount of data, like in this research (e.g. > 1M rows).<br/>
If you want to speed up the process, you can unzip the "crossref_dois.zip" archive in the dataset folder and then add the following line after importing your data in tutorial.py
```python
crossref_dois = Support.process_csv_input(path="./dataset/crossref_dois.csv")
```
**Note:** This line will allow to perform the DOI validation through a list of DOI registered by Crossref available in the dataset folder. It is recommended to perform the following step having at least 64GB of RAM, as over 120 million DOIs need to be stored in a set and kept on RAM throughout the execution of our software.

## Hardware configuration

The experiment was conducted on a computer with the following hardware specifications. Only the components relevant to the results' reproduction are reported:

- CPU: Intel Core i5 8500 @ 3.00 GHz, 6 core, 6 logic processors
- RAM: 32 GB DDR4 3000 MHz CL15
- Storage: 1 TB SSD Nvme PCIe 3.0

## Results

A visualization of the results of our experiment, as well as a comparison with the results obtained by applying a similar procedure derived from [Xu et al (2019)](https://doi.org/10.1007/s11192-019-03162-4) on the same data, are available at the address https://open-sci.github.io/2020-2021-grasshoppers-code/.

## References

- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021). Classes of errors in DOI names (Data Management Plan) (Version 5). Zenodo. https://doi.org/10.5281/zenodo.4733919
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021). Classes of errors in DOI names: output dataset (Version v1.0.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4892551
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021, June 8). Cleaning different types of DOI errors found in cited references on Crossref using automated methods (Version 2). Zenodo. http://doi.org/10.5281/zenodo.4734512
- Boente, Ricarda, Massari, Arcangelo, Santini, Cristian, & Tural, Deniz. (2021, May). Presentation of "Cleaning different types of DOI errors found in cited references on Crossref using automated methods" (Version 1). Zenodo. http://doi.org/10.5281/zenodo.4738553
- Ricarda Boente, Deniz Tural, Cristian Santini, Arcangelo Massari. (2021). Protocol: Investigating DOIs classes of errors V.5. protocols.io https://dx.doi.org/10.17504/protocols.io.buuknwuw
- Peroni, Silvio. (2021). Citations to invalid DOI-identified entities obtained from processing DOI-to-DOI citations to add in COCI (Version 1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4625300
- Xu, S., Hao, L., An, X. et al. Types of DOI errors of cited references in Web of Science with a cleaning method. Scientometrics 120, 1427–1437 (2019). https://doi.org/10.1007/s11192-019-03162-4
