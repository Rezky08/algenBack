import numpy as np
import pandas as pd
import math
import sys
import copy
class rules():
    def __init__(self,nn_params):
        self.nn_params = nn_params
        self.penalty = {
            'ruang_waktu' : 1,
            'dosen_ruang_waktu' : 1,
            'sks':1
        }


    def check_sks(self,chromosom):
        sks_score = 0
        chromosom_translate = []
        sesi_simplified = map(lambda x:x['sesi_mulai'],self.nn_params['sesi'])
        sesi_simplified = list(sesi_simplified)
        for item in chromosom:
            chromosom_translate.append(copy.deepcopy(self.nn_params['ruang_waktu'][item]))

        for index,item in enumerate(chromosom_translate):
            sks =self.nn_params['mata_kuliah'][index]['sks_matkul']
            sks-=1
            sesi_loc = np.where(np.array(sesi_simplified) == item['sesi']['sesi_mulai'])[0][0]

            # get sesi_selesai by sks_matkul
            try:
                sesi_selesai = sesi_loc+sks
                chromosom_translate[index]['sesi']['sesi_selesai'] = copy.deepcopy(self.nn_params['sesi'][sesi_selesai]['sesi_selesai'])

            except:
                sks_score+=1

        for index,item in enumerate(chromosom_translate):
            for inner_index,inner_item in enumerate(chromosom_translate):
                if inner_index == index:
                    continue
                if item['ruang']==inner_item['ruang'] and item['hari']==inner_item['hari']:
                    if item['sesi']['sesi_mulai']<inner_item['sesi']['sesi_mulai'] and item['sesi']['sesi_selesai']>inner_item['sesi']['sesi_mulai']:
                        sks_score += 1
                        break
        return sks_score


    def check_ruang_waktu(self,chromosom):
        """
        tidak boleh ada ruang waktu yang bentrok
        :return:
        """
        ruang_waktu_score = 0
        ruang_waktu_unique,ruang_waktu_counts = np.unique(chromosom,return_counts=True)
        fails = np.where(ruang_waktu_counts>1)
        ruang_waktu_score = len(fails[0])
        return ruang_waktu_score

    def check_dosen_ruang_waktu(self,chromosom):
        dosen_ruang_waktu_score = 0
        kode_dosen = map(lambda x:x['kode_dosen'],self.nn_params['mata_kuliah'])
        kode_dosen_ruang_waktu = []
        for index,item in enumerate(kode_dosen):
            kode_dosen_ruang_waktu.append(tuple([item,chromosom[index]]))
        kode_dosen_ruang_waktu_unique,kode_dosen_ruang_waktu_counts = np.unique(kode_dosen_ruang_waktu,return_counts=True,axis=0)
        fails = np.where(kode_dosen_ruang_waktu_counts>1)
        dosen_ruang_waktu_score = len(fails[0])
        return  dosen_ruang_waktu_score

    def calculate_chromosom(self,chromosom):
        """
        formulas = 1 / (1+(penalty1 * num_penalty1)+...+(penaltyn * num_penaltyn))
        :return:
        """

        num_penalty = {}
        sum_penalty = 0

        for k in self.penalty.keys():
            num_penalty[k] = 0

        num_penalty['ruang_waktu'] = self.check_ruang_waktu(chromosom)
        num_penalty['dosen_ruang_waktu'] = self.check_dosen_ruang_waktu(chromosom)
        num_penalty['sks'] = self.check_sks(chromosom)
        for k in self.penalty:
            sum_penalty += (self.penalty[k] * num_penalty[k])
        chromosom_score = 1 / (1+sum_penalty)
        return chromosom_score

    def calculate_pop(self,population):
        population_score = []
        for pop in population:
            score = self.calculate_chromosom(pop)
            population_score.append(score)
        return population_score
