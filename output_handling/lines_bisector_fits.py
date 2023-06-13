import numpy as np
import os
home_dir = os.environ['HOME'] + '/'
import pyCloudy as pc
from astropy.table import Table, hstack


zone = 'HII_PDR'

# # The directories in which we will have the models
# #dir_HII = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_grains/'
# #dir_HII = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_grains_reduced/'
# dir_HII = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_grains_full/'
# model_name_HII = 'model_HII'
# #dir_HII_nograin = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_nograin/'
# #dir_HII_nograin = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_nograin_reduced/'
# dir_HII_nograin = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_nograin_full/'
# model_name_HII_nograin = 'model_HII'
# #dir_HII_PDR = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_PDR/'
# #dir_HII_PDR = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/models_HII_PDR_reduced/'
dir_HII_PDR = '/Users/serenac/Desktop/research/PRIMA/cloudy_prima/'
model_name_HII_PDR = 'model_HII_PDR'



# setting verbosity to medium level, change to 3 for high verbosity
pc.log_.level = 1

# reading the Cloudy outputs and putting them in a list of CloudyModel objects
# Ms = pc.load_models('{0}{1}'.format(dir_HII, model_name_HII), read_grains = False)
# Ms_nograin = pc.load_models('{0}{1}'.format(dir_HII_nograin, model_name_HII_nograin), read_grains = False)
Ms_HII_PDR = pc.load_models('{0}{1}'.format(dir_HII_PDR, model_name_HII_PDR), read_grains = False)


# read linelist_HII_AGN.text
line_list_name = []
line_list_wl = []
line_index =[]


def extract_parameters(modelname) :
    
    en_tete ='{0}{1}'.format(dir_HII_PDR, model_name_HII_PDR) + '_'
    if modelname.startswith(en_tete):
        chaine_paremetres = modelname.replace(en_tete, '')     
    x = chaine_paremetres.partition('_')  
    if x[0] == 'PDR' :
        chaine_paremetres = x[2]
        x = chaine_paremetres.partition('_')
    metallicite=float(x[0])
    chaine_paremetres = x[2]
    x = chaine_paremetres.partition('_')
    densite=float(x[0])
    chaine_paremetres = x[2]
    x = chaine_paremetres.partition('_')
    intensite=float(x[0])
    chaine_paremetres = x[2]
    parametres= [metallicite,densite,intensite]
    return parametres

tab_dzetaO = [] # the metallicity
tab_density = []
tab_logU = []


for M in Ms :   
    parametres_lus= extract_parameters(M.model_name)
    tab_dzetaO.append(parametres_lus[0])
    tab_density.append(parametres_lus[1])
    tab_logU.append(parametres_lus[2])

tab_dzetaO=list(dict.fromkeys(tab_dzetaO))
tab_dzetaO.sort()
tab_density=list(dict.fromkeys(tab_density))
tab_density.sort()
tab_logU=list(dict.fromkeys(tab_logU))
tab_logU.sort()

"""
# or
tab_dzetaO = [-2.0,-1.5,-1.0,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05, 0.0, 0.05, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
tab_dzetaO.sort()
# metallicity BC03 Z=[0.051, 0.022, 0.008, 0.004, 0.0004, 0.0001] <-> [0.50, 0.15, -0.20, -0.50, -1.5, -2.0]
tab_density = [1.0, 2.0, 3.0]#  [3.0] #
tab_density.sort()
tab_logU = [-1.0,-1.1,-1.2,-1.3,-1.4,-1.5,-1.6,-1.7,-1.8,-1.9,-2.0,-2.1,-2.2,-2.3,-2.4,-2.5,-2.6,-2.7,-2.8,-2.9,-3.0,-3.1,-3.2,-3.3,-3.4,-3.5,-3.6,-3.7,-3.8,-3.9,-4.0]
tab_logU.sort()


tab_dzetaO = [0.0]
tab_dzetaO.sort()
# metallicity BC03 Z=[0.051, 0.022, 0.008, 0.004, 0.0004, 0.0001] <-> [0.50, 0.15, -0.20, -0.50, -1.5, -2.0]
tab_density = [1.0]#  [3.0] #
tab_density.sort()
tab_logU = [-1.2,-1.1,-1.0]
tab_logU.sort()
"""

