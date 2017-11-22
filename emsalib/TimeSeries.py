import matplotlib
from .TimeSample import TimeSample
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate, fftpack

class TimeSeries:
    y = []
    ts = []
    ys = []

    def __init__(self, **kwargs):
        self.ts = kwargs.get('ts',[])
        self.ys = kwargs.get('ys',[])
        self.convertRaw()

    def zeroMean(self):
        self.ys = self.ys - np.mean(self.ys)
        self.convertRaw()

    def convertRaw(self):
        self.y = []
        for i in range(len(self.ts)):
            self.y.append(TimeSample(self.ts[i], self.ys[i]))

    def labelPeakValley(self):
        search_order = 5
        peaks_idx = np.array(signal.argrelmax(self.ys, order=search_order))
        valleys_idx = np.array(signal.argrelmin(self.ys, order=search_order))

        peaks_t = self.ts[peaks_idx]
        valleys_t = self.ts[valleys_idx]
        peaks = self.ys[peaks_idx]
        valleys = self.ys[valleys_idx]

    def resample(self):
        fs = 33
        ps = 1 / fs
        n = np.int16(8192)
        freq = np.linspace(0, fs / 2, num=int(n // 2))
        ts_new = np.arange(min(self.ts), max(self.ts), ps)
        ys_interpolant = interpolate.interp1d(self.ts, self.ys)
        ys_new = ys_interpolant(ts_new)
        self.ts = ts_new
        self.ys = ys_new
        self.convertRaw()

    def plot(self, tstart=0, tend=None):
        plt.plot([yi.t for yi in self.y[tstart:tend]], [yi.y for yi in self.y[tstart:tend]])
        plt.grid()

    def genRandom(self, length):
        self.ts = np.array(range(length))
        self.ys = np.array(np.random.randn(length))
        self.convertRaw()

    def __str__(self):
        return str(self.ts[0:10]) + str(self.ys[0:10])