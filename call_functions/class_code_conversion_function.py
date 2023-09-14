import numpy as np
import pyarrow as pa

def class_code_conversion_function(df):
    if (isinstance(df, pa.Table)):
        df = df.to_pandas()
    df['AGE'] = df['AGE'].astype(int)
    df['CLASS_CODE'] = None
    
    state_except = set(['09','52','21','25','29','31','32','37'])
    non_business = set(['1','3','4'])
    non_farm_non_business = set(['1','4'])
    business_non_farm = set(['1','2','4'])

    # This line of code looks for single car farm polices where it's a female over 0 or a male 25 or older and since this is single car farm, the use is always non business
    single_car_pol_cond1 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for single car non-farm polices where it's a female over 0 or a male 25 or older
    single_car_pol_cond2 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(non_farm_non_business)) & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for single car farm polices where it's a male under 25. This conversion calls for either business or non-business, so just using the the farm use code is fine.
    single_car_pol_cond3 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & ((df['DRIVER_SEX'] == 'M') & (df['AGE'] < 25))

    # This line of code looks for single car non-farm polices where it's a male under 25. This conversion calls for either business or non-business, but since this is non-farm, we look for use codes of pleasure, commuting and business
    single_car_pol_cond4 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(business_non_farm)) & (~df['STATE_NUMBER'].isin(state_except))) & ((df['DRIVER_SEX'] == 'M') & (df['AGE'] < 25))

    # This line of code looks for single car non-farm polices where it's a female over 0 or a male 25 or older and has a use case of business
    single_car_pol_cond5 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for single car farm polices where the operator is 65 or older and since this is a single car farm, the use is always non business
    single_car_pol_cond6 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)

    # This line of code looks for single car non-farm polices where the operator is 65 or older and the use case is non-business
    single_car_pol_cond7 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(non_farm_non_business)) & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)

    # This line of code looks for single car non-farm polices where the operator is 65 or older and the use case is business
    single_car_pol_cond8 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)
    

    # This line of code looks for multi car farm polices where it's a female over 0 or a male 25 or older and since this is multi car farm, the use is always non business
    multi_car_pol_cond1 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for multi car non-farm polices where it's a female over 0 or a male 25 or older
    multi_car_pol_cond2 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(non_farm_non_business)) & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for multi car farm polices where it's a male under 25. This conversion calls for either business or non-business, so just using the the farm use code is fine.
    multi_car_pol_cond3 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & ((df['DRIVER_SEX'] == 'M') & (df['AGE'] < 25))

    # This line of code looks for multi car non-farm polices where it's a male under 25. This conversion calls for either business or non-business, but since this is non-farm, we look for use codes of pleasure, commuting and business
    multi_car_pol_cond4 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(business_non_farm)) & (~df['STATE_NUMBER'].isin(state_except))) & ((df['DRIVER_SEX'] == 'M') & (df['AGE'] < 25))

    # This line of code looks for multi car non-farm polices where it's a female over 0 or a male 25 or older and has a use case of business
    multi_car_pol_cond5 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (~df['STATE_NUMBER'].isin(state_except))) & (((df['DRIVER_SEX'] == 'F') & (df['AGE'] > 0)) | ((df['DRIVER_SEX'] == 'M') & (df['AGE'] >= 25)))

    # This line of code looks for multi car farm polices where the operator is 65 or older and since this is a multi car farm, the use is always non business
    multi_car_pol_cond6 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)

    # This line of code looks for multi car non-farm polices where the operator is 65 or older and the use case is non-business
    multi_car_pol_cond7 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(non_farm_non_business)) & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)

    # This line of code looks for multi car non-farm polices where the operator is 65 or older and the use case is business
    multi_car_pol_cond8 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (~df['STATE_NUMBER'].isin(state_except))) & (df['AGE'] >= 65)
    
    single_car_pol_code = ['12030','12000','16030','16000','14000','15630','15600','15500']
    multi_car_pol_code = ['12010','12020','16030','16000','14020','15610','15620','15520']
    
    florida = '09'

    # This line of code looks for single car farm polices where it's a single male under 25 that's not the principal operator
    florida_single_car_cond1 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for single car non-farm polices where it's a single male under 25 that's not the principal operator
    florida_single_car_cond2 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for single car farm polices where its a married male under 25
    florida_single_car_cond3 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for single car non-farm polices where its a marred male under 25
    florida_single_car_cond4 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for single car farm polices where it's a single male under 25 that's the principal operator
    florida_single_car_cond5 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for single car non-farm polices where it's a single male under 25 that's the principal operator
    florida_single_car_cond6 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for single car farm policies where its a female under 25
    florida_single_car_cond7 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'F')))

    # This line of code looks for single car non-farm policies where its a female under 25
    florida_single_car_cond8 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'F')))

    # This line of code looks for single car farm policies where its an operator that is between the ages of 25-29
    florida_single_car_cond9 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 25) & (df['AGE'] <= 29)))

    # This line of code looks for single car non-farm policies where its an operator that is between the ages of 25-29
    florida_single_car_cond10 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 25) & (df['AGE'] <= 29)))

    # This line of code looks for single car farm policies where its an operator 65 and over
    florida_single_car_cond11 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for single car policies where its an operator 645 and over with a use code pleasure
    florida_single_car_cond12 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for single car policies where its an operator 645 and over with a use code business
    florida_single_car_cond13 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for a single car farm policies where a class code hasn't been given yet
    florida_single_car_cond14 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida))

    # This line of code looks for single car policies where a class code has not been given and the use code is pleasure
    florida_single_car_cond15 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['STATE_NUMBER'] == florida))

    # This line of code looks for single car policies where a class code has not been given and the use code is business
    florida_single_car_cond16 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == florida))
    
    
    # This line of code looks for multi car farm polices where it's a multi male under 25 that's not the principal operator
    florida_multi_car_cond1 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for multi car non-farm polices where it's a multi male under 25 that's not the principal operator
    florida_multi_car_cond2 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for multi car farm polices where its a married male under 25
    florida_multi_car_cond3 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for multi car non-farm polices where its a marred male under 25
    florida_multi_car_cond4 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for multi car farm polices where it's a multi male under 25 that's the principal operator
    florida_multi_car_cond5 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for multi car non-farm polices where it's a multi male under 25 that's the principal operator
    florida_multi_car_cond6 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['DRIVER_MARITAL_STATUS'] == 'S')))

    # This line of code looks for multi car farm policies where its a female under 25
    florida_multi_car_cond7 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'F')))

    # This line of code looks for multi car non-farm policies where its a female under 25
    florida_multi_car_cond8 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida) & (df['AGE'] < 25)) & (((df['DRIVER_SEX'] == 'F')))

    # This line of code looks for multi car farm policies where its an operator that is between the ages of 25-29
    florida_multi_car_cond9 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 25) & (df['AGE'] <= 29)))

    # This line of code looks for multi car non-farm policies where its an operator that is between the ages of 25-29
    florida_multi_car_cond10 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 25) & (df['AGE'] <= 29)))

    # This line of code looks for multi car farm policies where its an operator 65 and over
    florida_multi_car_cond11 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for multi car policies where its an operator 645 and over with a use code pleasure
    florida_multi_car_cond12 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for multi car policies where its an operator 645 and over with a use code business
    florida_multi_car_cond13 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == florida)) & (((df['AGE'] >= 65)))

    # This line of code looks for a multi car farm policies where a class code hasn't been given yet
    florida_multi_car_cond14 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == florida))

    # This line of code looks for multi car policies where a class code has not been given and the use code is pleasure
    florida_multi_car_cond15 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['STATE_NUMBER'] == florida))

    # This line of code looks for multi car policies where a class code has not been given and the use code is business
    florida_multi_car_cond16 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == florida))
    
    florida_single_car_code = ['16130','16100','16230','16200','16330','16300','16430','16400','16530','16500','15130','15100','15500','12130','12100','14000']
    florida_multi_car_code = ['16110','16120','16210','16220','16310','16320','16410','16420','16510','16520','15110','15120','15520','12110','12120','14020']
    
    hawaii = '52'

    # This line of code looks for single car polices where it's a use code of pleasure
    hawaii_single_car_cond1 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & (df['USE_CODE'] == '1'))

    # This line of code looks for single car polices where it's a use code of communting
    hawaii_single_car_cond2 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & (df['USE_CODE'] == '4'))

    # This line of code looks for single car polices where it's a use code of business
    hawaii_single_car_cond3 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & ((df['USE_CODE'] == '2') | (df['USE_CODE'] == '3')))
    
    # This line of code looks for multi car polices where it's a use code of pleasure
    hawaii_multi_car_cond1 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & (df['USE_CODE'] == '1'))

    # This line of code looks for multi car polices where it's a use code of communting
    hawaii_multi_car_cond2 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & (df['USE_CODE'] == '4'))

    # This line of code looks for multi car polices where it's a use code of business
    hawaii_multi_car_cond3 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'] == hawaii) & ((df['USE_CODE'] == '2') | (df['USE_CODE'] == '3')))
    
    hawaii_single_car_code = ['12140','12240','14040']
    hawaii_multi_car_code = ['12160','12260','14060']
    
    mich_mont = ('21','25')
   
    # This line of code looks for single car farm polices where it's principal operator less than 20
    mich_mont_single_car_cond1 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for single car non-farm polices where it's principal operator less than 20
    mich_mont_single_car_cond2 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for single car farm policies where its principal operator is within ages 21-24
    mich_mont_single_car_cond3 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car non-farm policies where its principal operator is within ages 21-24
    mich_mont_single_car_cond4 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car farm polices where it's non-principal operator less than 20
    mich_mont_single_car_cond5 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for single car non-farm polices where it's non-principal operator less than 20
    mich_mont_single_car_cond6 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for single car farm policies where its non-principal operator is within ages 21-24
    mich_mont_single_car_cond7 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car non-farm policies where its non-principal operator is within ages 21-24
    mich_mont_single_car_cond8 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car farm policies where the principal opertator is 65 and older
    mich_mont_single_car_cond9 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 65)))

    # This line of code looks for single car non-farm policies where the principal opertator is 65 and older
    mich_mont_single_car_cond10 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 65)))

    # This line of code looks for single car farm policies where the class code is still blank
    mich_mont_single_car_cond11 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'].isin(mich_mont)))

    # This line of code looks for single car non-farm policies where the class code is still blank and the use code is pleasure
    mich_mont_single_car_cond12 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['STATE_NUMBER'].isin(mich_mont)))

    # This line of code looks for single car non-farm policies where the class code is still blank and the use code is business
    mich_mont_single_car_cond13 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'].isin(mich_mont)))
    
    
    # This line of code looks for multi car farm polices where it's principal operator less than 20
    mich_mont_multi_car_cond1 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for multi car non-farm polices where it's principal operator less than 20
    mich_mont_multi_car_cond2 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for multi car farm policies where its principal operator is within ages 21-24
    mich_mont_multi_car_cond3 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car non-farm policies where its principal operator is within ages 21-24
    mich_mont_multi_car_cond4 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car farm polices where it's non-principal operator less than 20
    mich_mont_multi_car_cond5 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for multi car non-farm polices where it's non-principal operator less than 20
    mich_mont_multi_car_cond6 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] < 25) & (df['AGE'] <= 20)))

    # This line of code looks for multi car farm policies where its non-principal operator is within ages 21-24
    mich_mont_multi_car_cond7 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car non-farm policies where its non-principal operator is within ages 21-24
    mich_mont_multi_car_cond8 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car farm policies where the principal opertator is 65 and older
    mich_mont_multi_car_cond9 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 65)))

    # This line of code looks for multi car non-farm policies where the principal opertator is 65 and older
    mich_mont_multi_car_cond10 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['STATE_NUMBER'].isin(mich_mont)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['AGE'] >= 65)))

    # This line of code looks for multi car farm policies where the class code is still blank
    mich_mont_multi_car_cond11 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'].isin(mich_mont)))

    # This line of code looks for multi car non-farm policies where the class code is still blank and the use code is pleasure
    mich_mont_multi_car_cond12 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['STATE_NUMBER'].isin(mich_mont)))

    # This line of code looks for multi car non-farm policies where the class code is still blank and the use code is business
    mich_mont_multi_car_cond13 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['CLASS_CODE'].isnull()) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'].isin(mich_mont)))
    
    mich_mont_single_car_code = ['16910','16910','16930','16930','16950','16950','16970','16970','17000','17000','12130','12100','14000']
    mich_mont_multi_car_code = ['16920','16920','16940','16940','16960','16960','16980','16980','17000','17000','12110','12120','14020']
    
    nj = '29'
    
    # This line of code looks for single car farm policies where its an unmarried female 20 or less with a discount code of 'DDF'
    nj_single_car_cond1 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried female 20 or less with a discount code of 'DDF'
    nj_single_car_cond2 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an unmarried female 20 or less without a discount code of 'DDF'
    nj_single_car_cond3 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried female 20 or less without a discount code of 'DDF'
    nj_single_car_cond4 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an married male 20 or less with a discount code of 'DDF'
    nj_single_car_cond5 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an married male 20 or less with a discount code of 'DDF'
    nj_single_car_cond6 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an married male 20 or less without a discount code of 'DDF'
    nj_single_car_cond7 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an married male 20 or less without a discount code of 'DDF'
    nj_single_car_cond8 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an married male 21-24
    nj_single_car_cond9 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for single car non-farm policies where its an married male 21-24
    nj_single_car_cond10 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for single car farm policies where its an unmarried male 20 or less thats not the principal operator with a discount code of 'DDF'
    nj_single_car_cond11 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried male 20 or less thats not the principal operator with a discount code of 'DDF'
    nj_single_car_cond12 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an unmarried male 20 or less thats not the principal operator without a discount code of 'DDF'
    nj_single_car_cond13 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried male 20 or less thats not the principal operator without a discount code of 'DDF'
    nj_single_car_cond14 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an unmarried male 21-24
    nj_single_car_cond15 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for single car non-farm policies where its an unmarried male 21-24
    nj_single_car_cond16 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for single car farm policies where its an unmarried male 20 or less thats the principal operator with a discount code of 'DDF'
    nj_single_car_cond17 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried male 20 or less thats the principal operator with a discount code of 'DDF'
    nj_single_car_cond18 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an unmarried male 20 or less thats the principal operator without a discount code of 'DDF'
    nj_single_car_cond19 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car non-farm policies where its an unmarried male 20 or less thats the principal operator without a discount code of 'DDF'
    nj_single_car_cond20 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm policies where its an unmarried male 21-24 thats the principal operator
    nj_single_car_cond21 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for single car non-farm policies where its an unmarried male 21-24 thats the principal operator
    nj_single_car_cond22 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for single car farm policies where its an unmarried male 25-29 thats the principal operator
    nj_single_car_cond23 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 25) & (df['AGE'] <=29)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for single car non-farm policies where its an unmarried male 25-29 thats the principal operator
    nj_single_car_cond24 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 25) & (df['AGE'] <=29)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for single car farm policies where the principal operator is 65 or older
    nj_single_car_cond25 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for single car policies where the principal operator is 65 or older and a use code of pleasure
    nj_single_car_cond26 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for single car policies where the principal operator is 65 or older and a use code of business
    nj_single_car_cond27 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for single car farm policies where the class code is null or not equal to '9405'
    nj_single_car_cond28 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for single car policies where the class code is null or not equal to '9405' and a use code of pleasure
    nj_single_car_cond29 = ((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for single car policies where the class code is null or not equal to '9405' and a use code of business
    nj_single_car_cond30 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))
    
    
    # This line of code looks for multi car farm policies where its an unmarried female 20 or less with a discount code of 'DDF'
    nj_multi_car_cond1 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried female 20 or less with a discount code of 'DDF'
    nj_multi_car_cond2 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an unmarried female 20 or less without a discount code of 'DDF'
    nj_multi_car_cond3 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried female 20 or less without a discount code of 'DDF'
    nj_multi_car_cond4 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'F') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an married male 20 or less with a discount code of 'DDF'
    nj_multi_car_cond5 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an married male 20 or less with a discount code of 'DDF'
    nj_multi_car_cond6 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an married male 20 or less without a discount code of 'DDF'
    nj_multi_car_cond7 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an married male 20 or less without a discount code of 'DDF'
    nj_multi_car_cond8 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & (df['AGE'] <= 20) & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an married male 21-24
    nj_multi_car_cond9 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for multi car non-farm policies where its an married male 21-24
    nj_multi_car_cond10 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] == 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for multi car farm policies where its an unmarried male 20 or less thats not the principal operator with a discount code of 'DDF'
    nj_multi_car_cond11 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried male 20 or less thats not the principal operator with a discount code of 'DDF'
    nj_multi_car_cond12 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an unmarried male 20 or less thats not the principal operator without a discount code of 'DDF'
    nj_multi_car_cond13 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried male 20 or less thats not the principal operator without a discount code of 'DDF'
    nj_multi_car_cond14 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an unmarried male 21-24
    nj_multi_car_cond15 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for multi car non-farm policies where its an unmarried male 21-24
    nj_multi_car_cond16 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24))))

    # This line of code looks for multi car farm policies where its an unmarried male 20 or less thats the principal operator with a discount code of 'DDF'
    nj_multi_car_cond17 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried male 20 or less thats the principal operator with a discount code of 'DDF'
    nj_multi_car_cond18 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an unmarried male 20 or less thats the principal operator without a discount code of 'DDF'
    nj_multi_car_cond19 = (((df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car non-farm policies where its an unmarried male 20 or less thats the principal operator without a discount code of 'DDF'
    nj_multi_car_cond20 = (((df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & (df['AGE'] <= 20) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & ((~df['DISCOUNT_STRING'].str.contains('DDF',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm policies where its an unmarried male 21-24 thats the principal operator
    nj_multi_car_cond21 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for multi car non-farm policies where its an unmarried male 21-24 thats the principal operator
    nj_multi_car_cond22 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 21) & (df['AGE'] <=24)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for multi car farm policies where its an unmarried male 25-29 thats the principal operator
    nj_multi_car_cond23 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 25) & (df['AGE'] <=29)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for multi car non-farm policies where its an unmarried male 25-29 thats the principal operator
    nj_multi_car_cond24 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['STATE_NUMBER'] == nj)) & ((df['DRIVER_SEX'] == 'M') & (df['DRIVER_MARITAL_STATUS'] != 'M') & ((df['AGE'] >= 25) & (df['AGE'] <=29)) & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')))

    # This line of code looks for multi car farm policies where the principal operator is 65 or older
    nj_multi_car_cond25 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for multi car policies where the principal operator is 65 or older and a use code of pleasure
    nj_multi_car_cond26 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for multi car policies where the principal operator is 65 or older and a use code of business
    nj_multi_car_cond27 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for multi car farm policies where the class code is null or not equal to '9405'
    nj_multi_car_cond28 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for multi car policies where the class code is null or not equal to '9405' and a use code of pleasure
    nj_multi_car_cond29 = ((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & ((df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))

    # This line of code looks for multi car policies where the class code is null or not equal to '9405' and a use code of business
    nj_multi_car_cond30 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2')) & ((df['CLASS_CODE'].isnull()) | (df['CLASS_CODE'] != '9405')) & (df['STATE_NUMBER'] == nj))
    
    nj_single_car_code = ['18881','18880','18891','18890','18901','18900','18911','18910','18921','18920','18931','18930','18941','18940','18951','18950','18961','18960','18971','18970','18981','18980','18991','18990','18841','18840','18790','18811','18810','18870']
    nj_multi_car_code = ['18883','18882','18893','18892','18903','18902','18913','18912','18923','18922','18933','18932','18943','18942','18953','18952','18963','18962','18973','18972','18983','18982','18993','18992','18843','18842','18792','18813','18812','18872']
    
    penn = '37'
    
    # This line of code looks for single car farm policies where the principal operator married and 20 or less
    penn_single_car_cond1 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for single car non-farm policies where the principal operator married and 20 or less
    penn_single_car_cond2 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for single car farm policies where the principal operator is 21-24
    penn_single_car_cond3 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car non-farm policies where the principal operator is 21-24
    penn_single_car_cond4 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for single car farm policies where the principal operator married and 20 or less
    penn_single_car_cond5 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] != 'M')))

    # This line of code looks for single car non-farm policies where the principal operator married and 20 or less
    penn_single_car_cond6 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] != 'M')))

    # This line of code looks for single car farm policies where the principal operator is 21-24 and unmarried
    penn_single_car_cond7 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for single car non-farm policies where the principal operator is 21-24 and unmarried
    penn_single_car_cond8 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for single car farm policies where the principal operator is 25-29 and unmarried
    penn_single_car_cond9 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 25) & (df['AGE'] <= 29)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for single car farm policies where the principal operator is 25-29 and unmarried
    penn_single_car_cond10 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 25) & (df['AGE'] <= 29)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for single car farm policies where the driver is 65 and over
    penn_single_car_cond11 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for single car non-farm policies where the driver is 65 and over
    penn_single_car_cond12 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for single car farm polices where the class code is still blank
    penn_single_car_cond13 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['CLASS_CODE'].isnull()) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for single car policies where the class code is still blank with a use code of pleasure
    penn_single_car_cond14 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['CLASS_CODE'].isnull()) & (df['STATE_NUMBER'] == penn))

    # This line of code looks for single car policies where the class code is still blank with a use code of business
    penn_single_car_cond15 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['CLASS_CODE'].isnull())) & (df['STATE_NUMBER'] == penn))

    
    # This line of code looks for multi car farm policies where the principal operator married and 20 or less
    penn_multi_car_cond1 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for multi car non-farm policies where the principal operator married and 20 or less
    penn_multi_car_cond2 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] == 'M')))

    # This line of code looks for multi car farm policies where the principal operator is 21-24
    penn_multi_car_cond3 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car non-farm policies where the principal operator is 21-24
    penn_multi_car_cond4 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)))

    # This line of code looks for multi car farm policies where the principal operator married and 20 or less
    penn_multi_car_cond5 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] != 'M')))

    # This line of code looks for multi car non-farm policies where the principal operator married and 20 or less
    penn_multi_car_cond6 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] <= 20) & (df['DRIVER_MARITAL_STATUS'] != 'M')))

    # This line of code looks for multi car farm policies where the principal operator is 21-24 and unmarried
    penn_multi_car_cond7 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for multi car non-farm policies where the principal operator is 21-24 and unmarried
    penn_multi_car_cond8 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 21) & (df['AGE'] <= 24)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for multi car farm policies where the principal operator is 25-29 and unmarried
    penn_multi_car_cond9 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 25) & (df['AGE'] <= 29)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for multi car farm policies where the principal operator is 25-29 and unmarried
    penn_multi_car_cond10 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P') & (df['STATE_NUMBER'] == penn)) & ((df['AGE'] >= 25) & (df['AGE'] <= 29)) & (df['DRIVER_MARITAL_STATUS'] != 'M'))

    # This line of code looks for multi car farm policies where the driver is 65 and over
    penn_multi_car_cond11 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for multi car non-farm policies where the driver is 65 and over
    penn_multi_car_cond12 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] != '3') & (df['AGE'] >= 65) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for multi car farm polices where the class code is still blank
    penn_multi_car_cond13 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['CLASS_CODE'].isnull()) & (df['STATE_NUMBER'] == penn)))

    # This line of code looks for multi car policies where the class code is still blank with a use code of pleasure
    penn_multi_car_cond14 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '1') | (df['USE_CODE'] == '4')) & (df['CLASS_CODE'].isnull()) & (df['STATE_NUMBER'] == penn))

    # This line of code looks for multi car policies where the class code is still blank with a use code of business
    penn_multi_car_cond15 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['CLASS_CODE'].isnull())) & (df['STATE_NUMBER'] == penn))
    
    penn_single_car_code = ['16710','16710','16730','16730','16800','16800','16820','16820','16840','16840','17000','17000','12130','12100','14000']
    penn_multi_car_code = ['16720','16720','16740','16740','16810','16810','16830','16830','16850','16850','17020','17020','12110','12120','14020']

    ny = '31'
    
    # This line of code looks for single car personal use polices where it's a non-male driver that is under 25
    ny_single_car_cond1 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(['1','4'])) & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for single car business use polices where it's a non-male driver that is under 25
    ny_single_car_cond2 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for single car farm use polices where it's a non-male driver that is under 25
    ny_single_car_cond3 = (((~df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for single car personal use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_single_car_cond4 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_single_car_cond5 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_single_car_cond6 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car personal use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_single_car_cond7 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_single_car_cond8 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_single_car_cond9 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car personal use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_single_car_cond10 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_single_car_cond11 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_single_car_cond12 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car personal use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_single_car_cond13 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_single_car_cond14 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_single_car_cond15 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car personal use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_single_car_cond16 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_single_car_cond17 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_single_car_cond18 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car personal use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_single_car_cond19 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car business use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_single_car_cond20 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for single car farm use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_single_car_cond21 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (~df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))
   
   
    # This line of code looks for multi car personal use polices where it's a non-male driver that is under 25
    ny_multi_car_cond1 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'].isin(['1','4'])) & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for multi car business use polices where it's a non-male driver that is under 25
    ny_multi_car_cond2 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '2') & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for multi car farm use polices where it's a non-male driver that is under 25
    ny_multi_car_cond3 = (((df['DISCOUNT_STRING'].str.contains('MC1', case=False)) & (df['USE_CODE'] == '3') & (df['STATE_NUMBER'] == ny)) & (((df['AGE'] >= 25) & (df['DRIVER_SEX'] == 'M')) | (df['DRIVER_SEX'] == 'F')))

    # This line of code looks for multi car personal use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_multi_car_cond4 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_multi_car_cond5 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where it's a male under 25 thats either married or is not the principal operator without a driver training code of DTR
    ny_multi_car_cond6 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car personal use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_multi_car_cond7 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_multi_car_cond8 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where it's a male under 25 thats either married or is not the principal operator with a driver training code of DTR
    ny_multi_car_cond9 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] == 'M') | (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car personal use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_multi_car_cond10 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_multi_car_cond11 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where its a male under 25 that's unmarred and not the prinicipal operator and without a driver training code of DTR
    ny_multi_car_cond12 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car personal use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_multi_car_cond13 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_multi_car_cond14 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where its a male under 25 that's unmarred and not the prinicipal operator and with a driver training code of DTR
    ny_multi_car_cond15 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] != 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car personal use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_multi_car_cond16 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_multi_car_cond17 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where its a male under 25 that's unmarred, the prinicipal operator, and without a driver training code of DTR
    ny_multi_car_cond18 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((~df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car personal use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_multi_car_cond19 = (((df['USE_CODE'].isin(['1','4'])) & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car business use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_multi_car_cond20 = (((df['USE_CODE'] == '2') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))

    # This line of code looks for multi car farm use policies where its a male under 25 that's unmarred, the prinicipal operator, and with a driver training code of DTR
    ny_multi_car_cond21 = (((df['USE_CODE'] == '3') & (df['DRIVER_SEX'] == 'M') & (df['STATE_NUMBER'] == ny)) & ((df['AGE'] < 25) & ((df['DRIVER_MARITAL_STATUS'] != 'M') & (df['PRINCIPAL_OCCASIONAL_INDICATOR'] == 'P')) & ((df['DISCOUNT_STRING'].str.contains('DTR',case=False)) & (df['DISCOUNT_STRING'].str.contains('MC1', case=False)))))
   
    ny_single_car_code = ['11110','13110','11510','12110','12110','12510','12170','12170','12570','12210','12210','12610','12270','12270','12670','12310','12310','12710','12370','12370','12770']
    ny_multi_car_code = ['11120','13120','11520','12120','12120','12520','12140','12140','12540','12220','12220','12620','12240','12240','12640','12320','12320','12720','12340','12340','12740']
    
    single_car_code = single_car_pol_code + florida_single_car_code + hawaii_single_car_code + mich_mont_single_car_code + nj_single_car_code + penn_single_car_code + ny_single_car_code
    multi_car_code = multi_car_pol_code + florida_multi_car_code + hawaii_multi_car_code + mich_mont_multi_car_code + nj_multi_car_code + penn_multi_car_code + ny_multi_car_code

    df['CLASS_CODE'] = np.select([single_car_pol_cond1,single_car_pol_cond2,single_car_pol_cond3,single_car_pol_cond4,single_car_pol_cond5,single_car_pol_cond6,single_car_pol_cond7,single_car_pol_cond8,florida_single_car_cond1,florida_single_car_cond2,florida_single_car_cond3,florida_single_car_cond4,florida_single_car_cond5,florida_single_car_cond6,florida_single_car_cond7,florida_single_car_cond8,florida_single_car_cond9,florida_single_car_cond10,florida_single_car_cond11,florida_single_car_cond12,florida_single_car_cond13,florida_single_car_cond14,florida_single_car_cond15,florida_single_car_cond16,hawaii_single_car_cond1,hawaii_single_car_cond2,hawaii_single_car_cond3,mich_mont_single_car_cond1,mich_mont_single_car_cond2,mich_mont_single_car_cond3,mich_mont_single_car_cond4,mich_mont_single_car_cond5,mich_mont_single_car_cond6,mich_mont_single_car_cond7,mich_mont_single_car_cond8,mich_mont_single_car_cond9,mich_mont_single_car_cond10,mich_mont_single_car_cond11,mich_mont_single_car_cond12,mich_mont_single_car_cond13,nj_single_car_cond1,nj_single_car_cond2,nj_single_car_cond3,nj_single_car_cond4,nj_single_car_cond5,nj_single_car_cond6,nj_single_car_cond7,nj_single_car_cond8,nj_single_car_cond9,nj_single_car_cond10,
    nj_single_car_cond11,nj_single_car_cond12,nj_single_car_cond13,nj_single_car_cond14,nj_single_car_cond15,nj_single_car_cond16,nj_single_car_cond17,nj_single_car_cond18,nj_single_car_cond19,nj_single_car_cond20,nj_single_car_cond21,nj_single_car_cond22,nj_single_car_cond23,nj_single_car_cond24,nj_single_car_cond25,nj_single_car_cond26,nj_single_car_cond27,nj_single_car_cond28,nj_single_car_cond29,nj_single_car_cond30,penn_single_car_cond1,penn_single_car_cond2,penn_single_car_cond3,penn_single_car_cond4,penn_single_car_cond5,penn_single_car_cond6,penn_single_car_cond7,penn_single_car_cond8,penn_single_car_cond9,penn_single_car_cond10,penn_single_car_cond11,penn_single_car_cond12,penn_single_car_cond13,penn_single_car_cond14,penn_single_car_cond15,ny_single_car_cond1,ny_single_car_cond2,ny_single_car_cond3,ny_single_car_cond4,ny_single_car_cond5,ny_single_car_cond6,ny_single_car_cond7,ny_single_car_cond8,ny_single_car_cond9,ny_single_car_cond10,ny_single_car_cond11,ny_single_car_cond12,ny_single_car_cond13,ny_single_car_cond14,ny_single_car_cond15,ny_single_car_cond16,ny_single_car_cond17,ny_single_car_cond18,ny_single_car_cond19,ny_single_car_cond20,ny_single_car_cond21,multi_car_pol_cond1,multi_car_pol_cond2,
    multi_car_pol_cond3,multi_car_pol_cond4,multi_car_pol_cond5,multi_car_pol_cond6,multi_car_pol_cond7,multi_car_pol_cond8,florida_multi_car_cond1,florida_multi_car_cond2,florida_multi_car_cond3,florida_multi_car_cond4,florida_multi_car_cond5,florida_multi_car_cond6,florida_multi_car_cond7,florida_multi_car_cond8,florida_multi_car_cond9,florida_multi_car_cond10,florida_multi_car_cond11,florida_multi_car_cond12,florida_multi_car_cond13,florida_multi_car_cond14,florida_multi_car_cond15,florida_multi_car_cond16,hawaii_multi_car_cond1,hawaii_multi_car_cond2,hawaii_multi_car_cond3,mich_mont_multi_car_cond1,mich_mont_multi_car_cond2,mich_mont_multi_car_cond3,mich_mont_multi_car_cond4,mich_mont_multi_car_cond5,mich_mont_multi_car_cond6,mich_mont_multi_car_cond7,mich_mont_multi_car_cond8,mich_mont_multi_car_cond9,mich_mont_multi_car_cond10,mich_mont_multi_car_cond11,mich_mont_multi_car_cond12,mich_mont_multi_car_cond13,nj_multi_car_cond1,nj_multi_car_cond2,nj_multi_car_cond3,nj_multi_car_cond4,nj_multi_car_cond5,nj_multi_car_cond6,nj_multi_car_cond7,nj_multi_car_cond8,nj_multi_car_cond9,nj_multi_car_cond10,nj_multi_car_cond11,nj_multi_car_cond12,nj_multi_car_cond13,nj_multi_car_cond14,nj_multi_car_cond15,nj_multi_car_cond16,
    nj_multi_car_cond17,nj_multi_car_cond18,nj_multi_car_cond19,nj_multi_car_cond20,nj_multi_car_cond21,nj_multi_car_cond22,nj_multi_car_cond23,nj_multi_car_cond24,nj_multi_car_cond25,nj_multi_car_cond26,nj_multi_car_cond27,nj_multi_car_cond28,nj_multi_car_cond29,nj_multi_car_cond30,penn_multi_car_cond1,penn_multi_car_cond2,penn_multi_car_cond3,penn_multi_car_cond4,penn_multi_car_cond5,penn_multi_car_cond6,penn_multi_car_cond7,penn_multi_car_cond8,penn_multi_car_cond9,penn_multi_car_cond10,penn_multi_car_cond11,penn_multi_car_cond12,penn_multi_car_cond13,penn_multi_car_cond14,penn_multi_car_cond15,ny_multi_car_cond1,ny_multi_car_cond2,ny_multi_car_cond3,ny_multi_car_cond4,ny_multi_car_cond5,ny_multi_car_cond6,ny_multi_car_cond7,ny_multi_car_cond8,ny_multi_car_cond9,ny_multi_car_cond10,ny_multi_car_cond11,ny_multi_car_cond12,ny_multi_car_cond13,ny_multi_car_cond14,ny_multi_car_cond15,ny_multi_car_cond16,ny_multi_car_cond17,ny_multi_car_cond18,ny_multi_car_cond19,ny_multi_car_cond20,ny_multi_car_cond21], (single_car_code + multi_car_code), df['CLASS_CODE'])


    return df