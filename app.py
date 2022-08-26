from flask import Flask, request, render_template
from numpy import random
import joblib
import os
import pandas as pd

import numpy as np

# Create Flask object to run
app = Flask(__name__,template_folder= 'templates' )

important_ingredients_acne = ['Benzoyl Peroxide', 'Betaine Salicylate', 'Salicylic Acid', 'Zinc Sulfate', 'Phytosphingosine', 'Potassium Azeloyl Diglycinate/Azelaic Acid', 'Zinc Gluconate', 'Zinc Pca']
important_ingredients_aging = ['Acetyl Hexapeptide-1', 'Ascorbic Acid (Vitamin C/Ascorbyl Glucoside/Magnesium Ascorbyl Phosphate/Tetrahexyldecyl Ascorbate/Ascorbyl Tetraisopalmitate)', 'Carnosine', 'Genistein', 'Ginkgo Biloba', 'Green Tea', 'Hexapeptide-10', 'Hydrolyzed Hyaluronic Acid','Mandelic Acid','Palmitoyl Pentapeptide-4','Palmitoyl Tripeptide-1','Resveratrol','Tocopheryl Acetate','Ubiquinone']
important_ingredients_brightning = ['Acetyl Glucosamine','Arbutin','Ascorbic Acid (Vitamin C/Ascorbyl Glucoside/Magnesium Ascorbyl Phosphate/Tetrahexyldecyl Ascorbate/Ascorbyl Tetraisopalmitate)','Glutathione','Kojic Acid','Lactic Acid','Phenylethyl Resorcinol','Resveratrol','Niacinamide','Tetrapeptide-30','Tranexamic Acid','Undecylenoyl Phenylalanine']




df_acne_akmal = pd.read_excel('Anti Acne Serum file Akmal.xlsx')
df_aging_akmal = pd.read_excel('Anti aging Serum file Akmal.xlsx')
df_brightning_akmal = pd.read_excel('Brightning Serum file Akmal.xlsx')
dir_list_acne = os.listdir('anti_acne_models')
dir_list_aging = os.listdir('anti_aging_models')
dir_list_brightning = os.listdir('brightning_models')
df_brightning_akmal['name'] = df_brightning_akmal['name'].str.replace(',','')
def givlis_df(dictionin):
    print(dictionin)
    df = pd.DataFrame(    columns = ['Male', 'Female',
                                     'White Race', 'Black Race',
                                     'Elder Age', 'Intermediate Age', 'Young Age',
                                     'Tropical', 'Dry', 'Temperate', 'Continental', 'Polar', 
                                     'Age_Elder Age', 'Age_Intermediate Age', 'Age_Young Age',
                                     'SkinType_Combination', 'SkinType_Dry', 'SkinType_Normal', 'SkinType_Oily',
                                     'SkinConcerns_Acne', 'SkinConcerns_Aging', 'SkinConcerns_Blackheads', 'SkinConcerns_Calluses', 'SkinConcerns_Cellulite', 'SkinConcerns_Cuticles', 'SkinConcerns_Dark circles', 'SkinConcerns_Dullness', 'SkinConcerns_Pores', 'SkinConcerns_Puffiness', 'SkinConcerns_Redness', 'SkinConcerns_Sensitivity', 'SkinConcerns_Stretch marks', 'SkinConcerns_Sun damage', 'SkinConcerns_Uneven skin tones',
                                     'SkinTyone_Dark', 'SkinTyone_Deep', 'SkinTyone_Ebony', 'SkinTyone_Fair', 'SkinTyone_Light', 'SkinTyone_Medium', 'SkinTyone_Olive', 'SkinTyone_Porcelain', 'SkinTyone_Tan'])

    if   (dictionin['Gender'] == 'Male') :

        df['Male'] = [1]
    if   (dictionin['Gender'] == 'Female') :
        df['Female'] = [1]
    if   (dictionin['Age'] == '13-17') or (dictionin['Age'] == '18-24')  or (dictionin['Age'] == '25-34'):
        df['Young Age'] = [1]
        
    
    if   (dictionin['Age'] == '35-44') or (dictionin['Age'] == '45-54')  :  
        df['Intermediate Age'] = [1]
        
    if   (dictionin['Age'] == '55-120') :
        df['Elder Age'] = [1]
        
        
    if   (dictionin['Race'] == 'White') :
        df['White Race'] = [1]
        
    if   (dictionin['Race'] == 'Black') :
        df['Black Race'] = [1]
        
    if   (dictionin['Climate'] == 'Tropical') :
        df['Tropical'] = [1]
        
    if   (dictionin['Climate'] == 'Dry') :
        df['Dry'] = [1]
        
    if   (dictionin['Climate'] == 'Temperate') :
        df['Temperate'] = [1]
        
    if   (dictionin['Climate'] ==  'Continental') :
        df['Continental'] = [1]
        
    if   (dictionin['Climate'] == 'Polar') :
        df['Polar'] = [1]
        
    df['SkinType'+'_'+dictionin['SkinType']] = [1]
    df['SkinTyone'+'_'+dictionin['SkinTyone']] = [1]
    df['SkinConcerns'+'_'+dictionin['SkinConcerns']] = [1]
    df = df.replace(np.NaN,0)
    print(df)
    return df
    
