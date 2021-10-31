# -*- coding: utf-8 -*-
import sys, os
sys.path.append("..")
import pandas as pd
from model.regression import PolynomialRegression, XgboostRegression, RegressionWorkflowBase

class ModelSelection(object):

    def __init__(self, model):
        self.model = model
        self.reg_workflow = RegressionWorkflowBase()

    def activate(self, data, degree=2):
        X = data.loc[:, 'SIO2(WT%)':'AL2O3(WT%)']
        y = data.loc[:, 'FEOT(WT%)']

        X_train, X_test, y_train, y_test = self.reg_workflow.data_split(X, y)

        # model option
        if self.model == "Polynomial Regression":
            self.reg_workflow = PolynomialRegression()
            X_train, X_test = self.reg_workflow.poly(X_train, X_test)
        elif self.model == "Xgboost":
            self.reg_workflow = XgboostRegression()
            #print(type(self.reg_workflow))

        # common components for every algorithms
        self.reg_workflow.fit(X_train, y_train)
        y_test_prediction = self.reg_workflow.predict(X_test)
        self.reg_workflow.score(y_test, y_test_prediction)
        self.reg_workflow.cross_validation(X_train, y_train, cv_num=10)

        # special components of different algorithms
        # self.reg_workflow.special_components()
