import pandas as pd
import glob
import datetime

data_paths = glob.glob('./temp/crawling_data_*.csv')
print(data_paths)

df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp])
df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/concat_review_test_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%h%M')), index=False)