print('model parameters available')
print('dzetaO=', tab_dzetaO, len(tab_dzetaO), ' metallicities')
print('density=', tab_density, len(tab_density), 'densities')
print('logU=', tab_logU, len(tab_logU), 'ionization parameters')

#===============================================================================================

def change_metallicity(zeta) :
   if zeta == -3.0 : 
        Zm = 0.00001
   elif zeta == -2.0 : 
        Zm = 0.0001
   elif zeta == -1.5 :
        Zm = 0.0004
   elif zeta == -1.0 :
        Zm = 0.001
   elif zeta == -0.8 :
        Zm = 0.002
   elif zeta == -0.7 :
        Zm = 0.0025
   elif zeta == -0.6 :
        Zm = 0.003
   elif zeta == -0.5 :
        Zm = 0.004
   elif zeta == -0.4 :
        Zm = 0.005
   elif zeta == -0.3 :
        Zm = 0.006
   elif zeta == -0.25 :
        Zm = 0.007
   elif zeta == -0.2 :
        Zm = 0.008
   elif zeta == -0.15 :
        Zm = 0.009
   elif zeta == -0.1 :
        Zm = 0.011
   elif zeta == -0.05 :
        Zm = 0.012
   elif zeta == 0.0 :
        Zm = 0.014
   elif zeta == 0.05 :
        Zm = 0.016
   elif zeta == 0.10 :
        Zm = 0.019
   elif zeta == 0.12 :
        Zm = 0.02
   elif zeta == 0.15 :
        Zm = 0.022
   elif zeta == 0.20 :
        Zm = 0.025
   elif zeta == 0.25 :
        Zm = 0.030
   elif zeta == 0.30 :
        Zm = 0.033
   elif zeta == 0.35 :
        Zm = 0.037
   elif zeta == 0.40 :
        Zm = 0.041
   elif zeta == 0.45 :
        Zm = 0.046
   elif zeta == 0.50 :
        Zm = 0.051
   else :
       print('problem with metallicity')              
   return Zm

#===============================================================================================
# generate the CIGALE line_wavelengths.dat file, where all the wavelengths are in nm

