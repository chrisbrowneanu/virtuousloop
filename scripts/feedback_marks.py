#!/usr/bin/env python3
# python ./scripts/feedback_marks.py
#
#
# chris.browne@anu.edu.au - all care and no responsibility :)
# ===========================================================

'''turns the marks spreadsheet into pdf feedback'''
'''expects one submission per row'''

import os
import config as c
import functions as f
from jinja2 import Template, Environment, FileSystemLoader

template_dir = c.d['jinja']
env = Environment(loader=FileSystemLoader(template_dir))

def feedback_marks():

    cfg = f.load_config()
    f.pnt_notice(c.msg['console_start'], os.path.basename(__file__))
    f.pnt_info(c.msg["console_loading"])
    
    # load in tsvs of needed fields
    marks_df = f.load_tsv('marks')
    marks_dict = marks_df.to_dict(orient='index')

    # create a df of just the crit for manipulation
    crit_df = f.filter_row('fields', 'field', 'crit_')
    crit_dict = crit_df.set_index["field"].to_dict("index")

    levels_df = f.load_tsv('crit_levels')
    print(levels_df)
    levels_dict = levels_df.set_index("index").to_dict("index")

    field_df = f.delete_duplicates('fields', crit_df)
    field_dict = field_df.to_dict(orient='index')

    f.pnt_info(c.msg["console_creating_feedback_files"])
    
    # create distribution charts for later
    if cfg['crit_display']['graph']:
        stats = f.make_crit_list(crit_df, marks_df)
        f.make_crit_chart(crit_df, stats, "na")

    ## need to figure out display of the rubric if applicable - probably html->pdf here

    print(cfg)
    print(crit_dict)
    print(levels_dict)

    ## iterate through the marks file
    for record in marks_dict.values():
        # evaluate whether to use the list_team or list_name field
        if cfg['feedback_type']['group']:
            this_record = record['list_team']
            this_record_name = record['list_team']
        else:
            this_record = record['user']
            this_record_name = record['list_name']

        print(this_record)
            
        template = env.get_template("feedback_marks.html")
        with open(c.d['html'] + this_record + '.html', 'w') as out:
            out.write(template.render(
                record=record,
                record_name=this_record_name,
                options_dict=cfg,
                field_dict=field_dict,
                crit_dict=crit_dict,
                levels_dict=levels_dict,
            ))

        f.weasy_pdf(this_record)

    ## print message to console - complete!
    f.pnt_notice(c.msg['console_complete'], os.path.basename(__file__))
