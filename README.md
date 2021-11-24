<!-- image -->

<h1 align="center"> single-machine-scheduling </h1>
<h2 align="center"> Solve single machine scheduling problem with Carlier and Schrage algorithms </h2>

<!-- https://shields.io/ -->
<p align="center">
  <img alt="Top language" src="https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python">
  <img alt="Status" src="https://img.shields.io/badge/Status-done-green?style=for-the-badge">
  <img alt="Code size" src="https://img.shields.io/github/languages/code-size/KamilGos/single-machine-scheduling?style=for-the-badge">
</p>

<!-- table of contents -->
<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#package-content">Content</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#microscope-tests">Tests</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#technologist-author">Author</a> &#xa0; | &#xa0;
</p>

<br>


## :dart: About ##
This repository contains two algorithms (Carlier and Schrage) used for solving [single-machine schedulling problem](https://en.wikipedia.org/wiki/Single-machine_scheduling)

Every taks that has to be served on machine has three variables:
 
 * R - preparation time,
 * P - execution time,
 * Q - delivery time. 

## :package: Content
 * [data](data) - folder with example data (problems to solve)
 * [carlier.py](carlier.py) - implementation of Carlier algorithm and its modification called "Carlier with elimination"
 * [schrage.py](schrage.py) - implementation of Schrage algorithm

## :checkered_flag: Starting ##
```bash
# Clone this project
$ git clone https://github.com/KamilGos/single-machine-scheduling

# Access
$ cd single-machine-scheduling

# Run the relevant script
$ sudo python3 carlier.py
$ sudo python3 schrage.py
```

## :microscope: Tests ##
<h2>Carlier algorithm</h2>
<div align="center" id="put_id"> 
  <img src=images/carlier.png width="400" />
  &#xa0;
</div>

<h2>Schrage algorithm</h2>
<div align="center" id="put_id"> 
  <img src=images/schrage.png width="400" />
  &#xa0;
</div>


## :memo: License ##

This project is under license from MIT.

## :technologist: Author ##

Made with :heart: by <a href="https://github.com/KamilGos" target="_blank">Kamil Goś</a>

&#xa0;

<a href="#top">Back to top</a>



<!-- ADDONS -->
<!-- images -->
<!-- <h2 align="left">1. Mechanics </h2>
<div align="center" id="inventor"> 
  <img src=images/model_1.png width="230" />
  <img src=images/model_2.png width="236" />
  <img src=images/model_3.png width="228" />
  &#xa0;
</div> -->

<!-- one image -->
<!-- <h2 align="left">2. Electronics </h1>
<div align="center" id="electronics"> 
  <img src=images/electronics.png width="500" />
  &#xa0;
</div> -->


<!-- project dockerized -->
<!-- <div align="center" id="status"> 
  <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png" alt="simulator" width="75" style="transform: scaleX(-1);"/>
   <font size="6"> Project dockerized</font> 
  <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png" alt="simulator" width="75"/>
  &#xa0;
</div>
<h1 align="center"> </h1> -->