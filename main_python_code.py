import numpy as np
import pandas as pd
import os

# Контейнер для данных
class ModelContainer:
    def __init__(self):
        self.sets = {}
        self.parameters = {}

    def add_set(self, name, records, description=""):
        self.sets[name] = {
            "records": records,
            "description": description
        }

    def add_parameter(self, name, domain, description=""):
        self.parameters[name] = {
            "domain": domain,
            "values": None,
            "description": description
        }

    def set_values(self, name, values):
        if name in self.parameters:
            self.parameters[name]["values"] = values
        else:
            raise KeyError(f"Parameter {name} not found.")

# Инициализация контейнера модели
m = ModelContainer()

# Определение наборов данных (аналог Set в gamspy)
sam_columns = ["Sector1", "Sector2", "CAP", "LAB"]  # Пример
m.add_set("u", records=sam_columns, description="SAM entry")
m.add_set("i", records=[str(i) for i in range(1, 4)], description="goods")
m.add_set("h", records=["CAP", "LAB"], description="factor")
m.add_set("h_mob", records=["LAB"], description="mobile factor")
m.add_set("t", records=[str(i) for i in range(11)], description="time")

# Определение параметров (аналог Parameter в gamspy)
params = [
    "Y00", "F00", "X00", "Z00", "Xp00", "Xg00", "Xv00", "E00", "M00", "Q00", "D00", "Sp00", "Td00",
    "Tz00", "Tm00", "III00", "II00", "KK00", "CC00", "FF00", "Sf00", "tauz00", "taum00", "Y0", "F0", "X0",
    "Z0", "Xp0", "Xv0", "E0", "M0", "Q0", "D0", "Sp0", "Td0", "Tz0", "Tm0", "III0", "II0", "KK0", "CC0",
    "FF0", "pf0", "py0", "pz0", "pq0", "pe0", "pm0", "pd0", "pk0", "epsilon0", "PRICE0", "ror", "dep", "pop", "zeta",
    "SAM", "SAMGAP"
]
for param in params:
    m.add_parameter(param, domain=[], description=param)

# Установка значений для некоторых параметров
m.set_values("ror", 0.05)
m.set_values("dep", 0.04)
m.set_values("pop", 0.02)
m.set_values("zeta", 1)

current_path = os.path.abspath(os.path.dirname(__file__))
sam_path = os.path.join(current_path, "data", "databank_2017_type1_common_HOH.xlsx")
sam_df = pd.read_excel(sam_path, sheet_name="shortened", index_col=0, header=0)

m.set_values("SAM", sam_df)

# Вычисление разницы между строками и столбцами SAM (аналог вычисления SAMGAP)
row_sums = sam_df.sum(axis=1)
col_sums = sam_df.sum(axis=0)
SAMGAP = row_sums - col_sums
m.set_values("SAMGAP", SAMGAP)

print("SAMGAP:")
print(SAMGAP)