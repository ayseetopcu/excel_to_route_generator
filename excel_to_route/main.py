import pandas as pd
import numpy as np
import random
import os
import sys
import datetime
import openpyxl


# Rota Dosyası Oluşturucu Sınıfı
class RouteFileGenerator:
    def __init__(self, df):
        self.df = df
        self.sort_df('SysDate')  # DataFrame'i 'SysDate' sütununa göre sıralayın
        self.dfLast = pd.DataFrame(columns=['id', 'type', 'depart', 'from', 'to'])
        self.index = 0
        self.start_range = 0
        self.end_range = 300
        self.last_date = self.df['SysDate'].iloc[0]
        self.temp_random_depart_list = np.random.randint(low=self.start_range, high=self.end_range,
                                                         size=self.get_total_vehicles())
        self.car_id = 0
        self.moto_id = 0
        self.truck_id = 0
        self.van_id = 0

    def sort_df(self, column_name):
        self.df = self.df.sort_values(by=column_name)

    def get_total_vehicles(self):
        self.car = self.df[self.df.SysDate == self.last_date]['Car'].sum()
        self.motorcycle = self.df[self.df.SysDate == self.last_date]['Motorcycle'].sum()
        self.truck = self.df[self.df.SysDate == self.last_date]['Truck'].sum() + \
                     self.df[self.df.SysDate == self.last_date]['Van'].sum()
        self.total = self.car + self.motorcycle + self.truck
        return self.total

    def run(self):
        for index, row in self.df.iterrows():
            if row['SysDate'] != self.last_date:
                self.last_date += pd.Timedelta(minutes=5)
                self.start_range += 300
                self.end_range += 300
                self.temp_random_depart_list = np.random.randint(low=self.start_range, high=self.end_range,
                                                                 size=self.get_total_vehicles())

            if row['Car'] > 0:
                for i in range(row['Car']):
                    temp_df = pd.DataFrame({'id': f'Car{self.car_id}', 'type': 'Car',
                                            'depart': random.choice(self.temp_random_depart_list),
                                            'from': row['ComingRouteId'], 'to': row['GoingRouteId']}, index=[0])
                    self.dfLast = pd.concat([self.dfLast, temp_df], ignore_index=True)
                    self.car_id += 1

            if row['Motorcycle'] > 0:
                for i in range(row['Motorcycle']):
                    temp_df = pd.DataFrame({'id': f'Motorcycle{self.moto_id}', 'type': 'Motorcycle',
                                            'depart': random.choice(self.temp_random_depart_list),
                                            'from': row['ComingRouteId'], 'to': row['GoingRouteId']}, index=[0])
                    self.dfLast = pd.concat([self.dfLast, temp_df], ignore_index=True)
                    self.moto_id += 1
            
            if row['Truck'] > 0:
                for i in range(row['Truck']):
                    temp_df = pd.DataFrame({'id': f'Truck{self.truck_id}', 'type': 'Truck',
                                            'depart': random.choice(self.temp_random_depart_list),
                                            'from': row['ComingRouteId'], 'to': row['GoingRouteId']}, index=[0])
                    self.dfLast = pd.concat([self.dfLast, temp_df], ignore_index=True)
                    self.truck_id += 1

            if row['Van'] > 0:
                for i in range(row['Van']):
                    temp_df = pd.DataFrame({'id': f'Van{self.van_id}', 'type': 'Truck',
                                            'depart': random.choice(self.temp_random_depart_list),
                                            'from': row['ComingRouteId'], 'to': row['GoingRouteId']}, index=[0])
                    self.dfLast = pd.concat([self.dfLast, temp_df], ignore_index=True)
                    self.van_id += 1

        a = self.dfLast.sort_values(by='depart')  # DataFrame'i 'depart' sütununa göre sırala
        with open("C:/Users/ayses/OneDrive/Masaüstü/proje dosyası/routes/Kilis_7913.rou.xml", "w") as r:
            print("<?xml version='1.0' encoding='UTF-8'?>", file=r)
            print(
                '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">',
                file=r)
            print('<vType id="Motorcycle" vClass="motorcycle"/> ', file=r)
            print('<vType id="Car" vClass="passenger"/>', file=r)
            print('<vType id="Truck" vClass="truck"/>', file=r)
            for index, row in a.iterrows():
                random_color = '{},{},{}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                print(
                    f'\t<trip id="{str(row["id"])}" type="{row["type"]}" depart="{row["depart"]}" departLane'
                    f'="best" departSpeed="avg" color="{random_color}" from="{row["from"]}_0" to="{row["to"]}_1"/>',
                    file=r)
            print("</routes>", file=r)
        print('Toplam Arabalar: ', self.car_id)
        print('Toplam Motorsikletler: ', self.moto_id)
        print('Toplam Kamyonlar: ', self.truck_id)
        print('Toplam Minibüsler: ', self.van_id)
        print('Toplam Araçlar: ', self.car_id + self.moto_id + self.truck_id + self.van_id)
        print('Bitti')
        return a



# Excel dosyasını okuyan fonksiyon
def read_excel_file(excel_file_path):
    """
    Excel dosyasını sayfa sayfa okur ve bir DataFrame nesnesi döndürür
    """
    df = pd.read_excel(excel_file_path)
    df['SysDate'] = pd.to_datetime(df['SysDate'], format='%d.%m.%Y %H:%M')
    return df.sort_values(by='SysDate')  # DataFrame'i 'SysDate' sütununa göre sıralayın


if __name__ == "__main__":
    excel_file_path = "C:/Users/ayses/OneDrive/Masaüstü/proje dosyası/excels/7913_data.xlsx"
    data_df = read_excel_file(excel_file_path)

    route_generator = RouteFileGenerator(data_df)
    route_generator.run()
