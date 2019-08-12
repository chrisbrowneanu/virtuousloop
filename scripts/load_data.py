#!/usr/bin/env python3
# python ./scripts/11_load_data.py
#
#
# chris.browne@anu.edu.au - all care and no responsibility :)
# ===========================================================

'''runs checks'''

import os
import glob
from pathlib import Path
import config as c
import functions as f
import codecs

def load_data():

    # check that config exists
    cfg=f.config_exists()

    # print message to console - starting!
    f.pnt_notice(c.msg['console_start'],os.path.basename(__file__))

    # load directories
    f.make_directories(c.d)

    # print message to console
    f.pnt_info(c.msg["console_loading"])

    # load in all csvs in the files dir
    glob.glob('./files/*.csv')
    for files in glob.glob('./files/*.csv'):
        this_csv=Path(files).stem
        f.load_csv(this_csv)
        if this_csv == 'students':
            # rename fields
            f.rename_header(this_csv, 'user id', 'user')
            f.rename_header(this_csv, 'first_name', 'first')
            f.rename_header(this_csv, 'surname', 'last')
            f.check_duplicates(this_csv, 'user')
        elif this_csv == 'marks':
            # rename fields
            f.rename_header(this_csv, 'username', 'marker_id')
            f.rename_header(this_csv, 'user', 'marker_name')
            # split the user - name column in c.df[this_csv]
            c.df[this_csv][['user','name']] = c.df[this_csv]['list_name'].str.split('\s+-\s+', expand=True)
            f.check_duplicates(this_csv, 'user')
        elif this_csv == 'fields':
            # lower fields to match marks.csv lower
            f.col_to_lower(this_csv, 'field')
        elif this_csv == 'crit_levels':
            # rename fields
            f.rename_header(this_csv, 'level', 'index')
        elif this_csv == 'data_tmc':
            # rename fields
            f.rename_header(this_csv, 'teamdropdown', 'list_team')

        #print(c.df[this_csv])
        c.df[this_csv].to_csv(c.t[this_csv], sep='\t', encoding='utf-8', index=False)


    if cfg['feedback_type']['json'] == 'true':
        #f.json_list(c.t['students'])
        f.load_tsv('students')
        # get a list of teams
        teams=c.df['students'].groupby(['group']).count().reset_index()
        # need member_count to set the right number of fields
        member_count=teams['user'].max()

        # create a list of teams to iterate through
        team_list=[]
        for i, row in teams.iterrows():
            this_team = row['group']
            team_list.append(this_team)

        # add a column with user - first last
        for i, row in c.df['students'].iterrows():
            list_name=row['user'] + " - " + row['first'] + " " + row['last']
            c.df['students'].at[i,'list_name'] = list_name
        
        # open up a file to print to
        with open(c.f['json'], 'w') as out:
            for team in team_list:
                # get just the members of the team
                this_team_df=f.filter_row('students', 'group', team)
                print("\'" + team + "\': ", file=out, end = '')
                this_team_list=[''] * member_count
                j=0
                for i, row in this_team_df.iterrows():
                    this_team_list[j]=row['list_name']
                    j=j+1
                print(str(this_team_list) + ",", file=out)
        
        # remove the final comma
        with open(c.f['json'], 'rb+') as out:
            out.seek(-2, os.SEEK_END)
            out.truncate()


    # print message to console - complete!
    f.pnt_notice(c.msg['console_complete'],os.path.basename(__file__))