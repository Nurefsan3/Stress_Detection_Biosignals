# Biosignal-Based Stress Detection and Personalized Stress Management System


This project investigates stress detection in university students using physiological signals (ECG and GSR) collected during Mental Arithmetic Task.

University students often experience high levels of stress due to academic pressure and exam anxiety. The aim of this project is to analyze physiological stress responses and explore potential interventions that may help students manage stress.

## Signals

The physiological signals used in this study include:

- ECG (Electrocardiogram)
- GSR / EDA (Galvanic Skin Response / Electrodermal Activity)

These signals are collected during Mental Arithmetic Task and analyzed to detect physiological changes related to stress.

 ## Project Pipeline

  <img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/72360fa0-80e9-443e-b7d0-6744b3faff6a" />

## Experiment

Phase 1 – Standard MAT Experiment

In the first phase, participants undergo the standard MAT protocol. First, during the Baseline phase, the participant’s normal physiological responses are measured to obtain baseline data.  Participants then solve mental arithmetic problems of varying difficulty levels under time pressure for approximately five minutes each. During the rest phases between tasks, participants are shown only a blank white screen.

The objective of this phase is to measure participants’ physiological baseline responses under stress.

The experimental procedure is as follows:


  <img width="705" height="100" alt="image" src="https://github.com/user-attachments/assets/f2218eb1-752b-426f-90dd-9c17f71d1536" />
  <img width="705" height="100" alt="Screenshot 2025-10-15 134416" src="https://github.com/user-attachments/assets/17862b9c-2b41-4dbd-9ec4-01a9cf1b626b" />

Phase 2 – Intervention Experiment

Approximately 2–3 weeks after the first experiment, the same participants are enrolled in the same experimental protocol again. In this phase, the task structure remains the same, but the rest phases are modified.

While the standard MAT protocol features a blank screen during rest phases, this phase will incorporate stress-reduction techniques during rest phases:

instrumental music

guided breathing exercises

The purpose of this phase is to examine the effects of different stress-reduction methods on participants’ physiological stress responses.






  ## MAT Design

The Mental Arithmetic Task (MAT) is a task that requires participants to solve arithmetic problems under time pressure in order to induce cognitive stress. The task consists of two different difficulty levels.

Level 1 
At this level, participants solve simpler arithmetic problems involving addition and subtraction.

Level 2
In the second level, the difficulty of the questions increases.
When a participant answers a question correctly, the time allotted to solve the next question decreases.
When a participant answers a question incorrectly, the time allotted to solve the next question increases.

The Baseline and Rest sections consist solely of a blank screen.

This is intended to create stress by placing time pressure on the participant.


  

The following screenshots show the PsychoPy interface used to implement the cognitive stress task





<img width="700" height="300" alt="image" src="https://github.com/user-attachments/assets/e8b03b13-d63a-402e-b847-d1ddc9b66a07" />


## Data Processing

The collected physiological signals are analyzed using:

- **Python**
- **MATLAB**

Current analysis includes:

- BPM extraction from ECG signals  
- GSR signal processing

In future studies, we plan to derive HRV (Heart Rate Variability) metrics from ECG signals. The goal is to assess stress levels in a more detailed and reliable manner through HRV analysis.

## Example Experimental Results

The graph below shows the changes over time in a participant’s MAT task performance alongside their physiological signals. The graph illustrates how BPM and GSR signals changed throughout the experiment.

Additionally, the graph includes information regarding the participant’s MAT task performance. The following metrics are recorded:

Number of correct answers

Number of incorrect answers

Number of questions left unanswered due to time running out

These performance data, when evaluated alongside physiological signals, help analyze whether the participant was genuinely attempting to solve the questions during the task. For example, when unexpected results are observed in the physiological data, the MAT performance can be examined to assess whether the participant was sufficiently focused on the task.

The aim is to ensure the reliability and interpretability of the data obtained.

<img width="700" height="400" alt="Screenshot 2026-02-04 105117" src="https://github.com/user-attachments/assets/8bb62fa3-f95e-4530-bbf6-300772503b54" />


## Future Work

Planned future work includes:

- physiological feature extraction  
- stress classification models  
- evaluation of stress reduction interventions such as breathing exercises and music therapy  
- wearable stress monitoring systems

## Project Status

Ongoing research project.