def change_label(old_label, lbda) :
    new_label=old_label[0:5]
    new_label=new_label.replace('1','I')
    new_label=new_label.replace('2','II')
    new_label=new_label.replace('3','III')
    new_label=new_label.replace('4','IV')
    new_label=new_label.replace('5','V')
    new_label=new_label.replace('6','VI')
    new_label=new_label.replace('7','VII')
    new_label=new_label.replace('10','X')
    new_label=new_label.replace('14','XIV')
    new_label=new_label.replace(' ','')
    new_label=new_label.replace('R','')
    if lbda < 100.0 :
       new_label=new_label+'-'+str("%5.2f" %lbda)
    elif lbda < 1000.0 :
       new_label=new_label+'-'+str("%5.1f" %lbda)
    elif lbda < 100000.0 :
       new_label=new_label+'-'+str("%5.2f" %(lbda/1000))
    else:
       new_label=new_label+'-'+str("%5.1f" %(lbda/1000)) 
    new_label=new_label.replace('HI-97.25','Ly-gamma')
    new_label=new_label.replace('HI-102.6','Ly-beta')
    new_label=new_label.replace('HI-121.6','Ly-alpha')
    new_label=new_label.replace('SiIV-139.4','SiIV-139.7')
    new_label=new_label.replace('CaB-371.2','H-15')
    new_label=new_label.replace('CaB-372.2','H-14')
    new_label=new_label.replace('HI-379.8','H-10')
    new_label=new_label.replace('HI-383.5','H-9')
    new_label=new_label.replace('HI-388.9','H-8')
    new_label=new_label.replace('HI-397.0','H-epsilon')
    new_label=new_label.replace('HI-410.2','H-delta')
    new_label=new_label.replace('HI-434.0','H-gamma')
    new_label=new_label.replace('HI-486.1','H-beta')
    new_label=new_label.replace('HI-656.3','H-alpha')
    new_label=new_label.replace('NII-658.3','NII-658.4')
    new_label=new_label.replace('HI-901.5','Pa-10')
    new_label=new_label.replace('HI-922.9','Pa-9')
    new_label=new_label.replace('HI-954.6','Pa-epsilon')
    new_label=new_label.replace('HI- 1.00','Pa-delta')
    new_label=new_label.replace('HI- 1.09','Pa-gamma')
    new_label=new_label.replace('HI- 1.28','Pa-beta')
    new_label=new_label.replace('HI- 1.88','Pa-alpha')
    new_label=new_label.replace('HI- 1.74','Br-10')
    new_label=new_label.replace('HI- 1.82','Br-epsilon')
    new_label=new_label.replace('HI- 1.94','Br-delta')
    new_label=new_label.replace('HI- 2.17','Br-gamma')
    new_label=new_label.replace('HI- 2.63','Br-beta')
    new_label=new_label.replace('HI- 4.05','Br-alpha')
    new_label=new_label.replace('HI- 3.30','Pf-delta')
    new_label=new_label.replace('HI- 3.74','Pf-gamma')
    new_label=new_label.replace('HI- 4.65','Pf-beta')
    new_label=new_label.replace('HI- 7.46','Pf-alpha')
    new_label=new_label.replace('OIII-166.6','OIII-166.5')
    new_label=new_label.replace('MgII-279.6','MgII-279.8')
    new_label=new_label.replace('OII-372.6','OII-372.7')
    new_label=new_label.replace('SII-406.9','SII-407.0')
    new_label=new_label.replace('NII-654.3','NII-654.8')
    new_label=new_label.replace(' ','')
    if lbda == 190.873 and new_label == 'CIII-190.9' :
        new_label = 'CIII-190.8'
    if lbda == 232.54000000000002 and new_label == 'CII-232.5' :
        new_label = 'CII-232.6'
    return new_label



line_labels = Ms[0].emis_labels
line_list = open("line_list_HII_PDR.dat", "rt")



output = open('line_wavelengths_'+ zone +'.dat', "w")  
for line in line_list:
    line_name=line[0:14]
    line_list_name.append(line_name)
    unit=line[13]
    if unit=='A' : 
        wl=float(line[6:13])/1.e1
        #print(wl)
        line_list_wl.append(wl)
        line_name=change_label(line_name,wl)
        output.write(str("%7.3f" %wl)+','+line_name+'\n')
    elif unit=='m' :
        wl=float(line[6:13])*1.e3
        line_list_wl.append(wl)
        line_name=change_label(line_name,wl)
        output.write(str("%6.2f" %wl)+','+line_name+'\n')
    else :
        print('problem in wavelength units') 
    line_list_wl.append(wl)    
output.close()

line_index=[*range(1,len(line_list_name)+1)]

#print(line_list_name)

#=============================================================================
#les raies 
line_list = open('line_wavelengths_'+ zone +'.dat', 'r')
wave_lambda = []
for line in line_list :
    bq = line.strip()
    cq = ''
    i = 0
    while bq[i] != ',' :
        cq += bq[i]
        i+=1
    cq = eval(cq)
    wave_lambda.append(cq)
#=============================================================================


#=============================================================================
#Extinction de la PDR : from CLOUDY radiative transfer
# Function to calculate the power-law with constants a and b
def power_law(x, a, b,c):
    return(a*np.power(x, b)+c)
