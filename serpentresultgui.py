import sys
import os
import re
from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from oct2py import Oct2Py

octave_path = r"C:\Program Files\GNU Octave\Octave-10.2.0\mingw64\bin"
os.environ["PATH"] += os.pathsep + octave_path
oc = Oct2Py()

def isotope_to_zai(isotope):
    element_dict = {
        'H':1, 'He':2, 'Li':3, 'Be':4, 'B':5, 'C':6, 'N':7, 'O':8, 'F':9, 'Ne':10,
        'Na':11, 'Mg':12, 'Al':13, 'Si':14, 'P':15, 'S':16, 'Cl':17, 'Ar':18, 'K':19, 'Ca':20,
        'Sc':21, 'Ti':22, 'V':23, 'Cr':24, 'Mn':25, 'Fe':26, 'Co':27, 'Ni':28, 'Cu':29, 'Zn':30,
        'Ga':31, 'Ge':32, 'As':33, 'Se':34, 'Br':35, 'Kr':36, 'Rb':37, 'Sr':38, 'Y':39, 'Zr':40,
        'Nb':41, 'Mo':42, 'Tc':43, 'Ru':44, 'Rh':45, 'Pd':46, 'Ag':47, 'Cd':48, 'In':49, 'Sn':50,
        'Sb':51, 'Te':52, 'I':53, 'Xe':54, 'Cs':55, 'Ba':56, 'La':57, 'Ce':58, 'Pr':59, 'Nd':60,
        'Pm':61, 'Sm':62, 'Eu':63, 'Gd':64, 'Tb':65, 'Dy':66, 'Ho':67, 'Er':68, 'Tm':69, 'Yb':70,
        'Lu':71, 'Hf':72, 'Ta':73, 'W':74, 'Re':75, 'Os':76, 'Ir':77, 'Pt':78, 'Au':79, 'Hg':80,
        'Tl':81, 'Pb':82, 'Bi':83, 'Po':84, 'At':85, 'Rn':86, 'Fr':87, 'Ra':88, 'Ac':89, 'Th':90,
        'Pa':91, 'U':92, 'Np':93, 'Pu':94, 'Am':95, 'Cm':96, 'Bk':97, 'Cf':98, 'Es':99, 'Fm':100
    }
    match = re.match(r"([A-Za-z]+)(\d+)", isotope)
    if not match:
        return None
    element, mass_number = match.groups()
    element = element.capitalize()
    if element not in element_dict:
        return None
    Z = element_dict[element]
    A = int(mass_number)
    return f"{Z}{A:03d}0"  # Eg:'922350'

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(4, 3))
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()

    def clear_plot(self):
        self.ax.cla()
        self.draw()

    def plot(self, burnup, nuc_data, isotope):
        self.clear_plot()
        self.ax.plot(burnup, nuc_data, marker='o', linestyle='-', color='b')
        self.ax.set_title(f"{isotope}")
        self.ax.set_xlabel("Burnup (BU)")
        self.ax.set_ylabel("Atomic Density")
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.grid(True)
        self.draw()

    def plot1(self, burnup, keff_data, isotope):
        self.clear_plot()
        self.ax.plot(burnup, keff_data, marker='o', color='r')
        self.ax.set_title(f"{isotope}")
        self.ax.set_xlabel("Burnup (BU)")
        self.ax.set_ylabel("K_EFF")
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.grid(True)
        self.draw()

    def plot_flux(self, x, y, title):
        self.clear_plot()
        self.ax.semilogx(x, y, color='r')
        self.ax.set_title(title)
        self.ax.set_xlabel("Neutron energy (MeV)")
        self.ax.set_ylabel("Flux per lethargy")
        self.ax.grid(True, which='both')
        self.draw()

    def plot_multiple_loglog(self, data_list, xlabel, ylabel, title):
        self.clear_plot()
        for x, y, label, color in data_list:
            self.ax.loglog(x, y, label=label, color=color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        self.ax.legend()
        self.ax.grid(True, which='both')
        self.draw()

    def plot_multiple_semilogx(self, data_list, xlabel, ylabel, title):
        self.clear_plot()
        for x, y, label, color in data_list:
            self.ax.semilogx(x, y, label=label, color=color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        self.ax.legend()
        self.ax.grid(True, which='both')
        self.draw()

    def save_plot(self, file_path):
        self.figure.savefig(file_path)

class Page2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("page2.ui", self)
        layout = QtWidgets.QVBoxLayout(self.plotWidget2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = PlotCanvas(self.plotWidget2)
        layout.addWidget(self.canvas)

        self.plotButton1.clicked.connect(self.plot_graph1)
        self.selectFileButton1.clicked.connect(self.select_octave_file1)
        self.clearPlotButton1.clicked.connect(self.canvas.clear_plot)
        self.savePlotButton1.clicked.connect(self.save_plot1)  # Kaydet butonu

        self.octave_file_path = None

    def select_octave_file1(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Octave .m Select File", "", "Octave M Files (*.m)"
        )
        if file_path:
            self.octave_file_path = file_path.replace("\\", "/")
            QtWidgets.QMessageBox.information(self, "File Selected", f"Selected file:\n{self.octave_file_path}")

    def plot_graph1(self):
        if not self.octave_file_path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select the Octave script file first.")
            return
        keff_name1 = self.nuclideInput1.text().strip()
        if not keff_name1:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter the nuclide name.")
            return
        try:
            folder = os.path.dirname(self.octave_file_path)
            file_name = os.path.basename(self.octave_file_path).replace(".m", "")
            oc.eval("clear all;")
            oc.eval(f"cd('{folder}');")
            oc.eval(f"{file_name};")
            oc.eval(f"KEF = {keff_name1}(:,1);")
            oc.eval("Burnup = BURNUP(:,1);")
            keff_data = oc.pull("KEF")
            burnup = oc.pull("Burnup")
            self.canvas.plot1(burnup, keff_data, keff_name1)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error has occurred:\n{e}")

    def save_plot1(self):
        if not self.canvas.ax.lines:
            QtWidgets.QMessageBox.warning(self, "Warning", "No graph to save was found.")
            return
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Plot Save", "",
            "PNG file (*.png);;JPEG file (*.jpg);;PDF file (*.pdf)"
        )
        if file_path:
            try:
                self.canvas.save_plot(file_path)
                QtWidgets.QMessageBox.information(self, "Successful", f"Graph successfully saved:\n{file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while saving the graph:\n{e}")
class Page3(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("page3.ui", self)

        layout = QtWidgets.QVBoxLayout(self.plotWidget3)
        layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = PlotCanvas(self.plotWidget3)
        layout.addWidget(self.canvas)

        self.selectFileButton2.clicked.connect(self.select_octave_file2)
        self.clearPlotButton2.clicked.connect(self.canvas.clear_plot)
        self.savePlotButton2.clicked.connect(self.save_plot2)

        self.plotButton2_1.clicked.connect(self.plot_graph1_1)
        self.plotButton2_2.clicked.connect(self.plot_graph2_1)
        self.plotButton3_3.clicked.connect(self.plot_graph3_1)

        self.octave_file_path = None

    def select_octave_file2(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Octave .m File", "", "Octave M Files (*.m)"
        )
        if file_path:
            self.octave_file_path = file_path.replace("\\", "/")
            QtWidgets.QMessageBox.information(self, "File Selected", f"Selected file:\n{self.octave_file_path}")

    def run_octave_script(self):
        if not self.octave_file_path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select the Octave script file first.")
            return False
        try:
            folder = os.path.dirname(self.octave_file_path)
            file_name = os.path.basename(self.octave_file_path).replace(".m", "")
            oc.eval("clear all;")
            oc.eval(f"cd('{folder}');")
            oc.eval(f"{file_name};")
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run Octave script:\n{e}")
            return False

    def plot_graph1_1(self):
        if not self.run_octave_script():
            return
        try:
            x = oc.pull("DET1E")[:, 2]   # Octave 1-based index, Python 0-based, 3.sütun = 2.indeks
            y = oc.pull("DET1")[:, 10]   # 11.sütun = 10.indeks
            self.canvas.plot_flux(x, y, "Neutron flux per lethargy")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error plotting graph 1:\n{e}")

    def plot_graph2_1(self):
        if not self.run_octave_script():
           return
        try:
           x1 = oc.pull("DET2E")[:, 2]
           y1 = oc.pull("DET2")[:, 10]

           x2 = oc.pull("DET3E")[:, 2]
           y2 = oc.pull("DET3")[:, 10]

           x3 = oc.pull("DET4E")[:, 2]
           y3 = oc.pull("DET4")[:, 10]

           self.canvas.plot_multiple_loglog(
               [
                  (x1, y1, 'Capture', 'blue'),
                  (x2, y2, 'Fission', 'green'),
                  (x3, y3, 'Production', 'red')
               ],
               xlabel="Neutron energy (MeV)",
               ylabel="Rate per energy",
               title="Differential capture, fission and production spectra"
        )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error plotting graph 2:\n{e}")

    def plot_graph3_1(self):
       if not self.run_octave_script():
          return
       try:
           x1 = oc.pull("DET5E")[:, 2]
           y1_det5 = oc.pull("DET5")[:, 10]
           y1_det6 = oc.pull("DET6")[:, 10]
           y1 = y1_det5 + y1_det6

           x2 = oc.pull("DET7E")[:, 2]
           y2 = oc.pull("DET7")[:, 10]

           self.canvas.plot_multiple_semilogx(
              [
                 (x1, y1, 'Absorption (capt. + fiss.)', 'purple'),
                 (x2, y2, 'Production', 'orange')
              ],
              xlabel="Neutron energy (MeV)",
              ylabel="Rate per energy (cumulative)",
              title="Integral absorption and production spectra"
            )
       except Exception as e:
           QtWidgets.QMessageBox.critical(self, "Error", f"Error plotting graph 3:\n{e}")

    def save_plot2(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Plot As", "", "PNG Files (*.png);;JPEG Files (*.jpg);;PDF Files (*.pdf)"
        )
        if file_path:
            self.canvas.figure.savefig(file_path)
            QtWidgets.QMessageBox.information(self, "Saved", f"Plot saved to:\n{file_path}")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        layout = QtWidgets.QVBoxLayout(self.plotWidget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = PlotCanvas(self.plotWidget)
        layout.addWidget(self.canvas)

        self.plotButton.clicked.connect(self.plot_graph)
        self.selectFileButton.clicked.connect(self.select_octave_file)
        self.openPage2Button.clicked.connect(self.open_second_page)
        self.openPage3Button.clicked.connect(self.open_third_page)
        self.clearPlotButton.clicked.connect(self.canvas.clear_plot)
        self.savePlotButton.clicked.connect(self.save_plot)  # Save button
        
        self.octave_file_path = None

    def open_second_page(self):
        self.page2 = Page2()
        self.page2.show()
    def open_third_page(self):
        self.page3 = Page3()
        self.page3.show()
    def select_octave_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Octave .m Select File", "", "Octave M Files (*.m)"
        )
        if file_path:
            self.octave_file_path = file_path.replace("\\", "/")
            QtWidgets.QMessageBox.information(self, "File Selected", f"Selected File:\n{self.octave_file_path}")

    def plot_graph(self):
        if not self.octave_file_path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select the Octave script file first.")
            return
        isotope_name = self.nuclideInput.text().strip()
        if not isotope_name:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter the nuclide name.")
            return
        zai_code = isotope_to_zai(isotope_name)  # Örnek '922350'
        if zai_code is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "You entered an invalid nuclide name.")
            return
        octave_var = f"i{zai_code}"
        try:
            folder = os.path.dirname(self.octave_file_path)
            file_name = os.path.basename(self.octave_file_path).replace(".m", "")
            oc.eval(f"cd('{folder}');")
            oc.eval(f"{file_name};")
            idx = oc.pull(octave_var)
            if idx is None:
                QtWidgets.QMessageBox.warning(self, "Warning", f"{isotope_name} Index not found in Octave.")
                return
            oc.eval(f"NUC = TOT_ADENS({int(idx)},:);")
            oc.eval("Burnup = BU;")
            nuc_data = oc.pull("NUC")
            burnup = oc.pull("Burnup")
            self.canvas.plot(burnup, nuc_data, isotope_name)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An has occurred error:\n{e}")

    def save_plot(self):
        if not self.canvas.ax.lines:
            QtWidgets.QMessageBox.warning(self, "Warning", "No graph to save was found.")
            return
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Saved Plot", "",
            "PNG File (*.png);;JPEG File (*.jpg);;PDF File (*.pdf)"
        )
        if file_path:
            try:
                self.canvas.save_plot(file_path)
                QtWidgets.QMessageBox.information(self, "Successful", f"Graph successfully saved:\n{file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while saving the graph:\n{e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
