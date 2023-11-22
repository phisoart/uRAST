uRAST
=====================

## Overview
The phenotype-driven uRAST platform allows for drug susceptibility assessments straight from the patient's whole blood, eliminating the necessity for blood culture(BC). 
Moreover, we present an exceptionally sensitive pathogen ID test(QmapID) that doesn't require BC and delivers real-time species data, crucial for accurate AST analysis. 
When contrasted with traditional hospital AST, our method shorthen the turnaround time by over 60 hours, facilitating the swiftest recorded prescription of appropriate antibiotics.
This code encompasses two algorithms: 
1) Image processing algorithm and reporting time for SIR determination.
2) Deciphering algorithm for QmapID.

# System Requirements
## Hardware requirements
This code requires only a standard computer with enough RAM to support the in-memory operations.

## Software requirements
### OS Requirements
This package is supported for *macOS* and *Linux*. The package has been tested on the following systems:
+ macOS: Big Sur (11.6)
+ Linux: Ubuntu 16.04

### Python Dependencies
This code mainly depends on the Python scientific stack.
```
pillow
numpy
multiprocessing
pandas
scikit-learn
scipy
opencv-python
```

# Installation Guide:
### Install from Github
You can use "main.py" to use the codes.
```
git clone https://github.com/phisoart/uRAST
```

# Demo:
## Instructions to run on data
- Image processing algorithm and reporting time for SIR determination.
```
python3 main.py -a "uRAST" -f "source" -o "out_dir"
```
### output
<img src="https://github.com/phisoart/uRAST/blob/master/uRAST.jpg">

- Deciphering algorithm for QmapID.
```
python3 main.py -a "QmapID" -f "source" -o "out_dir"
```
### output
<img src="https://github.com/phisoart/uRAST/blob/master/QmapID.jpg">

## Expected run time for demo
Both algorithms, when executed on a standard computer, require a mere span ranging from several seconds to a few minutes.

Due to storage and security concerns, data are provided only for certain bacterial species and antibiotic combinations. If additional data are needed for research purposes, please contact the authors

## Acknowledgments
BiNEL (http://binel.snu.ac.kr) - This code is made available under the MIT License and is available for non-commercial academic purposes