def power_law_10(x,b,c) :
    return(10*np.power((x/550),b)+c)
def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
def double_gaus(x,a,x0,sigma,b,y0,teta,const) : 
    return(gaussian(x,a,x0,sigma)+gaussian(x,b,y0,teta)+const)

#extinction pour nanometre
def Extinction(wavelength) :
    if wavelength/10 <= 7024.06482691 :
        b = -1.449
        c = -0.188
        ext = power_law_10(wavelength/10,b,c)
    if wavelength/10 > 7024.06482691 and wavelength/10 <= 24350.1940048 : 
        a = 0.499
        x0 = 9787.722
        sigma = 1255.274
        b = 0.268
        y0 = 18424.505
        teta = 7524.082
        const =  -0.044
        ext = double_gaus(wavelength/10,a,x0,sigma,b,y0,teta,const) 
    if wavelength/10 > 24350.1940048 :
        a = 2499817.058
        b =  -1.638
        c =  0.00184
        ext = power_law(wavelength/10, a, b,c)
    return(ext)
#creation des extinction 10**-E pour les 147 raies
f = open('extinction_line' + ".txt" ,  "w")
for j in range(len(wave_lambda)) : 
    f.write(str(np.power(10,-Extinction(wave_lambda[j])))+'\n') 
f.close()
#=============================================================================

#=============================================================================
#Attenuation from Cardelli and al. 1989 : empirical laws 
def Dust_att(wavelength):
   
    x = 1/(wavelength*(1e-4))
    y = x - 1.82
    Rv = 3.1
    Av = 1
    a = 0
    b = 0
    
    #Infrared from 0.909 um to 3.33 um
    if x <= 1.1 :
        a = 0.574*(x**1.61)
        b = -0.527*(x**1.61)
        
    #Optical and Near-infrared from 0.303 um to 0.909 um 
    if x >= 1.1 and x <= 3.3 :
        a = 1 + 0.17699*y - 0.50447*(y**2) - 0.02427*(y**3)+0.72085*(y**4) + 0.01979*(y**5) - 0.77530*(y**6) + 0.32999*(y**7)
        b = 1.41338*y + 2.28305*(y**2) + 1.07233*(y**3) - 5.38434*(y**4) - 0.62251*(y**5) + 5.30260*(y**6) - 2.09002*(y**7)
        
        
    #Ultraviolet and Far-UV from 0.125 um to 0.303 um
    if x >= 3.3 and x <= 8 :
        if x >= 5.9 and x <= 8 :
            Fa = -0.04473*((x-5.9)**2) - 0.009779*((x-5.9)**3)
            Fb = 0.2130*((x-5.9)**2) + 0.1207*((x-5.9)**3)
        if x < 5.9 : 
            Fa = 0
            Fb = 0
        a = 1.752 - 0.316*x-0.104/((x-4.67)**2+ 0.341) + Fa
        b = -3.090 + 1.825*x + 1.206/((x-4.62)**2+0.263) + Fb
        
   
    #Far-UV from 0.1 um to 0.125 um
    if x >= 8 and x <= 10 :
        a = -1.073 - 0.628*(x-8) + 0.137*((x-8)**2) - 0.070*((x-8)**3)
        b =  13.670 + 4.257*(x-8) - 0.420*((x-8)**2) + 0.374*((x-8)**3)
        
    
    return((a + b/Rv)*Av)

  #creation des attenuations 10**-Att pour les 147 raies
g = open('dust_att_line' + ".txt" , "w")
for j in range(len(wave_lambda)) :
    g.write(str(np.power(10,-Dust_att(wave_lambda[j])))+'\n') 
g.close()  
#=============================================================================


#=============================================================================
#Gatt et Ext : attenuation + extinction des raies 
G = open('dust_att_line' + '.txt', 'r')
E = open('extinction_line' + '.txt', 'r')
Gatt = []
Ext = []
for l in G :
    lq = l.strip()
    lq = eval(lq)
    Gatt.append(lq) 
