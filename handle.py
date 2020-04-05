import json
import pandas as pd
import numpy as np
from dosen.pembagi_kelompok import pembagi_kelompok
from dosen.algen_only_dosen import algen_only_dosen
from mata_kuliah.algen_matkul import algen_matkul
import sys

class handle:
    def __init__(self,requests:dict):
        self.requests = requests

    def response(self):
        pass
    def kelompok(self):
        # get kelompok of matkul
        peminat_params = self.requests['peminat_params']
        peminat_props = self.requests['peminat_props']
        bagi_kelompok = pembagi_kelompok(peminat_params, peminat_props)
        bagi_kelompok = bagi_kelompok.bagi_kelompok()

        # get dosen by matkul

        return bagi_kelompok

    def dosen(self):
        nn_params = {
            'mata_kuliah' : self.requests['nn_params']['mata_kuliah'],
            'matkul_dosen': pd.DataFrame(self.requests['nn_params']['matkul_dosen']).to_dict(orient='list')
        }
        rules = self.requests['rules']
        num_generation = self.requests['num_generation']
        num_population = self.requests['num_population']
        crossover_rate = self.requests['crossover_rate']
        mutation_rate = self.requests['mutation_rate']
        timeout = self.requests['timeout']

        algen = algen_only_dosen(nn_params,rules,num_generation,num_population,crossover_rate,mutation_rate,timeout)
        max_chromosom,fit_score,running_time = algen.run_generation()
        results = []
        for index,chromosom in enumerate(max_chromosom):
            result = {
                'data': chromosom,
                'fit_score': fit_score[index]
            }
            results.append(result)
        response  = {
                'status' : 200,
                'time'  : running_time,
                'results': results
            }
        return response
    def jadwal(self):
        # rules = self.requests['rules']
        nn_params = self.requests['nn_params']

        ruang_waktu = []
        for ruang_item in self.requests['nn_params']['ruang']:
            for hari_item in self.requests['nn_params']['hari']:
                for sesi_item in self.requests['nn_params']['sesi']:
                    combine ={
                        'ruang' : ruang_item,
                        'hari' : hari_item,
                        'sesi' : sesi_item
                    }
                    ruang_waktu.append(combine)

        nn_params['ruang_waktu'] = ruang_waktu
        num_generation = self.requests['num_generation']
        num_population = self.requests['num_population']
        crossover_rate = self.requests['crossover_rate']
        mutation_rate = self.requests['mutation_rate']
        timeout = self.requests['timeout']
        algen = algen_matkul(nn_params, num_generation, num_population, crossover_rate, mutation_rate,
                                 timeout)
        max_chromosom, fit_score, running_time = algen.run_generation()
        results = []
        for index, chromosom in enumerate(max_chromosom):
            result = {
                'data': chromosom,
                'fit_score': fit_score[index]
            }
            results.append(result)
        response = {
            'status': 200,
            'time': running_time,
            'results': results
        }
        return response

    def dosen_dummy(self):
        nn_params = {
            'mata_kuliah' : self.requests['nn_params']['mata_kuliah'],
            'matkul_dosen': self.requests['nn_params']['matkul_dosen']
        }

        rules = self.requests['rules']
        num_generation = self.requests['num_generation']
        num_population = self.requests['num_population']
        crossover_rate = self.requests['crossover_rate']
        mutation_rate = self.requests['mutation_rate']
        timeout = self.requests['timeout']

        dummy = pd.read_csv('dosen/result/result_1.0.csv',index_col=0)
        dummy_dict = dummy.to_dict(orient='record')
        results = []
        for index in range(3):
            result = {
                'data': dummy_dict,
                'fit_score': 1
            }
            results.append(result)
        response = {
            'status': 200,
            'results': results
        }
        return response
