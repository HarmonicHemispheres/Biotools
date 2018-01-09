#!/usr/bin/env python3

#################################################

### Protein Comparison via site by site analysis
#
#
### EXAMPLE
# ARGS ::  0              1
# COMM ::  ./prot_comp.py path_to_control.file
#
#
### NOTES
#
# - groups file line format = "species name, (group # 1 or 2)"
# - alignment files should contain the species name in [] on the desc line 
#
#################################################

import os
import sys
import json
import sqlite3


#### Globals ####
exp_title = ""
gr1 = ""
gr2 = ""
grps = {}
aligns = ""
control = {}
out_db = ""

def main():
    global aligns
    global control
    

    # =======================================
    # first read user input from command line
    #
    if (len(sys.argv) != 2):
        exit("ERROR: invalid number of arguments")

    _control = os.path.abspath(sys.argv[1])

    # =======================================
    # parse control file for global variables
    #
    parse_control(_control)

    # =======================================
    # verifiy the output database file exists
    # if it does not, sqlite will create it.
    # ALSO add new table to db for experiment
    #
    global out_db
    conn = sqlite3.connect(out_db)
    c = conn.cursor()
    table_name = control["project"]["experiment title"]
    try:
        c.execute("create table {} ('{}', {}, {}, {}, {}, {}, {})".format(table_name, \
            "Protein_id", \
            "Percent_Sim", \
            "Alignment_Len", \
            "Total_Hits", \
            "Num_Spe", \
            "Num_1", \
            "Num_2" ))
    except:
        # table already exists
        pass

    conn.commit()
    conn.close()
    

    # =======================================
    # check all input files for alignment
    #
    #try:
    if (os.path.isdir(aligns) is True):
        

        for file in os.listdir(aligns):
            if ".fasta" in file:
                print("MESSAGE: starting {}".format(file))
                align = prepare(fl=aligns + "/" + file)

                if align != -1:
                    
                    res = compare(align)
                    if res is False:
                        pass
                    else:
                        res = stats(res, align, file)
                        insert_to_db(db=out_db, res_dict=res, tb=table_name)
                    

    elif (os.path.isfile(aligns) is True):
        align = prepare(aligns)
        res = compare(align)
        if align != -1:
            
            res = stats(res, align, os.path.basename(aligns) )
            insert_to_db(db=out_db, res_dict=res, tb=table_name)
            
    else:
        print("MESSAGE: aligns is not a file or dir")


    #except:
    #    exit("ERROR: prot_comp encountered a problem")

    


def parse_control(fl):
    global exp_title
    global gr1
    global gr2
    global grps
    global aligns
    global control
    global out_db

    # ===========================
    # load control file into dict
    # removes comment lines before parsing
    with open(fl, "r") as f:
        rd = ""
        for i in list(f.readlines()):
            if "//" not in i: 
                rd += i.replace("\n", "")
        control = json.loads(rd)
        


    exp_title = control["project"]["experiment title"]
    gr1 = control["project"]["group 1 title"]
    gr2 = control["project"]["group 2 title"]
    aligns = control["project"]["alignment/s path"]
    out_db = control["project"]["output db path"]

    # ===========================
    # convert groups file to dict
    #
    with open(control["project"]["groups path"], "r") as sp_file:
        sp_file_rd = sp_file.read().splitlines()
        for i in sp_file_rd:
            line = i.split(",")
            grps[line[0]] = line[1].strip(" ")

def prepare(fl):
    """ setup alignment in dict structure for speed """
    global grps

    with open(fl, "r") as alignment:
        out_list = []
        prot_id = ""
        prot_rd = alignment.read().split(">")[1:]
        
        if len(prot_rd) < 2:
            print("ERROR: file has 1 sequence, not aligned properly!")
            return -1

        for prot_i in prot_rd:    
            if len(prot_i) > 10:
                
                prot_id = prot_i.splitlines()[0].split("[")[-1].split("]")[0]
                prot_seq = ""
                
                gr = ""
                for k,v in grps.items():
                    if k in prot_id:
                        gr = v
                        break
                for i in prot_i.splitlines()[1:]:
                    prot_seq += i

                # index 0 = id line
                # index 1 = sequence
                # index 2 = group number
                out_list.append( (prot_id, prot_seq, gr) )

        return out_list
        

