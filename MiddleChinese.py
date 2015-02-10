# Johann-Mattis List, January 2010

from MiddleChineseData import *
from re import sub

class Wang(object):
        """Wang class for conversion of DOC into Baxter's system of Middle Chinese"""

        def __init__(self,string):

                # the try-statement is simply for differently encoded data
                try:
                        self.string = str(string)
                except:
                        self.string = string
                # Making the six-character string to attributes of the class
                if len(self.string) == 6:
                        self.she = string[0]
                        self.hu = string[1]
                        self.deng = string[2]
                        self.diao = string[3]
                        self.yun = string[4]
                        self.sheng = string[5]
                        self.quan = self.string # bad line only for testen.py
                else:
                        print("Exception! Data doesn't correspond to the expected format!")
                
                # Matching the important attributes with phonetic values
                self.initial = mch_sheng[self.sheng]
                self.final = mch_yun[self.yun]
                self.tone = mch_diao[self.diao]
                self.division = mch_deng[self.deng]
                self.medial = mch_hu[self.hu]

        def wang2baxter(self):
                """Method converts DOC-data into Baxter's MCH-spelling"""
                
                # Arranging the tones
                if self.tone == 'shangsheng':
                        TONE = 'X'
                elif self.tone == 'qusheng':
                        TONE = 'H'
                elif self.tone == 'pingsheng':
                        TONE = 'P'
                else:
                        TONE = 'R'

                # Arranging the Medials
                #if self.medial == 'kaikou':
                #       if 'y' in self.initial or 'j' in self.initial or self.final.startswith('j') or 'i' in self.final:
                #               MEDIAL = ''
                #       else:
                #               if self.division == 'sandeng':
                #                       MEDIAL = 'j'
                #               else:
                #                       MEDIAL = ''
                #else:
                #       if 'y' in self.initial or 'j' in self.initial or self.final.startswith('j') or 'i' in self.final:
                #               MEDIAL = 'w'
                #
                #else:
                #               if

                # Arranging the Medials
                if self.medial == 'kaikou':
                        if self.division != 'sandeng':
                                MEDIAL = ''
                        else:
                                MEDIAL = 'j'
                else:
                        if self.division != 'sandeng':
                                MEDIAL = 'w'
                        else:
                                MEDIAL = 'jw'

                # Arranging Initial and Final

                INITIAL = self.initial
                FINAL = self.final

                # Arranging the readings

                reading = INITIAL + MEDIAL + FINAL + TONE

                for i in range(2):
                        reading = reading.replace('jj','j')
                        reading = reading.replace('ww','w')
                        reading = reading.replace('wo','o')
                        reading = reading.replace('wu','u')
                        reading = reading.replace('yj','y')
                        reading = reading.replace('jwj','jw')
                        reading = reading.replace('ji','i')
                        reading = reading.replace('ywj','yw')
                        #reading = reading.replace('ywi','ywi')
                        reading = reading.replace('jwi','wi')
                        reading = reading.replace('yhj','yh')
                        #if '*' not in reading:
                        reading = reading.replace('pjw','pj')
                        reading = reading.replace('bjw','bj')
                        reading = reading.replace('phjw','phj')
                        reading = reading.replace('pw','p')
                        reading = reading.replace('bw','b')
                        reading = reading.replace('phw','ph')
                        reading = reading.replace('mjw','mj')
                        reading = reading.replace('mw','m')
                        reading = reading.replace('w*','*')
                                

                        #reading = reading.replace('yhj

                #if 'w' in reading and '*' in reading:
                #       reading = reading.replace('*','')
                #       print '*'
                #elif 'w' not in reading and '*' in reading:
                #       reading = reading.replace('*','w')
                #       print '*w'
                if self.medial == 'hekou' and 'p' not in self.initial and 'b' not in self.initial: # and 'm' not in self.initial:
                        reading = reading.replace('*','w')
                #elif self.medial == 'hekou':
                #       reading = reading.replace('!','w')
                else:
                        reading = reading.replace('*','')

                return reading

        def baxter2ipa(self):

            
            out = self.wang2baxter()
            for source,target in mch2ipa:
                out = out.replace(source,target)
            return out

                

