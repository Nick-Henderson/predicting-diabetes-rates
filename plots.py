# short function to plot residuals and histogram of results
def residual_plot(yhat,y_test,ax):
    ax.scatter(yhat,y_test-yhat)
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Residuals')
def hists(yhat, y_test, ax):
    ax.hist(yhat,label='Predicted',alpha=0.5,range=[0.05,0.16],bins=20)
    ax.hist(y_test,label='Actual',alpha=0.5,range=[0.05,0.16],bins=20)
    ax.set_xlabel('Diagnosed Diabetes Rate')
    ax.set_ylabel('Number of Counties')
    ax.legend()