def compare(prot_list):
    """ performs site by site comparison defining hits based on 
    control file specifications """
    global control

    # get list of AA's at "site" for each group
    g1 = []
    g2 = []
    for spe in prot_list:

        if (spe[2] == "1"):
            g1.append(spe[1][0])
        elif (spe[2] == "2"):
            g2.append(spe[1][0])
        
    if control["analysis"]["both_groups"] is True:
        if len(g1) == 0 or len(g2) == 0:
            return False

    alns = {}
    hit_sites = []

    for site in range(len(prot_list[0][1])):
        g1 = []
        g2 = []
        hit = False

        # get list of AA's at "site" for each group
        for spe in prot_list:

            if (spe[2] == "1"):
                g1.append(spe[1][site])
            elif (spe[2] == "2"):
                g2.append(spe[1][site])

        # record all hit sites in list
        if (is_hit(g1, g2) is True):
            hit_sites.append(site)
            hit = True

        # perform comparisons
        if (control["output"]["show sites"] == True):
            if (hit):
                print("{}  : HIT\ng1={}\ng2={}".format(site,g1,g2))
            
            elif (control["output"]["show all"] == True):
                print("{}  : NOT HIT\ng1={}\ng2={}".format(site,g1,g2))

    return hit_sites


def is_hit(l1, l2):
    """ decides whether the site is a hit """
    global control


    # checks if enough AA's are different between each group
    hit_thr = float(control["analysis"]["hit_thr"])

    # make sure all l1 are conserved by a percentage
    
    l1_counter = list(filter(("-").__ne__, l1))
    l2_counter = list(filter(("-").__ne__, l2))
    l1cp = l1_counter
    l2cp = l2_counter

    # build crossover list which will be used to subtract from original
    # lists and generate unique lists
    i = 0
    crossL = []
    while i < len(l1cp) and len(l1cp) > 1:
        if l1cp[i] in l2cp:
            val = str(l1cp[i])
            crossL.append(val)
            l1cp.remove(val)
            l2cp.remove(val)
            i -= 1
        
        i += 1
    

    ### Perform Checks as stated in the control analysis section ###
    if control["analysis"]["nocross"] == True:
        for i in crossL:
            if i != "-":
                ishit = 0
                return False

    if len(l1cp) < hit_thr * len(l1):
        return False

    
    return True
    


def stats(l, org, title):
    """ takes list of hits displays stats for alignment """

    global control


    res_record = {}
    res_record["Protein_id"] = title.split(".")[0]
    res_record["Percent_sim"] = len(l) / len(org[0][1])
    res_record["Alignment_len"] = len(org[0][1])
    res_record["Total_hits"] = len(l)
    res_record["Num_spe"] = len(org)
    res_record["Num_1"] = ""
    res_record["Num_2"] = ""


    print("---- Results for {} ----".format(title))

    if (control["analysis"]["perc_sim"] == True):    
        print("{:>20}: {:<12}".format("% similarity", len(l) / len(org[0][1]) ) )
        print("{:>20}: {:<12}".format("threshold", control["analysis"]["hit_thr"] ) )

    if (control["analysis"]["total_len"] == True):    
        print("{:>20}: {:<12}".format("alignment length", len(org[0][1]) ) )

    if (control["analysis"]["hit_count"] == True):    
        print("{:>20}: {:<12}".format("total hits", len(l) ) )

    if (control["analysis"]["sp_count"] == True):    
        print("{:>20}: {:<12}".format("total species count", len(org) ) )

    if (control["analysis"]["gr_count"] == True):    
        gr1 = control["project"]["group 1 title"]
        gr1c = 0
        gr2 = control["project"]["group 2 title"]
        gr2c = 0

        # Count species for each group
        error_list = []

        for i in org:
            if i[2] == "1":
                gr1c += 1
            elif i[2] == "2":
                gr2c += 1
            else:
                error_list.append(i[0])

        print("{:>20}: {:<12}".format("{} species count".format(gr1), gr1c ) )
        print("{:>20}: {:<12}".format("{} species count".format(gr2), gr2c ) )
        print("\n")

        res_record["Num_1"] = gr1c
        res_record["Num_2"] = gr2c

        if len(error_list) > 0:
            print("Species Not In Groups List\n--------------------------")
            for i in error_list:
                print(i)

        print("----------------------------------------------------\n\n")

        return res_record
            

def insert_to_db(db, res_dict, tb):
    """ inserts a entry of results into the output database """

    global control
    global out_db
    conn = sqlite3.connect(out_db)
    c = conn.cursor()

    command_str = "INSERT INTO {} ('{}', {}, {}, {}, {}, {}, {})".format(tb, \
        "Protein_id", \
        "Percent_Sim", \
        "Alignment_Len", \
        "Total_Hits", \
        "Num_Spe", \
        "Num_1", \
        "Num_2" )

    
    values_str = "VALUES ('{}', {}, {}, {}, {}, {}, {})".format(res_dict["Protein_id"], \
        res_dict["Percent_sim"], \
        res_dict["Alignment_len"], \
        res_dict["Total_hits"], \
        res_dict["Num_spe"], \
        res_dict["Num_1"], \
        res_dict["Num_2"])

    try:
        c.execute(command_str + " " + values_str)

    except:
        print("ERROR: bad insertion for {}".format(res_dict["protein id"]))

    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()



