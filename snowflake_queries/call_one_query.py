query = """
    WITH temp1 (policy_number,company_code,state_number,risk_code,product_name,line_coverage_code,limit_code,vin,USE_CODE,DRIVER_SEX,driver_marital_status,AGE,
    principal_occasional_indicator,sr22_file_indicator,coverage,coverage_description, DISCOUNT_STRING) as (
    SELECT
      fg.policy_number,
      fg.company_code,
      fg.state_number,
      fg.risk_code,
      fg.product_name,
      fg.line_coverage_code,
      fg.limit_code,
      fg.vin,
      CASE
        WHEN fg.use_code in ('5','7') THEN '1'
        WHEN fg.use_code in ('6','8','9','10') THEN '2'
        ELSE fg.use_code
      END as USE_CODE,
      CASE
        WHEN fg.driver_sex LIKE ' ' THEN 'F' 
        WHEN fg.driver_sex LIKE '' THEN 'F'
        WHEN fg.driver_sex LIKE 'x' THEN 'F'
        ELSE fg.driver_sex
      END as DRIVER_SEX,
      CASE
        WHEN fg.driver_marital_status LIKE ' ' THEN 'M'
        WHEN fg.driver_marital_status LIKE '' THEN 'M'
        ELSE fg.driver_marital_status
      END AS DRIVER_MARITAL_STATUS,
      datediff(year, try_to_date(fg.driver_birthdate), current_date) AS AGE,
      CASE
        WHEN fg.principal_occasional_indicator LIKE ' ' THEN 'P'
        WHEN fg.principal_occasional_indicator LIKE '' THEN 'P'
        ELSE fg.principal_occasional_indicator
      END AS PRINCIPAL_OCCASIONAL_INDICATOR,
      fg.sr22_file_indicator,
      cc.coverage,
      cc.coverage_description,
      CONCAT(COALESCE(fg.discount1,''),COALESCE(fg.discount2,''),COALESCE(fg.discount3,''),COALESCE(fg.discount4,''),COALESCE(fg.discount5,''),COALESCE(fg.discount6,''),COALESCE(fg.discount7,''),COALESCE(fg.discount8,''),COALESCE(fg.discount9,''),COALESCE(fg.discount10,''),
      COALESCE(fg.discount11,''),COALESCE(fg.discount12,''),COALESCE(fg.discount13,''),COALESCE(fg.discount14,''),COALESCE(fg.discount15,''),COALESCE(fg.discount16,''),COALESCE(fg.discount17,''),COALESCE(fg.discount18,''),COALESCE(fg.discount19,''),COALESCE(fg.discount20,'')) as DISCOUNT_STRING
    FROM
      premiums.user_managed.finalmerge_gold fg
    JOIN
      premiums.published.conv_coverage cc on
      fg.state_number = cc.state_code and
      fg.line_coverage_code = cc.line_coverage_code and
      fg.limit_code = cc.limit_code
    ),
    temp2 (policy_number,company_code,state_number,risk_code,product_name,line_coverage_code,limit_code,vin,USE_CODE,DRIVER_SEX,driver_marital_status,AGE,
    principal_occasional_indicator,sr22_file_indicator,coverage,coverage_description, DISCOUNT_STRING) as (
    SELECT
      policy_number,
      company_code,
      state_number,
      risk_code,
      product_name,
      line_coverage_code,
      limit_code,
      vin,
      CASE
        WHEN use_code LIKE ' ' THEN '1'
        WHEN use_code LIKE '' THEN '1'
        ELSE use_code
      END AS USE_CODE,
      COALESCE(DRIVER_SEX, 'F') AS DRIVER_SEX,
      COALESCE(driver_marital_status,'M') AS DRIVER_MARITAL_STATUS,
      COALESCE(AGE, '25') AS AGE,
      COALESCE(principal_occasional_indicator, 'P') AS PRINCIPAL_OCCASIONAL_INDICATOR,
      sr22_file_indicator,
      coverage,
      coverage_description,
      DISCOUNT_STRING
    FROM
      temp1
    ),
    temp3 (policy_number,company_code,state_number,risk_code,product_name,line_coverage_code,limit_code,vin,USE_CODE,DRIVER_SEX,driver_marital_status,AGE,
    principal_occasional_indicator,sr22_file_indicator,coverage,coverage_description, DISCOUNT_STRING) as (
    SELECT
      trim(policy_number) as policy_number,
      trim(company_code) company_code,
      trim(state_number) as state_number,
      trim(risk_code) as risk_code,
      trim(product_name)as product_name,
      trim(line_coverage_code) as line_coverage_code,
      trim(limit_code) as limit_code,
      trim(vin) as vin,
      COALESCE(trim(USE_CODE), '1') AS USE_CODE,
      trim(DRIVER_SEX) as DRIVER_SEX,
      trim(DRIVER_MARITAL_STATUS) as DRIVER_MARITAL_STATUS,
      CAST(trim(AGE) AS INTEGER) AS AGE,
      trim(principal_occasional_indicator) as principal_occasional_indicator,
      trim(sr22_file_indicator) as sr22_file_indicator,
      trim(coverage) as coverage,
      trim(coverage_description) as coverage_description,
      trim(DISCOUNT_STRING) as DISCOUNT_STRING
    FROM
      temp2
    )
    SELECT TOP 1001
      *
    FROM
      temp3
    WHERE
      risk_code = 'AA'
    """

