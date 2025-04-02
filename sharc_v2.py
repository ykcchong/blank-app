

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:20:04 2025

@author: cyk280a
"""

import codecs
import re
import streamlit as st 
import json


st.set_page_config(layout="wide")

import opencc
converter = opencc.OpenCC('s2hk.json')

with codecs.open('sharc_en_rdict.json', 'r', 'utf') as f:
    rdict_en = json.load(f)
with codecs.open('sharc_sc_rdict.json', 'r', 'utf8') as f:
    rdict_sc = json.load(f)
with codecs.open('sharc_tc_rdict.json', 'r', 'utf8') as f:
    rdict_tc = json.load(f)
with codecs.open('sharc_crossrefs.json', 'r', 'utf8') as f:
    crossrefs = json.load(f)
with codecs.open('sharc_localization_diffs_3lang.json', 'r', 'utf8') as f:
    sharc_local = json.load(f)
with codecs.open('sharc_groups.json', 'r', 'utf8') as f:
    groups = json.load(f)
with codecs.open('sharc_choosable.json', 'r', 'utf8') as f: 
    choosable = json.load(f)

language_map_list = ['en', 'sc', 'tc']

language_map = {
    'en': 'Eng',
    'sc': '简',
    'tc': '繁'
}

glossary_map = {
    'req': {
        'en': 'Specified Requirements',
        'sc': '规范要求',
        'tc': '規範要求',
    }, 
    'evidence': {
        'en': 'Evidence for compliance',
        'sc': '达标佐证资料',
        'tc': '達標佐證資料',
    },
    'good': {
        'en': 'Good',
        'sc': '良好',
        'tc': '良好',
    },
    'excellent': {
        'en': 'Excellent',
        'sc': '优良',
        'tc': '優良',
    },
    'xref': {
        'en': 'Cross Reference',
        'sc': '相互引用',
        'tc': '相互引用',
    }, 
    'diff': { 
        'en': 'Differences in Practice',
        'sc': '差异内容',
        'tc': '差異內容',
    }, 
    'cons': { 
        'en': 'Consensus Principle',
        'sc': '共识原则',
        'tc': '共識原則',
    },
    'prac': { 
        'en': 'Practice Requirements',
        'sc': '实施要求',
        'tc': '實施要求',
    },

}

rdata_map = {
    'en': rdict_en, 
    'sc': rdict_sc,
    'tc': rdict_tc,
    }

def format_multiline(text): 
    text = re.sub(r'\n+', '<br>', text)
    return text

def get_clause_name_bilingual(clause): 
    return f'{rdict_tc[clause][0]} | {rdict_en[clause][0]}'

# st.title('The SHARK')

tab2, tab1 = st.tabs(('BySubject', 'ByClause'))

def display_clause(selected_clause, selected_languages, bold, disable_notification_localization=False, original_in_expander=True): 
    labels_req, labels_evidence, labels_good, labels_excellent = [], [], [], []
    labels_diff, labels_cons, labels_prac = [], [], []
    data_clauseno, data_clausename, data_req, data_evidence, data_good, data_excellent= [], [], [], [], [], []
    data_diff, data_cons, data_prac = [], [], []

    for language in language_map_list: 
        l_req = glossary_map['req'][language]
        l_evidence = glossary_map['evidence'][language]
        l_good = glossary_map['good'][language]
        l_excellent = glossary_map['excellent'][language]
        l_diff = glossary_map['diff'][language]
        l_cons = glossary_map['cons'][language]
        l_prac = glossary_map['prac'][language]
        
        d_clauseno = rdata_map[language][selected_clause][0]
        d_clausename = rdata_map[language][selected_clause][1]
        d_req = rdata_map[language][selected_clause][2]
        d_evidence = rdata_map[language][selected_clause][3]
        d_good = rdata_map[language][selected_clause][4]
        d_excellent = rdata_map[language][selected_clause][5]

        if selected_clause in sharc_local.keys(): 
            d_diff = sharc_local[selected_clause][language]['diff']
            d_cons = sharc_local[selected_clause][language]['cons']
            d_prac = sharc_local[selected_clause][language]['prac']
        else: 
            d_diff, d_cons, d_prac = '', '', ''

        if language in selected_languages: 
            labels_req.append(l_req)
            labels_evidence.append(l_evidence)
            labels_good.append(l_good)
            labels_excellent.append(l_excellent)
            data_clauseno.append(d_clauseno)
            data_clausename.append(d_clausename)
            data_req.append(format_multiline(d_req))
            data_evidence.append(format_multiline(d_evidence))
            data_good.append(format_multiline(d_good))
            data_excellent.append(format_multiline(d_excellent))

            if selected_clause in sharc_local.keys(): 
                labels_diff.append(l_diff)
                labels_cons.append(l_cons)
                labels_prac.append(l_prac)

                data_diff.append(format_multiline(d_diff))
                data_cons.append(format_multiline(d_cons))
                data_prac.append(format_multiline(d_prac))

    if bold: 
        insertbold = '<b>'
        insertboldend = '</b>'
    else:
        insertbold, insertboldend = '', ''  

    if len(selected_languages) == 1:
        tableitems = f'<p>{insertbold}__item1__{insertboldend}</p>'
    elif 'en' in selected_languages: 
        if len(selected_languages) == 2:
            tableitems = f'<table border="0" width="100%" cellspacing="1" cellpadding="0">\
                <tr><td width="60%" valign="top">{insertbold}__item1__{insertboldend}</td>\
                    <td width="40%" valign="top">{insertbold}__item2__{insertboldend}</td>\
                </tr></table>'
        elif len(selected_languages) == 3:
            tableitems = f'<table border="0" width="100%" cellspacing="1" cellpadding="0">\
                <tr><td width="50%" valign="top">{insertbold}__item1__{insertboldend}</td>\
                    <td width="25%" valign="top">{insertbold}__item2__{insertboldend}</td>\
                        <td width="25%" valign="top">{insertbold}__item3__{insertboldend}</td>\
                </tr></table>'
    else:
        if len(selected_languages) == 2:
            tableitems = f'<table border="0" width="100%" cellspacing="1" cellpadding="0">\
                <tr><td width="50%" valign="top">{insertbold}__item1__{insertboldend}</td>\
                    <td width="50%" valign="top">{insertbold}__item2__{insertboldend}</td></tr></table>'

    label_req = ' | '.join(labels_req)
    label_evidence = ' | '.join(labels_evidence)
    label_good = ' | '.join(labels_good)
    label_excellent = ' | '.join(labels_excellent)

    if selected_clause in sharc_local.keys():
        label_diff = ' | '.join(labels_diff)
        label_cons = ' | '.join(labels_cons)
        label_prac = ' | '.join(labels_prac)

    data_display_req = tableitems
    data_display_evidence = tableitems
    data_display_good = tableitems
    data_display_excellent = tableitems
    data_display_diff = tableitems
    data_display_cons = tableitems
    data_display_prac = tableitems

    for idx in range(len(selected_languages)):
        data_display_req = re.sub('__item' + str(idx+1) + '__', data_req[idx], data_display_req)
        data_display_evidence = re.sub('__item' + str(idx+1) + '__', data_evidence[idx], data_display_evidence)
        data_display_good = re.sub('__item' + str(idx+1) + '__', data_good[idx], data_display_good)
        data_display_excellent = re.sub('__item' + str(idx+1) + '__', data_excellent[idx], data_display_excellent)
        if selected_clause in sharc_local.keys():
            data_display_diff = re.sub('__item' + str(idx+1) + '__', data_diff[idx], data_display_diff)
            data_display_cons = re.sub('__item' + str(idx+1) + '__', data_cons[idx], data_display_cons)
            data_display_prac = re.sub('__item' + str(idx+1) + '__', data_prac[idx], data_display_prac)

    for clauseno, clausename in zip(data_clauseno, data_clausename): 
        st.html(f'<div style="font-size: 120%; color: DarkOliveGreen;"><b>{clauseno}.</b>  {clausename}</div>')

    if selected_clause in sharc_local.keys(): 
        if not disable_notification_localization: 
            # if 'en' in selected_languages:
            #     if len(selected_languages) == 1:
            #         st.info('Local customizations are applicable for this clause')
            #     else: 
            #         st.info('因應專家小組建議，此條目實施時會因應區域政策差異有不同的實施要求\nLocal customizations are applicable for this clause (Automated translation)')
            # else:
            if 'tc' in selected_languages: 
                st.info('因應專家小組建議，此條目實施時會因應區域政策差異有不同的實施要求')
            elif 'sc' in selected_languages:
                st.info('因应专家小组建议，此条目实施时会因应区域政策差异有不同的实施要求')
            else:
                st.info('Local customizations are applicable for this clause')

        st.html(f'<div style="page-break-inside: avoid;"><div style="font-size: 120%; color: FireBrick;">{label_diff}</div>{data_display_diff}</div>')
        st.html(f'<div style="page-break-inside: avoid;"><div style="font-size: 120%; color: darkcyan;">{label_cons}</div>{data_display_cons}</div>')
        st.html(f'<div style="page-break-inside: avoid;"><div style="font-size: 120%; color: deeppink;">{label_prac}</div>{data_display_prac}</div>')

    if 'en' in selected_languages:
        if len(selected_languages) == 1:
            ciha_std = 'Below lists the original clauses\n\nClick to expand'
        else: 
            ciha_std = '下列爲標準原文 Below lists the original clauses\n\n按此張開 Click to expand'
    else:
        if 'tc' in selected_languages: 
            ciha_std = '下列爲標準原文'
        else:
            ciha_std = '以下为标准原文'
                    
    if selected_clause in sharc_local.keys(): 
        if original_in_expander: 
            with st.expander(ciha_std, expanded=False): 
                st.html(f'<div style="font-size: 120%; color: FireBrick;">{label_req}</div>{data_display_req}')
                st.html(f'<div style="font-size: 120%; color: RoyalBlue;">{label_evidence}</div>{data_display_evidence}')
        else:
            st.html(f'<div style="font-size: 120%; color: FireBrick;">{label_req}</div>{data_display_req}')
            st.html(f'<div style="font-size: 120%; color: RoyalBlue;">{label_evidence}</div>{data_display_evidence}')
    else:
        st.html(f'<div style="font-size: 120%; color: FireBrick;">{label_req}</div>{data_display_req}')
        st.html(f'<div style="font-size: 120%; color: RoyalBlue;">{label_evidence}</div>{data_display_evidence}')


    st.html(f'<div style="font-size: 120%; color: GoldenRod;">{label_good}</div>{data_display_good}')
    st.html(f'<div style="font-size: 120%; color: Green;">{label_excellent}</div>{data_display_excellent}')

#
#
#
#
#
#

with tab1:
    clause_list = [x for x in rdict_tc.keys() if len(rdict_tc[x][2]) > 2]
    t1_input_col1_1, t1_input_col1_2 = st.columns((4,1))
    selected_clause = t1_input_col1_1.selectbox('Select clause', clause_list, format_func=get_clause_name_bilingual)
    selected_languages = set(t1_input_col1_2.segmented_control('Language to display', options=list(language_map.keys()), format_func=language_map.get, selection_mode='multi', default=['en', 'tc']))

    t1_input_col2_1, t1_input_col2_2, t1_input_col2_3 = st.columns((1,1,1))
    bold = t1_input_col2_1.checkbox('Bold clauses', value=False, key='t1_show_bold')
    disable_notification_localization = t1_input_col2_2.checkbox('Don\'t notify for localization', value=False, key='t1_disable_localization')
    original_in_expander = t1_input_col2_3.checkbox('Original in expander if localized', value=True, key='t1_show_original_in_expander')

    if len(selected_languages) == 0: 
        st.write('Choose a language. ')
        st.stop()

    if 'en' in selected_languages:
        if len(selected_languages) == 1:
            st.subheader('Selected Clause')
        else: 
            st.subheader('Selected Clause | 條目')
    else:
        st.subheader('條目')

    display_clause(selected_clause, selected_languages, bold, disable_notification_localization, original_in_expander)

    if selected_clause in crossrefs.keys(): 
        if 'en' in selected_languages:
            if len(selected_languages) == 1:
                st.subheader('Cross References')
            else: 
                st.subheader('Cross References | 相互引用')
        else:
            st.subheader('相互引用')

        crossref_list = crossrefs[selected_clause]
        for item in sorted(crossref_list): 
            display_clause(item, selected_languages, bold, disable_notification_localization, original_in_expander)



with tab2: 
    t2_input_col1_1, t2_input_col1_2 = st.columns((4,1))
    chosen_group = t2_input_col1_1.selectbox('Select a group', list(range(len(choosable))), 0, format_func=lambda x:converter.convert(choosable[x][1]))
    selected_languages = set(t2_input_col1_2.segmented_control('Language to display', options=list(language_map.keys()), format_func=language_map.get, selection_mode='multi',  key='tab2inp_lang', default=['en', 'tc']), )
    t2_input_col2_1, t2_input_col2_2, t2_input_col2_3 = st.columns((1,1,1))
    bold = t2_input_col2_1.checkbox('Bold clauses', value=False, key='t2_show_bold')
    disable_notification_localization = t2_input_col2_2.checkbox('Don\'t notify for localization', value=False, key='t2_disable_localization')
    original_in_expander = t2_input_col2_3.checkbox('Original in expander if localized', value=True, key='t2_show_original_in_expander')

    if len(selected_languages) == 0: 
        st.write('Choose a language. ')
        st.stop()

    group_title = choosable[chosen_group][1]
    #st.subheader(converter.convert(group_title))
    st.html(f'<div style="font-size: 150%; color: Black; font-weight: bold;">{converter.convert(re.sub(r'\|\|\ ([0-9]+)', r': Section \1<br>', group_title))}</div>')

    full_id = choosable[chosen_group][0]
    group_id = full_id[0]
    subject_id = full_id[1]

    ename, cname = groups[group_id]['name']
    tcname = converter.convert(cname)

    subj_ename, subj_cname = groups[group_id]['content'][subject_id]['name']
    subj_tcname = converter.convert(subj_cname)
    for item in choosable[chosen_group][2]: 
        display_clause(item, selected_languages, bold, disable_notification_localization, original_in_expander)
    
