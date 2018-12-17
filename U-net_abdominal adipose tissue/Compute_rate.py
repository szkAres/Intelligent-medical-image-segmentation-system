import os
import numpy as np

VAT_rate= np.ndarray((404), dtype=np.float32)
SAT_rate= np.ndarray((404), dtype=np.float32)

Path = os.path.dirname(os.path.realpath(__file__))
Results0 = np.load(Path + '\\Labels_Train.npy')     #专家标记数据
Results1 = np.load(Path + '\\Predict.npy')          #预测标记数据

#计算准确率
for i in range(404):
    VAT_right= 0
    VAT_all = 0
    SAT_right = 0
    SAT_all = 0
    for m in range(512):
        for n in range(512):
            if (Results0[i][m][n][1]): #VAT内脏脂肪组织
                VAT_all = VAT_all + 1
                if(Results1[i][m][n] == 1):
                    VAT_right = VAT_right + 1
            if (Results0[i][m][n][2]): #SAT皮下脂肪组织
                SAT_all = SAT_all + 1
                if(Results1[i][m][n] == 2):
                    SAT_right = SAT_right + 1
    VAT_rate[i] = VAT_right / VAT_all
    SAT_rate[i] = SAT_right / SAT_all
    print(i, "SAT_rate:", VAT_rate[i])
    print("VAT_rate:",VAT_rate[i],"\n")

print("Average SAT_Rate = ",np.mean(SAT_rate))
print("Average VAT_Rate = ",np.mean(VAT_rate),"\n")




