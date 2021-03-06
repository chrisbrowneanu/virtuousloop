#!/usr/bin/env python3
# python ./scripts/feedback_course.py
#
#
# chris.browne@anu.edu.au - all care and no responsibility :)
# ===========================================================

'''turns the feedback_course spreadsheet into pdf feedback'''

import os
from bs4 import BeautifulSoup
import pandas as pd
import config as c
import functions as f


def feedback_course():
    
    cfg = f.load_config()
    f.pnt_notice(c.msg['console_start'], os.path.basename(__file__))
    f.pnt_info(c.msg["console_loading"])

    tutors = f.load_tsv('feedback_course')
    tutors.drop_duplicates(subset=['tutor_name'], keep='first', inplace=True)
    feedback_course_df = f.load_tsv('feedback_course')
    crit_levels = f.load_tsv('crit_levels')
    crit = f.filter_row('fields', 'field', 'crit_')
    comm = f.filter_row('fields', 'field', 'comment_')

    tutor_list = f.create_list(tutors, 'tutor_name')
    crit_levels_list = f.create_list(crit_levels, 'index')

    f.pnt_info(c.msg["console_creating_feedback_files"])
    for i, row in crit.iterrows():
        this_crit = row['field']
        this_crit_list = []
        for tutor in tutor_list:
            this_tutor_df = feedback_course_df[feedback_course_df['tutor_name'].str.contains(tutor)]
            this_tutor_crit = []
            this_header = [tutor]
            for val in crit_levels_list:
                this_sum = (this_tutor_df[this_crit] == val).sum()
                this_tutor_crit.append(this_sum)
            this_crit_list.append(this_tutor_crit)
            this_crit_this_tutor = pd.DataFrame(this_tutor_crit, columns=this_header, index=crit_levels_list)
            f.make_feedback_chart(this_crit_this_tutor, c.d['charts'] + this_crit + "_" + tutor + ".png")
        
        this_crit_all_tutors = pd.DataFrame(this_crit_list, columns=crit_levels_list, index=tutor_list)
        this_crit_all_tutors = this_crit_all_tutors.T
        f.make_feedback_chart(this_crit_all_tutors, c.d['charts'] + this_crit + "_all.png")

    with open(c.d['yaml'] + 'all.yaml', 'w') as out:
        f.pandoc_yaml(out, 'All Tutors')

    with open(c.d['css'] + 'all_conf.css', 'w') as out:
        f.pandoc_css(out, 'Course Feedback', 'conf')

    # open up a file to print to
    with open(c.d['md'] + 'all_charts.md', 'w') as out:
        print("# Quantitative Feedback\n\n", file=out)
        for i, row in crit.iterrows():
            this_crit = str(row['field'])
            this_text = str(row['description'])
            this_image = c.d['charts'] + this_crit + "_all.png"
            print("### " + this_text + "\n\n", file=out)
            print("![](../../." + this_image + ")\n\n", file=out)

    confidential_files = [c.d['md'] + 'all_charts.md']

    for tutor in tutor_list:
        print(tutor)
        this_tutor_df = feedback_course_df[feedback_course_df['tutor_name'].str.contains(tutor)]
        with open(c.d['yaml'] + tutor + '.yaml', 'w') as out:
            f.pandoc_yaml(out, tutor)

        with open(c.d['css'] + tutor + '.css', 'w') as out:
            f.pandoc_css(out, tutor, 'anon')

        f_out = open(c.d['md'] + tutor + '.md', 'w')

        with f_out as out:
            try: 
                for i, row in crit.iterrows():
                    this_crit = str(row['field'])
                    this_text = str(row['description'])
                    this_image = c.d['charts'] + this_crit + "_" + tutor + ".png"
                    print("### " + this_text + "\n", file=out)
                    print("![](../../." + this_image + ")\n", file=out)

                for i, row in comm.iterrows():
                    this_field = str(row['field'])
                    this_description = str(row['description'])

                    this_df = this_tutor_df[['tutor_name',this_field]].dropna()

                    if this_field != 'comment_confidential':
                        print("\n\n## " + this_description + "\n\n", file=out)
                        for i, i_row in this_df.iterrows():
                            this_text = str(i_row[this_field])
                            if (this_text != "" or this_text != "nan" or this_text != "N/A"):
                                this_text_clean = BeautifulSoup(this_text, features="html5lib")
                                print("**Student Comment**\n\n" + this_text_clean.get_text() + "\n\n", file=out)
            finally:
                f_out.close()

        f.pandoc_html_single(tutor)
        f.pandoc_pdf(tutor)

        with open(c.d['md'] + tutor + '_conf.md', 'w') as out:
            print("\n\n# Feedback for " + tutor + "\n\n", file=out)
            confidential_files.append(c.d['md'] + tutor + '_conf.md')

            # loop through the comment columns
            for i, row in comm.iterrows():
                this_field = str(row['field'])
                this_description = str(row['description'])

                this_df = this_tutor_df[['tutor_name', 'user', this_field]].dropna()

                print("\n\n## " + this_description + "\n\n", file=out)
                for i, i_row in this_df.iterrows():
                    this_text = str(i_row[this_field])
                    this_user = str(i_row['user'])
                    if (this_text != "" or this_text != "nan" or this_text != "N/A"):
                        this_text_clean = BeautifulSoup(this_text, features="html5lib")
                        print("**" + this_user + "**\n\n" + this_text_clean.get_text() + "\n\n", file=out)

    with open(c.d['md'] + "all.md", 'w') as outfile:
        for fname in confidential_files:
            with open(fname) as infile:
                outfile.write(infile.read())

    f.pandoc_html_toc('all', 'all', 'conf')
    f.pandoc_pdf('all')

    f.pnt_notice(c.msg['console_complete'], os.path.basename(__file__))
