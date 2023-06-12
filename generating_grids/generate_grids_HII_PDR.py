import os
home_dir = os.environ['HOME'] + '/'
import pyCloudy as pc


# We define a function that will manage the input files of Cloudy. 
# This allow to easily change some parameters, very usefull to do a grid.
def make_model(dir_, model_name, dzetaO, dens, logU):
  #  full_model_name = '{0}_{1:.1f}_{1:.1f}_{1:.0f}_{2:.2f}'.format(model_name, delta, dzeta_O, dens, logU)
    full_model_name = model_name +"_%.2f" % dzetaO + "_%.1f" % dens + "_%.1f" % logU

   # Defining the object that will manage the input file for Cloudy
    c_input = pc.CloudyInput(full_model_name)  
    # Filling the object with the parameters
    if dzetaO in [-3.0] : 
        Z = 1e-5
    elif dzetaO in [-2.0] : 
        Z = 0.0001
    elif dzetaO in [-1.5, -1.0] :
        Z = 0.001
    elif dzetaO in [-0.8,-0.7] :
        Z = 0.002  
    elif dzetaO in [-0.6] :
        Z = 0.003  
    elif dzetaO in [-0.5, -0.4] :
        Z = 0.004 
    elif dzetaO in [-0.3] :
        Z = 0.006
    elif dzetaO in [-0.25, -0.2] :
        Z = 0.008
    elif dzetaO in [-0.15, -0.1, -0.05] :
        Z = 0.01
    elif dzetaO in [0.0] :
        Z = 0.014
    elif dzetaO in [0.05, 0.1, 0.12, 0.15] :
        Z = 0.02
    elif dzetaO in [0.2, 0.25, 0.3] :
        Z = 0.03
    elif dzetaO in [0.35, 0.4, 0.45, 0.5 ] :
        Z = 0.04
    else :
        print('problem with metallicity')
    #c_input.set_abund(predef= '"dzetaO'+ "_%.2f" % dzetaO +'_depletion.abn"' , nograins = True) # grain depletion is accounted for in the .abn file. 
    c_input.set_abund(predef= '"dzetaO'+ "_%.2f" % dzetaO +'.abn"' , nograins = True) # grain depletion is not accounted for in the .abn file. 
    c_input.set_star(SED= 'table star "BC03_chab.mod"',SED_params = (Z,10), lumi_unit = 'ionization parameter', lumi_value = logU) 
    c_input.set_cste_density(dens)    
    c_input.set_iterate(to_convergence = True) # (0) for no iteration, () for one iteration, (N) for N iterations.
    c_input.set_sphere(True) # () or (True) : sphere closed geometry, or (False): open geometry.
    

    options = ('element limit off -8',        
               'grains ism' ,    
               'grains PAH' ,# PAH do not scale with metallicity
               'set temperature convergence -2.3', #'-2.7', default = 0.005 = log(-2.3)
               'cosmic rays background, '#' linear 0.1266 in pdr_leiden.ini (meeting Leiden)
               'set csupra -16.64', # add cosmic rays, which are important at depth + 
               #'set H2 Jura ELRD', #use the H2 formation rate on grains, set H2 Jura SN99 in leiden.in but ELRD by default
               'database H2',
               'database H2 chemistry full',
               'set nchrg 2', # default = 2
               'set nend 2000', #'stop zone 400',#   default=1400  
              )
    c_input.set_other(options)
    
    # stop criteria
    #c_input.set_stop(stop_criter=('efrac -3.0','temperature 2')) # stop criterion for HII regions
    c_input.set_stop(stop_criter=('temperature 3 linear', 'AV point 10 linear')) # stop criterion for PDR 
   ##
    c_input.read_emis_file('LineList_HII_PDR.dat', emergent = True)
    c_input.set_line_file('LineList_HII_PDR.dat', absolute = True, emergent = True) 
 #   c_input.set_other('save h2 lines "_H2.lin" last electronic all')
    c_input.print_input(to_file = True, verbose = False)
    

