#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 18:40:47 2018

@author: mariachowdhury
"""
import sys

"""records include cmte"""
def getCmte(plc,plc_cmte):
    cmte_new=plc_cmte.split("|")
    plc_new=plc.split("|")
    name_postal_code=plc_new[0]+"|"+plc_new[1]
    cmte_name_postal_code=cmte_new[1]+"|"+cmte_new[2]
    if cmte_name_postal_code==name_postal_code:
        out=plc_cmte+"|"+plc_new[2]
        return out


"""collecting repeat donors' latest donations"""
def getMaxYear(person_list):
    max=-1
    out_rec=""
    for person in person_list:
        rec=person.split("|")
        if int(rec[3])>max:
            max=int(rec[3])
            out_rec=rec[0]+'|'+rec[2]+'|'+rec[3]+'|'+rec[4]
    return out_rec

def getPersonList(person, person_list_year):
    out=[]
    for ply in person_list_year:
        ply_rec=ply.split("|")
        person_name=ply_rec[1]+"|"+ply_rec[2]
        if person==person_name:
            out.append(ply)
    return getMaxYear(out)


"""counting the number of occurences"""
def getPersonOccurence(person,person_list):
    occurence=0
    for p in person_list:
        if p==person:
            occurence=occurence+1
    person_occurence=person+"|"+str(occurence)
    return person_occurence


"""Associating percentile"""
def getPercentile(out_rec,percentiles_item):
    out_rec_values=out_rec.split("|")
    out_rec_values[3]=percentiles_item
    out_rec_val= ('|'.join(out_rec_values))
    return out_rec_val


"""collecting repeat donors,calculating percentile record and writing to output file""" 
def collectingRepeatDonors(output_file,percentile_given,person_set,person_list_year): 
    out_list=[]
    for person in person_set:
        out_rec_person=getPersonList(person,person_list_year)
        out_list.append(out_rec_person)
        out_list.sort()    
        i=1
        amount=0  
        out=[]         
    for out_rec in out_list:
        if out_rec:
            out_rec_items=out_rec.split('|')
            amount=amount+int(out_rec_items[3])
            out_rec=out_rec+"|"+str(amount)+"|"+str(i)
            i=i+1
            out.append(out_rec)
        
    import math
    import os
    if os.path.exists(output_file):
        os.remove(output_file)
    output_write=open(output_file,'w')
    x=1
    if len(out)>0:
        x=len(out)
    percentile_ith=percentile_given*.01/x 
    percentile=(math.ceil(percentile_ith))
    percentile_rec=(out[percentile-1])
    percentiles_items=percentile_rec.split('|')
    percentiles_item=percentiles_items[3]
    for out_rec in out:
        out_rec_val=getPercentile(out_rec,percentiles_item)
        output_write.write(out_rec_val+"\n")        
    output_write.close()
    

def main(argv):
    input_file=argv[1]
    percentile_file=argv[2]
    output_file=argv[3]
    
    #import os
    #print("Current dir" + os.getcwd())
    
    #input_file=os.getcwd()+"/input/itcont.txt"
    #percentile_file=os.getcwd()+"/input/percentile.txt"
    #output_file=os.getcwd()+"/output/repeat_donors.txt"

    """reading percentile value"""
    percentile_given=0
    with open(percentile_file, mode="r",encoding="utf-8") as my_percentile_file:
        for line in my_percentile_file:
            percentile_given=int(line)
    
    """collecting all the records in a list from the input file"""
    input_records=[]
    with open(input_file, mode="r",encoding="utf-8") as my_file:
        for line in my_file:
            lines=line.split('|')
            if(len(lines)>1):
                input_records.append(lines)

   

    """collecting all the unique donors in a set"""
    person_list=[]
    person_list_cmte=[]
    for r in input_records:
        CMTE_ID=r[0]
        date=r[13]
        amount=r[14]
        name=r[7]
        postal_code=r[10]
        person=name+'|'+postal_code[:5]
        cmte=CMTE_ID+'|'+person+"|"+date[-4:]+"|"+amount
        person_list.append(person)
        person_list_cmte.append(cmte)
                   
    person_set=set()
    for p in person_list:
        person_set.add(p)
    


    """collecting person list with the number of occurences and years"""
    person_list_occurence=[]
    for person in person_set:
        person_occurence=getPersonOccurence(person,person_list)
        items=person_occurence.split("|")
        occurence=items[2]
        if occurence!="1":
            person_list_occurence.append(person_occurence)
    person_list_year=[]
    for plc in person_list_occurence:
        for plc_cmte in person_list_cmte:
         cmte_plc_date=getCmte(plc,plc_cmte)
         if cmte_plc_date:
             person_list_year.append(cmte_plc_date)



    
    collectingRepeatDonors(output_file,percentile_given,person_set,person_list_year)
if __name__ == '__main__':
	main(sys.argv[0:])
import os
input_file=os.getcwd()+"/itcont.txt"
percentile_file=os.getcwd()+"/percentile.txt"
output_file=os.getcwd()+"/repeat_donors.txt"
#getRepeatDonors(input_file,percentile_file,output_file)