query2 = """
WITH initial_pull (policy_event_transaction_id,policy_number,effective_date,policy_effective_date,company_code,state_number,rate_manual_code,product,line_coverage,limit_code,premium_amount,coverage,coverage_description,age,driver_marital_status,driver_sex,principal_occasional_indicator,sr22_file_indicator,vin,use_code,garaging_zip_code,garaging_zip_code_ext,model_year,exposure_count) as (
SELECT
  p.policy_event_transaction_id,
  p.policy_number,
  p.effective_date,
  p.policy_effective_date,
  p.company_code,
  p.state_number,
  p.rate_manual_code,
  cc.product,
  -- The substring columns are used to seperate the line coverage and the limit code. This is done to make the conditional logic and python more straight forward.
  substring(pc.line_coverage_limit_code,1,4) as line_coverage,
  substring(pc.line_coverage_limit_code,5,6) as limit_code,
  -- This will sum the premium amounts for each policy so that every single row doesn't comeback from the policy table
  sum(pc.premium_amount) as premium_amount,
  cc.coverage,
  cc.coverage_description,
  -- This will return the driver's age. When it comes back as null, it is defaulted to 25
  coalesce(datediff(year, try_to_date(d.birthdate), current_date), '25') as age,
  -- This will return the martial status of the driver. When it comes back as null, it is defaulted to M
  coalesce(nullif(trim(d.marital_status), ''), 'M') as driver_marital_status,
  -- This will return the driver's sex. When it comes back as null, it is defaulted to F
  coalesce(nullif(trim(d.sex), ''), 'F') as driver_sex,
  -- This will return whether or not the driver is the principal operator. When it comes back as null, it is defaulted to P
  coalesce(nullif(trim(d.principal_occasional_indicator), ''), 'P') as principal_occasional_indicator,
  d.sr22_file_indicator,
  v.vin,
  -- The use code is transformed based on the qualifications of call 1
  CASE
    WHEN v.use_code in ('5','7') THEN '1'
    WHEN v.use_code in ('6','8','9','10') THEN '2'
    -- The trim function will not get rid of the excess spaces in the use code column. (will need to do further investigation of table)
    WHEN v.use_code LIKE '' THEN '1'
    WHEN v.use_code LIKE ' ' THEN '1'
    WHEN v.use_code IS NULL THEN '1'
    ELSE v.use_code
  END AS use_code,
  v.garaging_zip_code,
  v.garaging_zip_code_ext,
  v.model_year,
  pc.exposure_count
FROM
  premiums.published.policy p
JOIN
  premiums.published.policy_coverage pc on
  p.policy_event_transaction_id = pc.policy_event_transaction_id
LEFT JOIN
  premiums.published.conv_coverage cc on
  p.state_number = cc.state_code and
  substring(pc.line_coverage_limit_code,1,4) = cc.line_coverage_code and
  substring(pc.line_coverage_limit_code,5,6) = cc.limit_code
JOIN
  premiums.published.driver d on
  p.policy_event_transaction_id = d.policy_event_transaction_id
JOIN
  premiums.published.vehicle v on
  p.policy_event_transaction_id = v.policy_event_transaction_id
WHERE
  initcap(cc.product) = 'Auto' and
  p.policy_effective_date between '2022-01-15' and '2022-12-15'
GROUP BY
  1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24
  ), driver_discount_string (policy_event_transaction_id, discount_string) as (
SELECT
  p.policy_event_transaction_id,
  /*CASE 
    WHEN (LISTAGG(DISTINCT pd.discount_code) LIKE '%DDF%') OR (LISTAGG(DISTINCT pd.discount_code) LIKE '%DTR%') OR (LISTAGG(DISTINCT pd.discount_code) LIKE '%MC1%')
    THEN LISTAGG(DISTINCT pd.discount_code)
    ELSE NULL 
  END AS discount_string*/
  listagg(trim(pd.discount_code))
FROM
  premiums.published.policy p
JOIN
  premiums.published.policy_discount pd on
  p.policy_event_transaction_id = pd.policy_event_transaction_id
group  by
  p.policy_event_transaction_id
  )
SELECT TOP 1000
  ip.policy_number,
  ip.effective_date,
  ip.policy_effective_date,
  ip.company_code,
  ip.state_number,
  ip.rate_manual_code,
  ip.product,
  ip.line_coverage,
  ip.limit_code,
  sum(ip.premium_amount) as premium_amount,
  ip.coverage,
  ip.coverage_description,
  ip.age,
  ip.driver_marital_status,
  ip.driver_sex,
  ip.principal_occasional_indicator,
  ip.sr22_file_indicator,
  ip.vin,
  ip.use_code,
  ip.garaging_zip_code,
  ip.garaging_zip_code_ext,
  ip.model_year,
  ip.exposure_count,
  case when d.discount_string = '000' then null else d.discount_string end as discount_string
FROM
  initial_pull ip
LEFT JOIN
  driver_discount_string d on
  ip.policy_event_transaction_id = d.policy_event_transaction_id
GROUP BY
  1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24
"""