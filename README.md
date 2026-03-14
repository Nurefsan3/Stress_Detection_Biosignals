# Biosignal-Based Stress Detection and Personalized Stress Management System


This project investigates stress detection in university students using physiological signals (ECG and GSR) collected during Mental Arithmetic Task.

University students often experience high levels of stress due to academic pressure and exam anxiety. The aim of this project is to analyze physiological stress responses and explore potential interventions that may help students manage stress.

## Signals

The physiological signals used in this study include:

- ECG (Electrocardiogram)
- GSR / EDA (Galvanic Skin Response / Electrodermal Activity)

These signals are collected during Mental Arithmetic Task and analyzed to detect physiological changes related to stress.

## Experiment

Phase 1 – Standard MAT Experiment

In the first phase, participants undergo the standard MAT protocol. First, during the Baseline phase, the participant’s normal physiological responses are measured to obtain baseline data.  Participants then solve mental arithmetic problems of varying difficulty levels under time pressure for approximately five minutes each. During the rest phases between tasks, participants are shown only a blank white screen.

The objective of this phase is to measure participants’ physiological baseline responses under stress.

The experimental procedure is as follows:


  <img width="605" height="65" alt="image" src="https://github.com/user-attachments/assets/f2218eb1-752b-426f-90dd-9c17f71d1536" />
  <img width="605" height="65" alt="Screenshot 2025-10-15 134416" src="https://github.com/user-attachments/assets/17862b9c-2b41-4dbd-9ec4-01a9cf1b626b" />

Phase 2 – Intervention Experiment

Approximately 2–3 weeks after the first experiment, the same participants are enrolled in the same experimental protocol again. In this phase, the task structure remains the same, but the rest phases are modified.

While the standard MAT protocol features a blank screen during rest phases, this phase will incorporate stress-reduction techniques during rest phases:

instrumental music

guided breathing exercises

The purpose of this phase is to examine the effects of different stress-reduction methods on participants’ physiological stress responses.



  ----------------------------------------------------------------------------------------------------------------------------------------------------------------

  ## Project Pipeline

  

The following screenshots show the PsychoPy interface used to implement the cognitive stress task

<img src="pipeline.png" width="700">


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
