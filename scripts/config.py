#!/usr/bin/env python3
# python ./scripts/config.py
#
#
# chris.browne@anu.edu.au - all care and no responsibility :)
# ===========================================================

'''is a module that stores values for the scripts'''


d = {
    "feedback": "./feedback/",
    "upload": "./feedback/upload/",
    "review": "./feedback/review/",
    "archive": "./feedback/archive/",
    "charts": "./feedback/archive/charts/",
    "rubric": "./feedback/archive/rubrics/",
    "yaml": "./feedback/archive/yaml/",
    "css": "./feedback/archive/css/",
    "nlp": "./feedback/archive/nlp/",
    "json": "./feedback/archive/json/",
    "md": "./feedback/archive/md/",
    "pdf": "./feedback/archive/pdf/",
    "html": "./feedback/archive/html/",
    "wordcloud": "./feedback/archive/wordcloud/",
    "txt": "./feedback/archive/txt/",
    "files": "./files/",
    "scales": "./files/scales/",
    "jinja": "./jinja/",
}

f = {
    "students": "./files/students.csv",
    "marks": "./files/marks.csv",
    "crit_levels": "./files/crit_levels.csv",
    "data_tmc": "./files/data_tmc.csv",
    "fields": "./files/fields.csv",
    "fields_course": "./files/fields_course.csv",
    "data_client": "./files/data_client.csv",
    "data_self": "./files/data_self.csv",
    "data_shadow": "./files/data_shadow.csv",
    "data_tutor": "./files/data_tutor.csv",
    "data_conv": "./files/data_conv.csv",
    "app_config": "./files/app_config.yml",
    "wattle": "./feedback/wattle_upload.csv",
    "wattle_analysis": "./feedback/wattle_analysis_upload.csv",
    "json": "./feedback/archive/json/database.json",
    "feedback_course": "./files/feedback_course.csv",
    "all_conf": "./feedback/all_tmc_conf.pdf"
}

t = {
    "students": "./files/students.tsv",
    "marks": "./files/marks.tsv",
    "wattle": "./feedback/wattle_upload.tsv",
    "crit_levels": "./files/crit_levels.tsv",
    "data_tmc": "./files/data_tmc.tsv",
    "fields": "./files/fields.tsv",
    "fields_course": "./files/fields_course.tsv",
    "data_client": "./files/data_client.tsv",
    "data_self": "./files/data_self.tsv",
    "data_shadow": "./files/data_shadow.tsv",
    "data_tutor": "./files/data_tutor.tsv",
    "data_conv": "./files/data_conv.tsv",
    "feedback_course": "./files/feedback_course.tsv",
    "data_self_sorted": "./files/data_self_sorted.tsv",
    "data_shadow_sorted": "./files/data_shadow_sorted.tsv",
}

df = {
    "students": "students_df",
    "marks": "marks_df",
    "wattle": "wattle_df",
    "crit_levels": "crit_levels_df",
    "data_tmc": "data_tmc_df",
    "fields": "fields_df",
    "fields_course": "fields_course_df",
    "marker": "marker_df",
    "client": "client_df",
    "data_self_sorted": "self_df",
    "data_shadow_sorted": "shadow_df",
    "data_client": "data_client_df",
    "data_self": "data_self_df",
    "data_shadow": "data_shadow_df",
    "data_tutor": "data_tutor_df",
    "data_conv": "data_conv_df",
    "feedback_course": "feedback_course_df",
}

h = {
    "rubric_header": "./includes/pdf/rubric_header.html",
    "rubric_footer": "./includes/pdf/rubric_footer.html",
}

msg = {
    "console_wattle": "organising the files for wattle upload..",
    "console_duplicates": "checking for duplicates..",
    "console_secrets": "creating secrets for each student..",
    "console_upload": "creating upload file..",
    "console_start": "STARTING...",
    "console_complete": "COMPLETE...",
    "console_loading": "loading files into the scripts..",
    "console_app_config_check": "checking that ./files/app_config.yml exists..",
    "console_app_config_fail": "Can't locate the default config file. Please find it. The script will fail.",
    "console_creating_feedback_files": "Creating feedback files..",
    "console_reading_feedback_files": "Reading feedback files...",
    "console_marks_tmc_conflict": "Both Marks and TMC are true is ./files/app_config.yml. Only one can be 'true'. The script will probably fail.",
    "check_dupes": "there are duplicates in the csv: ",
    "fail_warn": "Please find it. The script will fail.",
    "console_tmc": "Creating the Team Member Contributions",
    "console_many_eyes": "Creating the Many Eyes Feedback",
    #"console_tmc": "Creating the Team Member Contributions",
}


