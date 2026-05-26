import numpy as np
import pandas as pd
import random
import time
from openai import OpenAI
import mistune
from bs4 import BeautifulSoup
API_KEY =
client = OpenAI(api_key=f"{API_KEY}", base_url="https://api.deepseek.com")
def get_sentiment_level(comment):
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                    "role": "system",
                    "content": "#### 定位 \n - 智能助手名称 ：用户反馈建筑室内环境情感程度的分类专家\n- 主要任务 ：对输入的反馈情感进行自动分类，识别其所属的类别。\n #### 能力\n- 文本分析 ：能够准确分析反馈文本的情感登记\n- 分类识别 ：根据分析结果，将评论文本分类到预定义的种类中。\n\n#### 知识储备\n-评论种类 ：\n  - 正面的情感，返回整数1 \n  - 中性情感，请返回0 \n -负面的情感，返回整数-1   \n\n\n\n#### 使用说明\n- 输入 ：一段用户评论文本。\n- 输出 ：只输出用户评论文本所属的种类，不需要额外解释。\n"
            },
            {
                    "role": "user",
                    "content": f"{comment}"
            }
        ]
    )
    return completion.choices[0].message.content
def sentiment_level(path,file_name):
    df=pd.read_csv(path+file_name)
    df['Sent_lvl']=999
    sent_level=998
    for i in df.index:
        comment=df.loc[i,'Content']
        sent_level=get_sentiment_level(comment)
        #time.sleep(30)
        try:
            if len(sent_level)>=2:
                sent_level=sent_level[:2]
            elif len(sent_level)<=1:
                sent_level=sent_level[:1]
        except:
            print('sentiment_level error')
        df.loc[i,'Sent_lvl']=sent_level
        print(f'正在分析第{i}个，总共有{len(df)}个句子',sent_level)
        if (i + 1) % 300 == 0:
            df.to_csv(path+file_name+str(i)+'临时存储'+'sentiment_level.csv')
    df.to_csv(path+file_name+'sentiment_level.csv')
if __name__=='__main__':
    path='.\\Temp\\'
    file_name='2.9578env_prb_DeepSeek_envprlb183487summer1768543260.7401085Cleaned办公室温度2122232425_clean.csv.csv'
    sentiment_level(path,file_name)