# The directory in which we will have the models
dir_ = '/home/ptheule/simulations_CLOUDY/PDR/nebular_HII_PDR/'  
#writing the makefile in the directory dir_
pc.print_make_file(dir_ = dir_)
# setting verbosity to medium level, change to 3 for high verbosity
pc.log_.level = 3

# Generic name of the models
model_name = 'model_HII_PDR_test' 


# tables for the values of the SKIRTOR radiation field shape delta parameter,dzetaO metallicity, nH density and the logU radiation intensiy
#tab_dzetaO = [0.50, 0.15, -0.20, -0.50, -1.5, -2.0] #  the star metallicity is changed automatically (Z_gas = 0.0001, 0.004, 0.022)
tab_dzetaO = [0.0]#[-3.0, -2.0,-1.5,-1.0,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05, 0.0, 0.05, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5] #[-2.0,-1.0,-0.5, 0.0, 0.25, 0.5]#
# metallicity BC03 Z=[0.051, 0.022, 0.008, 0.004, 0.0004, 0.0001] <-> [0.50, 0.15, -0.20, -0.50, -1.5, -2.0]
# metallicity BPASS Z= [1e-05, 0.0001, 0.001, 0.002, 0.003, 0.004, 0.006, 0.008, 0.01, 0.014, 0.02, 0.03, 0.04 ] 
tab_dens =  [2.0]#[1.0, 2.0, 3.0] #  
tab_logU =  [-1.0] #[-1.0,-1.1,-1.2,-1.3,-1.4,-1.5,-1.6,-1.7,-1.8,-1.9,-2.0,-2.1,-2.2,-2.3,-2.4,-2.5,-2.6,-2.7,-2.8,-2.9,-3.0,-3.1,-3.2,-3.3,-3.4,-3.5,-3.6,-3.7,-3.8,-3.9,-4.0] #[-1.0,-2.0,-3.0,-4.0]


# write radiation, metallicity files, density and logU files 

output = open("dzetaO.dat", "w")
for dzetaO in tab_dzetaO :
    output.write("%.2f" % dzetaO + '\n')
output.close()

output = open("density.dat", "w")
for dens in tab_dens :
    output.write("%.1f" % dens + '\n')
output.close()

output = open("logU.dat", "w")
for logU in tab_logU :
    output.write("%.1f" %logU + '\n')
output.close()

### SAVE ###

# # Save list
save_list = [ ['continuum','.cont'], ['physical conditions','.phy'],  ['radius','.rad'] ]#,  ['emissivity','.emis'] ]#, ['output','.out'] automatic
pc.config.SAVE_LIST = save_list

# Save element
save_element = ''  #[['iron','.ele_Fe'],['Helium','.ele_He']]
pc.config.SAVE_LIST_ELEMS = save_element


# defining the models and writing the input files
for dzetaO in tab_dzetaO:
    for dens in tab_dens:
        for logU in tab_logU:
            make_model(dir_, model_name, dzetaO, dens, logU)
        
# Running the models on Cloudy using the makefile 
n_proc = 20 # n_proc processors # n'a pas l'air de marcher sur le portable, mais marche sur l'ordinateur de bureau
pc.log_.message('Running {0}'.format(model_name), calling = 'test1')
pc.config.cloudy_exe = '/home/ptheule/Programs/CLOUDY/c22.01/source/cloudy.exe'# sur l'ordinateur de bureau home_dir + 'bin/cloudy.exe'
#pc.config.cloudy_exe = '/home/ptheule/Cloudy/source/cloudy.exe'# sur le portable home_dir + 'bin/cloudy.exe'
pc.log_.timer('Starting Cloudy', quiet = True, calling = 'test1')
pc.run_cloudy(dir_ = dir_, n_proc = n_proc, model_name = model_name, use_make = True) #activate/deativate to run Cloudy        
pc.log_.timer('Cloudy ended after seconds:', calling = 'test1')        