def sorrr(dc):
    dcx = sorted(dc.items(), key=lambda x:x[1],reverse = True)
    return dcx

    
def acne_imp(custtdetails):
    dic_acne_imp = {}
    for i in important_ingredients_acne:
        i = i.replace('/','_')
        if i[0] == ' ':
            i = i[1:]        
        
        for p in dir_list_acne:
            if i in p:
                i = p
                break          
        
        
        
        xgb = joblib.load(f'anti_acne_models/{i}')
        proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
        pred = xgb.predict(givlis_df(custtdetails))[0]
        #print(i,proba,pred,proba.index(max(proba)))

        dic_acne_imp[i] = proba[1] * 100


    #dic_acne_imp = sorted(dic_acne_imp.items(), key=lambda x:x[1],reverse = True)
    i = None
    
    dic_acne_supp = {}    
    for j  in (df_acne_akmal['name']):
        if j not in important_ingredients_acne:
            j = j.replace('/','_')
            if j[0] == ' ':
                j = j[1:]            
            
            for p in dir_list_acne:
                if j in p:
                    j = p
                    break              
            xgb = joblib.load(f'anti_acne_models/{j}')
            proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
            pred = xgb.predict(givlis_df(custtdetails))[0]
            #print(i,proba,pred,proba.index(max(proba)))

            dic_acne_supp[j] = proba[1]  * 100
        
    #dic_acne_supp = sorted(dic_acne_supp.items(), key=lambda x:x[1],reverse = True)
        
        
        
    
    z =  [sorrr(dic_acne_imp),'_______________________',sorrr(dic_acne_supp)]
    return z







def aging_imp(custtdetails):
    dic_aging_imp = {}
    for i in important_ingredients_aging:
        i = i.replace('/','_') 
        if i[0] == ' ':
            i = i[1:]

        
        for p in dir_list_aging:
            if i in p:
                i = p
                break        
        
        
        xgb = joblib.load(f'anti_aging_models/{i}')
        proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
        pred = xgb.predict(givlis_df(custtdetails))[0]
        #print(i,proba,pred,proba.index(max(proba)))  
        #print(i,proba,pred,proba.index(max(proba)))

        dic_aging_imp[i] = proba[1] * 100


    #dic_acne_imp = sorted(dic_acne_imp.items(), key=lambda x:x[1],reverse = True)
    i = None
    
    dic_aging_supp = {}    
    for j  in (df_aging_akmal['name']):
        if j not in important_ingredients_aging:
            j = j.replace('/','_')
            if j[0] == ' ':
                j = j[1:]            
            
            for p in dir_list_aging:
                if j in p:
                    j = p
                    break            
            
            
            xgb = joblib.load(f'anti_aging_models/{j}')
            proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
            pred = xgb.predict(givlis_df(custtdetails))[0]
            #print(i,proba,pred,proba.index(max(proba)))

            dic_aging_supp[j] = proba[1]  * 100
        
    #dic_acne_supp = sorted(dic_acne_supp.items(), key=lambda x:x[1],reverse = True)
        
        
        
    
    z =  [sorrr(dic_aging_imp),'_______________________',sorrr(dic_aging_supp)]


    return z