for e in E :
    eq = e.strip()
    eq = eval(eq)
    Ext.append(eq) 
Gatt = np.array(Gatt)
Ext = np.array(Ext)
#=============================================================================


#=============================================================================
# generate on CIGALE lines.dat file per covering factor

covering = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
print(covering, len(covering), 'covering factors')

model_name_out= [M.model_name for M in Ms]
model_name_out_nograin= [M.model_name for M in Ms_nograin]
model_name_out_HII_PDR= [M.model_name for M in Ms_HII_PDR]
print(len(model_name_out)*len(covering), 'models')

t = []

metallicity_save = []
logU_save = []
lognH_save = []
coverage_save = [] 
index_save = []     

i = 1
for fcov in covering :                                 
    for dzetaO in tab_dzetaO : 
        Z = change_metallicity(dzetaO)            
        for logU in tab_logU :
            for dens in tab_density:                   
                metallicity_save.append(Z)
                logU_save.append(logU)
                lognH_save.append(dens)
                coverage_save.append(fcov)
                index_save.append(i)
                i += 1
                t_param_list = Table([index_save, metallicity_save, lognH_save, logU_save, coverage_save], names=('index','Z', 'log_nH', 'log_U', 'f_cov') )
                
#print(t_param_list)
        
t = t_param_list
       
for li in range(len(line_list_name)) : 
    flux_line = []
    for fcov in covering :                       
        for dzetaO in tab_dzetaO : 
            Z = change_metallicity(dzetaO)            
            for logU in tab_logU :
                for dens in tab_density:
                    name_ordered = '{0}{1}'.format(dir_HII, model_name_HII) + "_%.2f" % dzetaO + "_%.1f" % dens + "_%.1f" % logU                                  
                    index = model_name_out.index(name_ordered)                                    
                    I_HII = Ms[index].get_emis_rad(line_labels[li])/ Ms[index].Phi0 * 1.e-7  # flux in W /photon 
                    name_ordered = '{0}{1}'.format(dir_HII_nograin, model_name_HII_nograin) + "_%.2f" % dzetaO + "_%.1f" % dens + "_%.1f" % logU                                  
                    index = model_name_out_nograin.index(name_ordered)                                    
                    I_HII_nograin = Ms_nograin[index].get_emis_rad(line_labels[li])/ Ms_nograin[index].Phi0 * 1.e-7  # flux in W /photon                          
                    name_ordered = '{0}{1}'.format(dir_HII_PDR, model_name_HII_PDR) + "_%.2f" % dzetaO + "_%.1f" % dens + "_%.1f" % logU                                
                    index = model_name_out_HII_PDR.index(name_ordered)                                    
                    I_HII_PDR = Ms_HII_PDR[index].get_emis_rad(line_labels[li])/ Ms_HII_PDR[index].Phi0 * 1.e-7  # flux in W /photon 
                   
                    intensity_NLyc = (1-fcov)*I_HII_nograin*Gatt[li] + fcov*(I_HII_nograin*Ext[li] + (I_HII_PDR-I_HII))
                            
                    if intensity_NLyc < 1e-30 :
                       intensity_NLyc = 0.0                    
                                        
                    flux_line.append(intensity_NLyc)  
   # print(flux_line)
    t_line = Table()
    t_line[line_list_name[li]] = flux_line 
    #print(t_line)

    t = hstack([t , t_line])
    
#print(hstack([t_param_list, flux_line]))
#print(t_line)    
#t = hstack([t_param_list, t_line('H  1  1215.67A')])
            



#t = Table([line_save, flux_save, metallicity_save, lognH_save, logU_save, coverage_save], names=('line', 'flux', 'Z', 'log_nH', 'log_U', 'f_cov') )

print(t)

t.write('/Users/serenac/Desktop/research/PRIMA/cloudy_prima/lines_PDR_models_full.fits', format='fits', overwrite=True)


