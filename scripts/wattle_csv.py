#!/usr/bin/env python3
# python ./scripts/21_wattle_cs.py
#
#
# chris.browne@anu.edu.au - all care and no responsibility :)
# ===========================================================

'''creates a file ready to upload to Wattle'''

import os
from os import path
import csv
import pandas as pd
import yaml
import hashlib
from shutil import copyfile
import config as c
import functions as f


def wattle_csv():
    cfg = f.load_config()

    # print message to console - complete!
    f.pnt_notice(c.msg['console_start'], os.path.basename(__file__))

    # organising the files for uploading to wattle
    # print message to console
    f.pnt_info(c.msg["console_wattle"])

    # get the list of students
    f.load_tsv('students')
    f.load_tsv('marks')

    if cfg['feedback_type']['tmc']:
        for i, row in c.df['students'].iterrows():
            user = row['user']
            group = row['group']
            # secret = hashlib.sha1(row['user'].encode('utf-8')).hexdigest()
            # secret_file = user + "-" + secret + ".pdf"
            this_file = user + ".pdf"

            # cp pdf to secret here
            file_from = c.d['pdf'] + group + "_tmc_anon.pdf"
            file_to = c.d['upload'] + this_file

            if path.exists(file_from):
                copyfile(file_from, file_to)
                comment = "<a href=\"" + cfg['assignment'][
                    'feedback_url'] + "/" + user + ".pdf\">PDF Feedback</a>"
            else:
                comment = "No Team Member Contribution received from the team"

            # update the df
            c.df['students'].at[i, 'secret'] = comment
        wattle_out = c.df['students'][['user','group','firstname','lastname','secret']]

    # decide whether to use the list_team or list_name field
    elif not cfg['feedback_type']['group']:
        # print message to console - creating secrets
        f.pnt_info(c.msg['console_secrets'])

        # loop through each row and create a secret for each student
        for i, row in c.df['marks'].iterrows():
            user = row['user']
            # secret = hashlib.sha1(row['user'].encode('utf-8')).hexdigest()
            secret =""
            this_file = user + ".pdf"
            comment = "<a href=\"" + cfg['assignment'][
                'feedback_url'] + "/" + user + ".pdf\">PDF Feedback</a>"

            # update the df
            c.df['marks'].at[i, 'secret'] = comment


            # cp pdf to secret here
            file_from = c.d['pdf'] + user + ".pdf"
            file_to = c.d['upload'] + this_file

            copyfile(file_from, file_to)
        marks_out = c.df['marks'][['user', 'grade_final', 'secret']]
        wattle_out = marks_out.merge(c.df['students'], on='user', how='left')[['user', 'grade_final', 'secret']]

    else: # use the list_team
        # loop through each row and create a secret for each student
        for i, row in c.df['marks'].iterrows():
            group = row['list_team']
            if 'suggested_indicator' in c.df['marks']:
                comment = "Team Progress Indicator: " + row['suggested_indicator'] + "<br /><a href=\"" + cfg['assignment']['feedback_url'] + "/" + group + ".pdf\">PDF Feedback for " + group + "</a>"
            else:
                comment = "<a href=\"" + cfg['assignment']['feedback_url'] + "/" + group + ".pdf\">PDF Feedback for " + group + "</a>"

            c.df['marks'].at[i, 'secret'] = comment

            # cp pdf to secret here
            file_from = c.d['pdf'] + group + ".pdf"
            file_to = c.d['upload'] + group + ".pdf"
            copyfile(file_from, file_to)

        marks_out = c.df['marks'][['list_team', 'grade_final', 'secret']]
        print(marks_out)
        wattle_out = marks_out.merge(c.df['students'], left_on='list_team', right_on='group', how='left')[
            ['user', 'grade_final', 'secret', 'group']]
        print(wattle_out)

    f.pnt_info(c.msg['console_upload'])
    wattle_out.to_csv(c.f['wattle'], index=False)
    f.pnt_notice(c.msg['console_complete'], os.path.basename(__file__))
