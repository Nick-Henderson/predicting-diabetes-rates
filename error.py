def RMSE(y_test, yhat):
    return (((y_test - yhat)**2).sum()/len(y_test))**0.5