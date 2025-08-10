# Serpent-Results-Reader-GuiPy-PyQT5
A PyQt5-based GUI application to visualize Serpent Monte Carlo reactor simulation results using Octave scripts. Supports plotting burnup-dependent nuclide densities, neutron flux spectra, and keff evolution with interactive graphs and export options.
# Serpent-Results-Reader-GuiPy

**Serpent-Results-Reader-GuiPy** is a Python-based graphical user interface (GUI) application built with **PyQt5** and **matplotlib**, designed to visualize result data from **SERPENT** Monte Carlo reactor simulations via **Octave scripts (.m files)**.

The tool enables researchers and students in nuclear engineering to easily plot and analyze key reactor physics parameters like atomic densities, neutron flux spectra, capture/fission/production rates, and keff evolution.

---

## 🚀 Features

- 📂 Load and execute Octave `.m` result files
- 📊 Plot **atomic density vs. burnup**
- 🔁 Plot **Keff vs. burnup**
- 📈 Plot:
  - Neutron flux per lethargy (semilog-x)
  - Differential spectra (capture, fission, production) (log-log)
  - Integral spectra (absorption, production) (semilog-x)
- 💾 Save plots as `.png`, `.jpg`, `.pdf`
- 📑 Multi-page UI: MainWindow, Page2 (Keff), Page3 (Flux and Spectra)

---

## 🧩 Requirements

Before running the application, make sure you have the following installed:

### 🐍 Python Libraries

```bash
pip install PyQt5 matplotlib oct2py octave
git clone https://github.com/emilmammadzada99/Serpent-Results-Reader-GuiPy-PyQT5.git
cd Serpent-Results-Reader-GuiPy 
python3 serpentresultgui.py
```
## Screenshots

Here is the main window of the application:

![Main Window](Capture.PNG)
![Main Window2](Capture-1.PNG)
![Main Window3](Capture-2.PNG)
![Main Window4](Capture-3.PNG)
![Main Window5](Capture-4.PNG)

## Credits & References

This project uses and is inspired by the following resources:

- [Serpent Monte Carlo Reactor Physics Code](https://serpent.vtt.fi/)
- [GNU Octave - High-level programming language for numerical computations](https://octave.org/)
- [Python Programming Language](https://www.python.org/)
- [Real Python: Qt Designer and Python Integration Tutorial](https://realpython.com/qt-designer-python/)

