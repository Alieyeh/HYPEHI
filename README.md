<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Alieyeh/HYPEHD">
    <img src="Animated Logo 500x500 px.gif" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">HYPEHD</h3>

  <p align="center">
    A package to aid in data exploration for health data.
    <br />
    <a href="https://github.com/Alieyeh/HYPEHD/issues">Report Bug</a>
    ·
    <a href="https://github.com/Alieyeh/HYPEHD/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#dependencies">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#examples">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

**put description here**

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Dependencies
- Python 3 (with the following auto-installed packages)
    - numpy
    - matplotlib
    - seaborn
    - pandas
    - scipy.stats
    - itertools
    - sklearn.cluster
    - lifelines
    - math
    - operator

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Examples
Below are some examples of using this package. The test dataset is from https://github.com/insightsengineering/scda.2022

1. import package
   ```sh
   import visualization as vis
   import data_manipulation as da
   ```
2. read test data
   ```sh
   dm = pd.read_csv("data/demographic.csv")
   vs = pd.read_csv("data/vital_signs.csv")
   ```
3. filter data using `data_selection()` function in data_manipulation
   filter the dataset vs to select only weight records and merge it with dataset dm
   ```sh
   test = da.data_selection(keep_col=["USUBJID", "PARAMCD", "AVAL"], sort_by=["SEX", "AGE"], sort_asc=True, 
                            input_data=vs,cond='PARAMCD=="WEIGHT"', merge_data=dm, merge_by="USUBJID",
                            merge_keep_col=["USUBJID", "ITTFL", "SEX", "AGE", "TRT01P"])
   ```
4. derive baseline info using `derive_baseline()` function in data_manipulation
   calculate change from baseline, percent change from baseline of weight per each subject
   ```sh
   test = da.derive_baseline(input_data=test, by=["USUBJID", "PARAMCD"], value="AVAL", chg=True, pchg=True, 
                      base_visit='AVISITN==0')
   ```
5. generate demographic plots using `demo_graph()` function in visualization
   plots of AGE, SEX and RACE by different treatment group
   ```sh
   vis.demo_graph(var=["AGE", "SEX", "RACE"], input_data=dm, by='TRT01P')
   ```
6. generate line plots using `longitudinal_graph()` function in visualization
   plots of change from baseline, percent change from baseline by different visit
   ```sh
   vis.longitudinal_graph(outcome=["CHG", "PCHG"], time="AVISITN", group="TRT01P", input_data=test)
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Alieyeh/HYPEHD](https://github.com/Alieyeh/HYPEHD)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

