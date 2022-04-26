# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
import japanize_matplotlib
plt.rcParams["font.family"] = "MS Gothic" #フォントを日本語対応に
from pathlib import Path


class PlotDataReader(object):
    def __init__(self, path,encoding):
        self.freqs = []
        self.titles = []
        self.data = {}
        self.encoding = encoding
        self.path = Path(path)
        #assert self.path.exists(), f"[error] text file does not exist: {self.path}"
        self.load_txt(self.path)

        self.construction_analysis()

    def load_txt(self, path):
        with open(path, "r",encoding = self.encoding) as r:
            self.txt = r.read()

        self.lines = list(self.txt.strip().split("\n"))
        self.lines_num = len(self.lines)

    def construction_analysis(self):
        self.__analysis_header()
        self.__analysis_body()

    def __analysis_header(self):
        self.header = self.lines[0]
        heads = list(self.header.split("\t"))
        self.head_num = len(heads) - 1
        self.titles = heads[1:]
        assert len(self.titles) == self.head_num
        self.data = {title: [] for title in self.titles}

    def __analysis_body(self):
        body = self.lines[1:]
        for b in body:
            self.__analysis_line(b)

    def __analysis_line(self, line):
        data = list(line.split("\t"))
        if len(data) != len(self.titles) + 1:
            return

        self.freqs.append(float(data[0]))

        for (title, data_str) in zip(self.titles, data[1:]):
            db, th = [float(d) for d in data_str[1:-2].split("dB,")]
            self.data[title] += [(db, th)]
  
    def get_key(self, key):
        assert key in self.titles

        return self.data[key]

    def get_key_db(self, key):
        assert key in self.titles

        return [db for (db, _) in self.data[key]]

    def get_key_phase(self, key):
        assert key in self.titles

        return [th for (_, th) in self.data[key]]

# reader = PlotDataReader("./butterworth_chebyshev.txt")
reader = PlotDataReader("example.txt",encoding="shift_jis")
# グラフの描画

T = 5000

fig = plt.figure()

ax = fig.add_subplot(111)
ax.plot(reader.freqs, reader.get_key_db("V(n002)"), color="b", label="エネルギー特性[dB]")#V(n00?)を書き換え

ax.set_title("butterworth")
ax.set_ylabel("伝達特性[dB]")
ax.set_xlabel("周波数[Hz]")
