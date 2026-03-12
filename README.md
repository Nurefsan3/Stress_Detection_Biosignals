# Stress_Detection_Biosignals


This project investigates stress detection in university students using physiological signals collected during cognitive tasks.

University students often experience high levels of stress due to academic pressure and exam anxiety. The aim of this project is to analyze physiological stress responses and explore potential interventions that may help students manage stress.

## Signals

The physiological signals used in this study include:

- ECG (Electrocardiogram)
- GSR / EDA (Galvanic Skin Response / Electrodermal Activity)

These signals are collected during cognitive stress tasks and analyzed to detect physiological changes related to stress.

## Experiment

A cognitive stress experiment is implemented using the **Montreal Imaging Stress Task (MAT)** paradigm in PsychoPy.

The experiment includes:

- Baseline (resting) measurements  
- Cognitive stress tasks  
- Physiological signal recording
  
The experiment protocol is as follows:


  <img width="605" height="65" alt="image" src="https://github.com/user-attachments/assets/f2218eb1-752b-426f-90dd-9c17f71d1536" />
  <img width="605" height="65" alt="Screenshot 2025-10-15 134416" src="https://github.com/user-attachments/assets/17862b9c-2b41-4dbd-9ec4-01a9cf1b626b" />

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------

The following screenshots show the PsychoPy interface used to implement the cognitive stress task




<img width="785" height="400" alt="image" src="https://github.com/user-attachments/assets/e8b03b13-d63a-402e-b847-d1ddc9b66a07" />


## Data Processing

The collected physiological signals are analyzed using:

- **Python**
- **MATLAB**

Current analysis includes:

- BPM extraction from ECG signals  
- GSR signal processing  

## Example Experimental Results

The following figure shows an example analysis from a pilot experiment.

Top left: Average BPM values during baseline, stress task levels, and resting phases.  
Bottom left: GSR waveform showing physiological changes during the experiment.  
Right: Performance results from the MAT task (correct, wrong, and timeout responses).


<img width="700" height="400" alt="Screenshot 2026-02-04 105117" src="https://github.com/user-attachments/assets/8bb62fa3-f95e-4530-bbf6-300772503b54" />


## Future Work

Planned future work includes:

- physiological feature extraction  
- stress classification models  
- evaluation of stress reduction interventions such as breathing exercises and music therapy  
- wearable stress monitoring systems

## Project Status

Ongoing research project.
