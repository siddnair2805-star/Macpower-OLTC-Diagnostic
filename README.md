#### &#x20;**IoT-Enabled Intelligent Fault Diagnostic System for OLTCs**



An end-to-end predictive maintenance solution tailored for Macpower 11kV On-Load Tap Changers (OLTC). This project digitizes standard mechanical maintenance schedules into a proactive, data-driven IoT framework.



&#x20;📁 **Project Architecture**

\* `app.py`: Interactive Streamlit analytics dashboard for customers and fleet managers.

\* `oltc\_edge\_code.ino`: C++ firmware for the ESP32 microcontroller utilizing hardware interrupts to track mechanical operation counts and time transitions.

\* `documentation/`: Field nameplates and circuit panels from Macpower used for baseline validation.



&#x20;💡 **How It Works**

1\.  Edge Counting: The ESP32 tracks every tap operation using non-invasive contactor state tracking and saves the total permanently to EEPROM memory.

2\.  Anomalous Defect Detection: The microcontroller calculates the time duration of each tap cycle. If a cycle exceeds 4 seconds, it flags an internal "Mechanical Sluggishness" defect.

3\.  Real-Time Visualization: The system passes data to a web/mobile UI built with Streamlit, cross-referencing the 10,000-operation maintenance limit specified on the factory nameplate.



&#x20;⚙️ **How to Run the Dashboard Prototype**



&#x20;   Prerequisites:

&#x09;Ensure you have Python installed on your system. Open your terminal or Command Prompt and install the necessary dependencies:

&#x09;```bash

&#x09;pip install streamlit pandas matplotlib

