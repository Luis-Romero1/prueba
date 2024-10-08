from Classifier import logger
from Classifier.utils.common import fit_ml_models
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, davies_bouldin_score, silhouette_score, calinski_harabasz_score
from sklearn.pipeline import Pipeline
import pickle
import joblib  
import os
import io
import boto3


class pass_train:
    def __init__(self,config,df):
        self.param = config["params"]
        self.conf = config["training"]
        self.df=df
        os.makedirs(self.conf["root_dir"], exist_ok=True)
     
    
    def prepare_data(self):
        logger.info(f"Starting training")

        self.parameter_lr = self.param['parameter_lr']
        self.penal,self.size= self.parameter_lr["penalty"],self.parameter_lr["size"]
        self.parameter_lr.pop("penalty")
        self.parameter_lr.pop("size")


        #self.df = self.df.drop("Id", axis=1)
        x = self.df.drop(["species"], axis=1)
        y = self.df["species"]

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=self.size, random_state=42)



        # pipeline = Pipeline([
        # ("scaling", StandardScaler())
        #  ])
        # x_train= pipeline.fit_transform(x_train)
        # x_test= pipeline.fit_transform(x_test)
        

    def run_train(self):
        model_lr = LogisticRegression(penalty=self.penal, random_state=42)

        acc_score_train, acc_score_test, best_score , best_params= fit_ml_models(model_lr, self.parameter_lr, "Logistic Regression",
                                                                             self.x_train,self.y_train,self.x_test,self.y_test)
    
        model_lr = LogisticRegression(solver=best_params["algo__solver"], C=best_params["algo__C"],penalty=self.penal, random_state=42)
        model_lr.fit(self.x_train, self.y_train)

        

        if os.getenv("ENV")=="developer":
            pathf=self.conf["trained_model_path"]
            joblib.dump(model_lr,pathf)
        else:
            
            ###############################################
            # model_dir = os.environ.get('SM_MODEL_DIR', '/opt/ml/model')

            # # Guardar el modelo en la ruta especificada
            # model_path = os.path.join(model_dir, 'model.joblib')
            # joblib.dump(model_lr, model_path)

            ################################################
            # clf = joblib.load(os.path.join(os.environ.get("SM_MODEL_DIR"), "model.joblib"))
            # model_path = os.path.join(clf, "model.joblib")
            # joblib.dump(model,model_path)

            path_s3 = 'iris-sagemaker/model_train/model.joblib'

            access_point="arn:aws:s3:us-east-1:211125717993:accesspoint/iris-in180392"#os.getenv("ACESS_POINT")   

            model_buffer = io.BytesIO()
            joblib.dump(model_lr, model_buffer)
            model_buffer.seek(0)  
            s3 = boto3.client('s3')

            s3.upload_fileobj(model_buffer, access_point, path_s3,ExtraArgs={'ACL': 'bucket-owner-full-control'})

            
        


