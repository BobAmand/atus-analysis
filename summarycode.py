import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

'''
%matplotlib inline

GRAPHIC:
all_summary = pd.read_csv('data/atussum_2014.dat')
gender_sum = all_summary[['tucaseid','TEAGE', 'TESEX']]
gender_sum = gender_sum.rename(columns={'tucaseid':'CASE_ID',
                              'TEAGE': 'AGE',       # age in years
                              'TESEX': 'GENDER'     # gender; Male = 1, Female = 2
                                     }
                            )

m_age = gender_sum[gender_sum.GENDER == 1]          # Male = 1; list of ages
f_age = gender_sum[gender_sum.GENDER == 2]          # Female = 2; distribtuion of ages

'''
'''
GRAPHIC:
gender_sum['AGE'].plot(kind='hist')
plt.title("All Respondents by Age: {} count".format(gender_sum['CASE_ID'].count()))
plt.ylabel("Frequency")
plt.xlabel("Age in Years")
'''
'''
m_age['AGE'].plot(kind='hist', color='b', alpha=0.5, ylim=(0,900))
plt.title("Male Respondents by Age: {} count".format(m_age['AGE'].count()))
plt.ylabel("Frequency")
'''
'''
f_age['AGE'].plot(kind='hist', color='g', alpha=0.5)
plt.title("Female Respondents by Age: {} count".format(f_age['AGE'].count()))
plt.ylabel("Frequency")
'''
'''
x = list(m_age['AGE'])      # true list of male ages
y = list(f_age['AGE'])      # true list of female ages
xm = m_age['AGE'].mean()    # mean of male ages
yf = f_age['AGE'].mean()    # mean of female ages

plt.hist(x, bins=10, alpha=0.5, label='male')
plt.axvline(xm, color='b', linestyle='dashed', linewidth=2)
plt.hist(y, bins=10, alpha=0.5, label='female')
plt.axvline(yf, color='r', linestyle='dashed', linewidth=2)
plt.legend()
plt.title("Age Distribution by Gender")
plt.xlabel('Age in Years\n Males: N: {}, Mean Age(BLUE): {}, Stdev: {}\n Females: N: {}, Mean Age(RED): {}, Stdev: {}'
           .format(np.count_nonzero(x),
                   np.mean(x),
                   np.std(x),
                   np.count_nonzero(y),
                   np.mean(y),
                   np.std(y)
                  )
          )
plt.ylabel('Frequency')
plt.show()
'''
'''
pd.pivot_table(gender_sum, index=['GENDER'], values=['AGE'], aggfunc=[np.amin,
                                                                      np.amax,
                                                                      np.count_nonzero,
                                                                      np.average,
                                                                      np.std])

'''
'''
home_school = all_summary[['tucaseid','TRERNWA','PEEDUCA','TRCHILDNUM','t030203',]]
home_school = home_school.rename(columns={'tucaseid': 'CASE_ID',
                                          'PEEDUCA': 'MAX_ED',                # need categories
                                          'TRERNWA': 'WEEKLY_EARN',           # implied 2 digit weekly $
                                          'TRCHILDNUM': 'CHILDREN',           # number of children under 18 yrs.
                                          't030203': 'HOME_SCHOOLED',         # household children are homeschooled
                                          }
                                 )
home_school = home_school[home_school.CHILDREN != 0]            # removes those without children
home_school = home_school[home_school.WEEKLY_EARN != -1]        # removes those without recorded income
'''
'''
home_school.corr()
'''
'''
plt.hist(list(home_school['MAX_ED']),bins=(10))
'''
'''
plt.hist(list(home_school['WEEKLY_EARN']),bins=(10))
'''
'''
plt.hist(list(home_school['CHILDREN']),bins=(10))
'''
'''
xhs = list(home_school['MAX_ED'])
yhs = list(home_school['WEEKLY_EARN'])
cf = home_school['MAX_ED'].corr(home_school['WEEKLY_EARN'])

plt.scatter(x=xhs, y=yhs)
plt.title("CorrElatiion Coefficient: {}".format(cf))
plt.xlabel("Maximum Education: \n <39 = Less than HS, 39 = HS, 40-42 = Some College, 43 = BS/BA, >43 = Graduate Work")
plt.ylabel("Weekly Earning; Implied 2 digit value")
'''
'''
all_summary[all_summary['t030203'] == 360]
'''
'''
ver = all_summary[all_summary['t030203'] >= 1]
'''
'''
plt.hist(list(ver['t030203']))
'''
'''
pd.pivot_table(home_school,index=['HOME_SCHOOLED'])    #Not sure why this breaks on 0, 60, 120, and 150!
'''
'''
home_school['HOME_SCHOOLED']=home_school['HOME_SCHOOLED'].astype('category')
home_school['HOME_SCHOOLED'].cat.set_categories([0,1], inplace=True)
'''
'''
pd.pivot_table(home_school,index=['HOME_SCHOOLED'])      #There are only zeros in the home_school dataframe.
'''
'''
metro_set = all_summary[['tucaseid','TRERNWA','PEEDUCA','TRCHILDNUM','GTMETSTA',]]
metro_set = metro_set.rename(columns={'tucaseid': 'CASE_ID',
                                      'PEEDUCA': 'MAX_ED',         # <HS,HS,some COLL, BS, Grad
                                      'TRERNWA': 'WEEKLY_EARN',    # implied 2 digit weekly $
                                      'TRCHILDNUM': 'CHILDREN',    # number of children under 18 yrs.
                                      'GTMETSTA': 'METRO',         # 1 = METRO, 2 = NONMETRO
                                     }
                            )
metro_set = metro_set[metro_set.WEEKLY_EARN != -1]        # removes those without recorded income
metro_set = metro_set[metro_set.METRO != -1]              # removes 'blanks'
metro_set = metro_set[metro_set.METRO != -2]              # removes 'don't know'
metro_set = metro_set[metro_set.METRO != -3]              # removes 'refused'
metro_set = metro_set[metro_set.METRO != 3]               # removes 'Not Identified'
'''
'''
xmet = list(metro_set['METRO'])
ymet = list(metro_set['WEEKLY_EARN'])

plt.scatter(x=xmet, y=ymet)
plt.title("Metro living vs Weekly earning:\n {} corr. coef.".format(metro_set['METRO'].corr(metro_set['WEEKLY_EARN'])))
plt.xlabel("1 = Metro    2 = Non-Metro")
plt.ylabel("Weekly Earnings with implied 2 digits")
plt.show()
'''
'''
mset1 = metro_set[metro_set['METRO'] == 1]  #DataFrame with Metro = 1
mset2 = metro_set[metro_set['METRO'] == 2]  #DataFrame with Metro = 2

x = list(mset1['WEEKLY_EARN'])   #list of weekly earnings by Metro = 1
y = list(mset2['WEEKLY_EARN'])   #list of weekly earnings by Metro = 2

plt.hist(x, bins=20, alpha=0.5, color='b', label='METRO')
plt.hist(y, bins=20, alpha=0.5, color='r', label='NON-MET')
plt.title("Weekly Earnings distributed by Location")
plt.legend(loc='upper right')
plt.xlabel("Weekly Earning (2 digit implied)")
plt.ylabel("Frequency")
plt.show()
'''
'''
mset1 = metro_set[metro_set['METRO'] == 1]  #DataFrame with Metro = 1
mset2 = metro_set[metro_set['METRO'] == 2]  #DataFrame with Metro = 2

x = list(mset1['MAX_ED'])   #list of weekly earnings by Metro = 1
y = list(mset2['MAX_ED'])   #list of weekly earnings by Metro = 2

xm = mset1['MAX_ED'].mean()    # mean of education by Metro = 1
yf = mset2['MAX_ED'].mean()    # mean of education by Metro = 2


plt.hist(x, bins=20, alpha=0.5, color='b', label='METRO')
plt.axvline(xm, color='b', linestyle='dashed', linewidth=2)
plt.hist(y, bins=20, alpha=0.5, color='r', label='NON-MET')
plt.axvline(yf, color='r', linestyle='dashed', linewidth=2)
plt.title("Maximum Education distributed by Location")
plt.legend(loc='upper left')
plt.xlabel('Maximum Education\n Metro: N: {}, Mean(BLUE): {}, Stdev: {}\n Non-Metro: N: {}, Mean(RED): {}, Stdev: {}'
           .format(np.count_nonzero(x),
                   np.mean(x),
                   np.std(x),
                   np.count_nonzero(y),
                   np.mean(y),
                   np.std(y)
                  )
          )
plt.ylabel("Frequency")
plt.show()
'''
'''
mset1 = metro_set[metro_set['METRO'] == 1]  #DataFrame with Metro = 1
mset2 = metro_set[metro_set['METRO'] == 2]  #DataFrame with Metro = 2

x = list(mset1['CHILDREN'])   #list of children by Metro = 1
y = list(mset2['CHILDREN'])   #list of children by Metro = 2

plt.hist(x, bins=20, alpha=0.5, color='b', label='METRO')
plt.hist(y, bins=20, alpha=0.5, color='r', label='NON-MET')
plt.title("Number of Children (<18) distributed by Location")
plt.legend(loc='upper right')
plt.xlabel("Number of Children")
plt.ylabel("Frequency")
plt.show()
'''
