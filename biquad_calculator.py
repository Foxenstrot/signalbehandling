
# This program will calculate and present Nyquist biquad-filters for use in Audacity v. 3.6.4
# No guarantee it will work for past and/or future versions of Audacity
# Author: Mikael Foxell
# 2024-09-22


import numpy as np

sample_rate = 48000
starting_tone = 0
no_of_harmonics = 8
a_coeff_mult = 0.99
freq = 230
fs_div2 = sample_rate/2 

# sample_rate: sample_rate of the signal
# tone: tone to start the filter at, 0 is the fundamental tone
# fundamental_tone: frequency in Hz
# no_of_harmonics: how many tones to calculate -1
# a_coeff_mult: how much to dampen

def calc_coeff_audacity_manual(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult_list):
    while True:
            # Restructured to avoid out of bounds
            # If at the last tone, add *track* for correct format
            if tone == no_of_harmonics:
                harmonic = fundamental_tone*(tone+1)
                angle_of_freq = (harmonic/fs_div2) * 180
                rad_of_freq = angle_of_freq * np.pi/180
                real = np.cos(rad_of_freq)
                imag = np.sin(rad_of_freq)      
                b_coeff = [real+(imag*1j), real-(imag*1j)]
                a_coeff = [(real*a_coeff_mult_list[tone])+(imag*1j), 
                           (real*a_coeff_mult_list[tone])-(imag*1j)]
                
                a_coeff = np.poly(a_coeff)
                b_coeff = np.poly(b_coeff)
                tone +=1
                print(f' (biquad-m ', end='')

                calc_coeff_audacity_manual(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult_list)           
                print(f'*track* {b_coeff[0]} {b_coeff[1]} {b_coeff[2]} 1 {a_coeff[1]} {a_coeff[2]})',end='')

            elif tone <= no_of_harmonics:
                harmonic = fundamental_tone*(tone+1)
                angle_of_freq = (harmonic/fs_div2) * 180
                rad_of_freq = angle_of_freq * np.pi/180
                real = np.cos(rad_of_freq)
                imag = np.sin(rad_of_freq)      
                b_coeff = [real+(imag*1j), real-(imag*1j)]
                a_coeff = [(real*a_coeff_mult_list[int(tone)])+(imag*1j), 
                           (real*a_coeff_mult_list[tone])-(imag*1j)]
                
                a_coeff = np.poly(a_coeff)
                b_coeff = np.poly(b_coeff)
                tone += 1
                print(f' (biquad-m', end='')
                
                calc_coeff_audacity_manual(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult_list)
                print(f' {b_coeff[0]} {b_coeff[1]} {b_coeff[2]} 1 {a_coeff[1]} {a_coeff[2]})', end='')
                
            return


def calc_coeff_audacity(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult): 
    while True:
        harmonic = fundamental_tone*(tone+1)
        angle_of_freq = (harmonic/fs_div2) * 180
        rad_of_freq = angle_of_freq * np.pi/180
        real = np.cos(rad_of_freq)
        imag = np.sin(rad_of_freq)      
        b_coeff = [real+(imag*1j), real-(imag*1j)]
        a_coeff = [(real*a_coeff_mult)+(imag*1j), 
                   (real*a_coeff_mult)-(imag*1j)]
        a_coeff = np.poly(a_coeff)
        b_coeff = np.poly(b_coeff)
        
        if tone == no_of_harmonics:
            tone +=1
            print(f' (biquad-m ', end='')
            calc_coeff_audacity(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult)           
            print(f'*track* {b_coeff[0]} {b_coeff[1]} {b_coeff[2]} 1 {a_coeff[1]} {a_coeff[2]})',end='')
        elif tone <= no_of_harmonics:

            tone += 1
            print(f' (biquad-m', end='')
            
            calc_coeff_audacity(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult)
            print(f' {b_coeff[0]} {b_coeff[1]} {b_coeff[2]} 1 {a_coeff[1]} {a_coeff[2]})', end='')
            
        return
        
def calc_coeff(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult): 
    while True:
        harmonic = fundamental_tone*(tone+1)
        angle_of_freq = (harmonic/fs_div2) * 180
        rad_of_freq = angle_of_freq * np.pi/180
        real = np.cos(rad_of_freq)
        imag = np.sin(rad_of_freq)      
        b_coeff = [real+(imag*1j), real-(imag*1j)]
        a_coeff = [(real*a_coeff_mult)+(imag*1j), (real*a_coeff_mult)-(imag*1j)]
        a_coeff = np.poly(a_coeff)
        b_coeff = np.poly(b_coeff)
        tone += 1
             
        if tone <= no_of_harmonics+1:
            
            calc_coeff(sample_rate, tone, fundamental_tone, no_of_harmonics, a_coeff_mult)
            print(f'Frequency: {freq*tone} | A_Mult: {a_coeff_mult} | N = {tone-1} | \nb0= {b_coeff[0]} | b1= {b_coeff[1]} | b2= {b_coeff[2]} | a0= 1 | a1= {a_coeff[1]} | a2= {a_coeff[2]})')
      
        return
        


# Main:
sample_rate = input("Enter Sample rate: ")
freq = int(input("Enter frequency: "))
no_of_harmonics = int(input("Enter number of harmonics: "))
a_coeff_mult_choice = input("Same A-Coefficient multiplier for all harmonics? (Y/N): ")
if a_coeff_mult_choice.lower() == "n" or a_coeff_mult_choice.lower() == "no":
    a_coeff_mult_list = []
    for i in range(no_of_harmonics+1):
        print(f'Enter A-coefficient for frequency {freq*(i+1)} Hz: ')
        a_coeff_mult_list.append(float(input("")))
else:
    a_coeff_mult = float(input("Enter A-coefficient: "))

audacity = input("Formatted for Audacity? (Y/N)")
if audacity.lower() == "y" or audacity.lower == "yes":
    print(f'')
    print(f'')
    print(f'')
    if a_coeff_mult_choice.lower() == "n" or a_coeff_mult_choice.lower() == "no":
        calc_coeff_audacity_manual(sample_rate, starting_tone, freq, no_of_harmonics, a_coeff_mult_list) 
    else:
        calc_coeff_audacity(sample_rate, starting_tone, freq, no_of_harmonics, a_coeff_mult)
    print(f'\n')
else:
    print(f'')
    print(f'')
    calc_coeff(sample_rate, starting_tone, freq, no_of_harmonics, a_coeff_mult) 
    print(f'\n')   