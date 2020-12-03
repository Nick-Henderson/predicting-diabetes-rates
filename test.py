from sklearn.preprocessing import StandardScaler
from error import RMSE
import numpy as np
import pandas as pd
# function takes a model, a kfolds object, an X dataframe, and a y array

def test_model(model,kf,X, y,prnt=True):
    #empty lists for error scores, yhats from each fold, and y_tests from each fold
    error_scores = []
    yhats = []
    y_tests = []
    
    # looping through the different splits
    for train_index, test_index in kf.split(X):
        # getting train and test sets
        X_train, X_test = X.values[train_index], X.values[test_index]
        y_train, y_test = y[train_index],y[test_index]
        
        # scaling X
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        
        # fitting the model and predicting y-values
        model.fit(X_train,y_train)
        yhat = model.predict(X_test)

        # using our RMSE function to test the model
        error_scores.append(RMSE(yhat,y_test))
        
        # appending yhat and y_test to lists for use outside the function
        yhats.append(yhat)
        y_tests.append(y_test)
        
    # print error score and return yhats and y_tests (for residual plots, etc.)
    if prnt:
        print(f'Average RMSE: {np.mean(error_scores)}')
    return error_scores, yhats, y_tests
    
def add_features(X,y,kf,model,initial_features=[]):
    feature_list = initial_features
    best_feature = 0
    best_score = 1
    for feature in range(25):
        if feature not in feature_list:
            X_sub = X.iloc[:,feature_list+[feature]]
            errors, yhats, y_tests = test_model(model, kf,X_sub, y,prnt=False)
            score = np.mean(errors)
            if score < best_score:
                best_score = score
                best_feature = feature
    feature_list.append(best_feature)
    return feature_list, best_score
    