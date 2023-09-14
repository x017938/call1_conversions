import numpy as np
import pyarrow as pa

def subline_conversion_function(df):
    if (isinstance(df, pa.Table)):
        df = df.to_pandas()
    df['SUBLINE_CODE'] = None
    
    in_states = ['06', '07', '08', '52', '15', '19', '22', '31', '33', '36', '43', '46' ]

    # This line of code looks for states that aren't apart of our hard coded states
    non_state_specific_cond1 = (~df['STATE_NUMBER'].isin(in_states))

    # This line of code looks for states that are in our list of hard coded states and doesnt have a limit code of 21 or 22
    non_state_specific_cond2 = ((df['STATE_NUMBER'].isin(in_states)) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    # This line of code looks for states that are in our list of hard coded states and have a limit code of 21 or 22
    non_state_specific_cond3 = ((df['STATE_NUMBER'].isin(in_states)) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    non_state_specific_code = ['00','01','00']

    florida = '09'

    # This line of code looks for florida policies where the coverages are either liability or no fault with a SR2 discount code
    florida_cond1 = ((df['STATE_NUMBER'] == florida) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])) & (df['DISCOUNT_STRING'].str.contains('SR2',case='False')))

    # This line of code looks for florida policies where the coverages are either liability or no fault without a SR2 discount code
    florida_cond2 = ((df['STATE_NUMBER'] == florida) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])) & (~df['DISCOUNT_STRING'].str.contains('SR2',case='False')))

    # This line of code looks for florida policies where the coverage is physical damage
    florida_cond3 = ((df['STATE_NUMBER'] == florida) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    florida_code = ['03','01','00']
  
    nh = '28'

    nh_cond1 = ((df['STATE_NUMBER'] == nh))

    nh_code = ['08']

    nj = '29'

    # This line of code looks for nj policies where the line coverage is 1909 and the limit code is 39
    nj_cond1 = ((df['STATE_NUMBER'] == nj) & (df['LINE_COVERAGE'] == '1909') & (df['LIMIT_CODE']== '39'))

    # This line of code looks for nj policies where the line coverage either 1919 or 1967
    nj_cond2 = ((df['STATE_NUMBER'] == nj) & ((df['LINE_COVERAGE'] == '1919') | (df['LINE_COVERAGE'] == '1967')))

    # This line of code looks for nj policies where the line coverage either 1919 or 1967
    nj_cond3 = ((df['STATE_NUMBER'] == nj) & ((df['LINE_COVERAGE'] == '1909') & (df['LIMIT_CODE'] != '39')) | (df['LINE_COVERAGE'] == '1984'))

    # This line of code looks for nj policies where the coverage is physical damage
    nj_cond4 = ((df['STATE_NUMBER'] == nj) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    nj_code = ['09','07','08','01']

    ky = '16'

    # This line of code looks for ky policies where the line coverage is 1919
    ky_cond1 = ((df['STATE_NUMBER'] == ky) & (df['LINE_COVERAGE'] == '1919'))

    # This line of code looks for ky policies where the line coverage is 1910
    ky_cond2 = ((df['STATE_NUMBER'] == ky) & (df['LINE_COVERAGE'] == '1910'))

    # This line of code looks for ky policies where the coverage is physical damage
    ky_cond3 = ((df['STATE_NUMBER'] == ky) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    ky_code = ['04','01','00']

    nc = '32'

    nc_cond1 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['+F', 'OJ', 'VG', 'VM'])) & (df['LINE_COVERAGE'] == '2101'))

    nc_cond2 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'OA') & (df['LINE_COVERAGE'] == '2103'))

    nc_cond3 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == '+B') & (df['LINE_COVERAGE'] == '2104'))

    nc_cond4 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == '>Y') & (df['LINE_COVERAGE'] == '2114'))

    nc_cond5 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'OF') & (df['LINE_COVERAGE'] == '2220'))

    nc_cond6 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['>Q','VX'])) & (df['LINE_COVERAGE'] == '2101'))

    nc_cond7 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['>V', 'V7', 'X+', 'Z+'])) & (df['LINE_COVERAGE'] == '2103'))

    nc_cond8 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['+D','VS'])) & (df['LINE_COVERAGE'] == '2104'))

    nc_cond9 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['OH','VL'])) & (df['LINE_COVERAGE'] == '2114'))

    nc_cond10 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['+H', '5+', '>T', 'VY'])) & (df['LINE_COVERAGE'] == '1910'))

    nc_cond11 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'VK') & (df['LINE_COVERAGE'] == '1966'))

    nc_cond12 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin([']B','>2'])) & (df['LINE_COVERAGE'] == '1993'))

    nc_cond13 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['+E', '+G', 'V3', 'V4', 'V8', 'VB'])) & (df['LINE_COVERAGE'] == '1995'))

    nc_cond14 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin([']C','>W','W+'])) & (df['LINE_COVERAGE'] == '2001'))

    nc_cond15 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['OD', 'VE', 'VJ', '}A'])) & (df['LINE_COVERAGE'] == '2801'))

    nc_cond16 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'VF') & (df['LINE_COVERAGE'] == '2901'))

    nc_cond17 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'VH') & (df['LINE_COVERAGE'] == '1966'))

    nc_cond18 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['}D','OC'])) & (df['LINE_COVERAGE'] == '1993'))

    nc_cond19 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'] == 'OG') & (df['LINE_COVERAGE'] == '1995'))

    nc_cond20 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['3+','4+'])) & (df['LINE_COVERAGE'] == '2001'))

    nc_cond21 = ((df['STATE_NUMBER'] == nc) & (df['RATE_MANUAL_CODE'].isin(['2+','Y+'])) & (df['LINE_COVERAGE'] == '2801'))
    
    nc_code = ['04','04','04','04','04','05','05','05','05','07','07','07','07','07','07','07','08','08','08','08','08']

    penn = '37'

    is_L = [
    "5D", "}Z", "6P", "<L", "9(", ":4", "<K", "E+", "QR", "1T",
    ":V", "{Y", "1X", "8{", "QT", "1U", "<X", "JW", "6M", "49",
    "G+", "5H", "M+", "9+", "}T", "{6", "R+", "@Q", "5M", "}W",
    "6F", "$L", "6C", "V+", "4C", "D+", "N+", "$P", "4N", "XM",
    "<T", "&&", "T+", "6?", "<Q", "9{", "6N", "9?",
    "5Q", "A+", "(N", "$Q", ":A", "QW", "5K", "U+", "1L", "1V",
    "P+", "RF", "<S", ")4", "<J", "FU", "6J", "$R", "7?", "$K",
    "5P", "<V", "<Z", "-R", "8R", "$J", "WL", "}M", "RN", "FO",
    "6K", "(U", "8+", "<M", "VR", "(R", "<H", "<Y", "5B", "5J",
    ":F", "8(", "WD", "36", "<N", "F+", "1W", "FH", "QV", "VQ",
    "(T", ":N", "FS", "6R", "BM", "5L", "5R", "4J", "4M", "(S",
    "1Q", "$H", "$N", "FN", "<R", "FJ", "L+", "FT", "HK",
    "@M", "<B", "JU", "(M", "{Z", "(P", "QS", "Q+", "8Q", "}Q",
    "J+", "4R", "S+", "8H", "5F", "<A", "@G", "8?",
    "$M", "{2", "B+", "H+", "<F", "1J", "1K", "C+", "$G", "8J",
    "WH", "@H", "K+", "{3", "(H", "@L", "WB"
]

    is_F = [
        "U+", "FU", "{F", "$Q", "1T", ":F", "HN", "}M", "4N", "HV", "D+", "49", "5H", "5F", ":4",
        "9(", "<B", ":N", "FN", "T(", "6M", "<R", "}Q", "1W", "<H", "LN", "VQ", "&&", "FT", "4J",
        "7H", "WL", "6J", "$P", "QW", "FO", "QT", "}T", "5J", "J+", "{K", "QR", "RN", "1U", "QS",
        "BM", "XX", "JW", "5R", "5L", "L+", "XM", "H+", "5D", "7J", "36", "FJ", "K+", "T+", "XF",
        "J(", "WH", "QV", "4R", "<J", "4U", "$R", "M+", "FS", "B+", "6?", "6R", "P+", "1X", "WB",
        ":V", "WK", "{D", "?J", "S+", "}W", "RR", "WJ", "5P", "20", "G+", "8(", "WM", "VR", "<Y",
        "5M", "4K", "$G", "5B", "?Y", "V+", "4M", "?K", "WF", "HK", "$L", "?Z", "C+", "8{", "7?",
        "4Z", "R+", "$J", "E+", "}Z", "5Q", "WD", "9+", ")4", "RF", "6C", "6N", "4C", "RK", "{E",
        "1V", "$M", "N+", "8+", "$H", "7R", "F+", "Q+", "XQ", "FH", "4F", "9?", "A+", "$K", "<A",
        "JU", "9{", "4P", "$N", "4Y", "8?"
    ]


    penn_cond1 = ((df['STATE_NUMBER'] == penn) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22']))  & (df['RATE_MANUAL_CODE'].isin(is_F)))

    penn_cond2 = ((df['STATE_NUMBER'] == penn) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])) & (df['RATE_MANUAL_CODE'].isin(is_L)))

    penn_cond3 = ((df['STATE_NUMBER'] == penn) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    penn_code = ['05','07','00']

    mich = '21'

    mich_cond1 = ((df['STATE_NUMBER'] == mich) & (df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    mich_cond2 = ((df['STATE_NUMBER'] == mich) & (~df['LINE_COVERAGE'].str.slice(0,2).isin(['21','22'])))

    mich_code = ['00','01']

    subline_code = non_state_specific_code + florida_code + nh_code + nj_code + ky_code + nc_code + penn_code + mich_code

    df['SUBLINE_CODE'] = np.select([non_state_specific_cond1,non_state_specific_cond2,non_state_specific_cond3,florida_cond1,florida_cond2,florida_cond3,nh_cond1,nj_cond1,nj_cond2,nj_cond3,nj_cond4,ky_cond1,ky_cond2,ky_cond3,nc_cond1,nc_cond2,nc_cond3,nc_cond4,nc_cond5,nc_cond6,nc_cond7,nc_cond8,nc_cond9,nc_cond10,nc_cond11,nc_cond12,nc_cond13,nc_cond14,nc_cond15,nc_cond16,nc_cond17,nc_cond18,nc_cond19,nc_cond20,nc_cond21,penn_cond1,penn_cond2,penn_cond3,mich_cond1,mich_cond2], subline_code, df['SUBLINE_CODE'])

    return df