def brightning_imp(custtdetails):
    print(custtdetails)
    dic_brightning_imp = {}
    for i in important_ingredients_brightning:
        i = i.replace('/','_')
        print(i)
        if i[0] == ' ':
            i = i[1:]
        for p in dir_list_brightning:
            if i in p:
                print(p)
                i = p
                break
            
        xgb = joblib.load(f'brightning_models/{i}')
        proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
        pred = xgb.predict(givlis_df(custtdetails))[0]
        #print(i,proba,pred,proba.index(max(proba)))  
        #print(i,proba,pred,proba.index(max(proba)))

        dic_brightning_imp[i] = proba[1] * 100


    #dic_acne_imp = sorted(dic_acne_imp.items(), key=lambda x:x[1],reverse = True)
    i = None
    
    dic_brightning_supp = {}    
    for j  in (df_brightning_akmal['name']):
        if j not in important_ingredients_brightning:
            j = j.replace('/','_')
            print(j)            
            
            if j[0] == ' ':
                j = j[1:]           
            
            
            for p in dir_list_brightning:
                if j in p:
                    print(p)
                    j = p
                    break            
            xgb = joblib.load(f'brightning_models/{j}')
            
            proba = list(xgb.predict_proba(givlis_df(custtdetails))[0])
            pred = xgb.predict(givlis_df(custtdetails))[0]
            #print(i,proba,pred,proba.index(max(proba)))

            dic_brightning_supp[j] = proba[1]  * 100
        
    #dic_acne_supp = sorted(dic_acne_supp.items(), key=lambda x:x[1],reverse = True)
        
        
        
    
    z = [sorrr(dic_brightning_imp),'_______________________',sorrr(dic_brightning_supp)]

    return  z
 
 
 
 
 
 
 
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

   
    SkinConcerns = str(request.form.get('SkinConcerns'))

    Age = str(request.form.get('Age'))

    SkinType = str(request.form.get('SkinType'))

    Gender = str(request.form.get('Gender'))

    SkinTone = str(request.form.get('SkinTyone'))

    Race = str(request.form.get('Race'))
   
    Climate = str(request.form.get('Climate'))  


               

 
    out = {}
   
   

    if SkinConcerns == 'Acne':
        custdetails = {'SkinConcerns':SkinConcerns,'Age':Age,'SkinType':SkinType,'SkinTyone':SkinTone,'Gender':Gender,
                  'Race':Race,'Climate':Climate}
 
        out = acne_imp(custdetails)
    if SkinConcerns == 'Aging':
        custdetails = {'SkinConcerns':SkinConcerns,'Age':Age,'SkinType':SkinType,'SkinTyone':SkinTone,'Gender':Gender,
                  'Race':Race,'Climate':Climate}
 
        out = aging_imp(custdetails)          
    if (SkinConcerns != 'Acne') and (SkinConcerns != 'Aging'):
        custdetails = {'SkinConcerns':SkinConcerns,'Age':Age,'SkinType':SkinType,'SkinTyone':SkinTone,'Gender':Gender,
                  'Race':Race,'Climate':Climate}
 
        out = brightning_imp(custdetails)     
       
    print(out)

    return render_template('index.html', prediction_text= out)



   
   
if __name__ == "__main__":
    app.run()