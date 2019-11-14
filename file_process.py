import os
import pandas as pd

if __name__ == '__main__':
    save_path = r''
    files = os.listdir(save_path)
    info_dict = {
        'link':[],
        'title':[],
        'Time_Stamp':[]
    }
    for file in files:
        file_path = os.path.join(save_path,file)
        with open(file_path,'r',encoding='utf-8') as f:
            # TODO:should debug to check whether the time_stamp is read
            link = f.readline()
            time_stamp = f.readline()
            info_dict['title'].append(file.split('.')[0])
            info_dict['link'].append(link)
            info_dict['Time_Stamp'].append(time_stamp)
    df = pd.DataFrame(info_dict)
    df.to_excel(r'f:\SP_dang\info_TNYT.xlsx',index=False)