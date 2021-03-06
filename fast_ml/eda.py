import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display
from fast_ml.utilities import printmd , normality_diagnostic , plot_categories , \
plot_categories_with_target , calculate_mean_target_per_category , plot_target_with_categories

class eda:
    """
    Does the EDA for numerical variable
    
    Optional Arguments:
    target: define the target variable
    model : regression / classification 
    """
    def __init__ (self, df, target = None, model = None):
        self.__df__ = df
        self.__target__ = target
        self.__model__ = model
        self.__length_df__= len(df)
    
    def eda_numerical_variable(self, variable):
        '''
        Parameter:
            variable: pass the variable for which EDA is required
            
        provides basic statistcs, missing values, distribution, spread statistics, 
        Q-Q plot, Box plot, outliers using IQR, various variable transformations'''
        c = variable
        s = self.__df__[variable]

        
        # 1. Basic Statistics

        print ('Total Number of observations : ', len(s))
        print ()

        print ('Datatype :', (s.dtype))
        print ()

        printmd ('**<u>5 Point Summary :</u>**')

        print ('  Minimum  :\t\t', s.min(), '\n  25th Percentile :\t', s.quantile(0.25), 
               '\n  Median :\t\t', s.median(), '\n  75th Percentile :\t', s.quantile(0.75), 
               '\n  Maximum  :\t\t', s.max())

        print ()

        # 2. Missing values

        printmd ('**<u>Missing Values :</u>**')

        print ('  Number :', s.isnull().sum())
        print ('  Percentage :', s.isnull().mean()*100, '%')

        # 3. Histogram
        
        printmd ('**<u>Variable distribution and Spread statistics :</u>**')

        sns.distplot(s.dropna(), hist = True, fit = norm, kde = True)
        plt.show()

        # 4. Spread Statistics

        print ('Skewness :' , s.skew())
        print ('Kurtosis :', s.kurt())
        print ()

        # 5. Q-Q plot
        printmd ('**<u>Normality Check :</u>**')
        res = stats.probplot(s.dropna(), dist = 'norm', plot = plt)
        plt.show()

        # 6. Box plot to check the spread outliers
        print ()
        printmd ('**<u>Box Plot and Visual check for Outlier  :</u>**')
        sns.boxplot(s.dropna(), orient = 'v')
        plt.show()

        # 7. Get outliers. Here distance could be a user defined parameter which defaults to 1.5

        print ()
        printmd ('**<u>Outliers (using IQR):</u>**')

        IQR = np.quantile(s, .75) - np.quantile(s, .25)
        upper_boundary = np.quantile(s, .75) + 1.5 * IQR
        lower_boundary = np.quantile(s, .25) - 1.5 * IQR

        print ('  Right end outliers :', np.sum(s>upper_boundary))
        print ('  Left end outliers :', np.sum(s < lower_boundary))

        # 8. Various Variable Transformations

        print ()
        printmd (f'**<u>Explore various transformations for {c}</u>**')
        print ()

        print ('1. Logarithmic Transformation')
        s_log = np.log(s)
        normality_diagnostic(s_log)

        print ('2. Exponential Transformation')
        s_exp = np.exp(s)
        normality_diagnostic(s_exp)

        print ('3. Square Transformation')
        s_sqr = np.square(s)
        normality_diagnostic(s_sqr)

        print ('4. Square-root Transformation')
        s_sqrt = np.sqrt(s)
        normality_diagnostic(s_sqrt)

        print ('5. Box-Cox Transformation')
        s_boxcox, lambda_param = stats.boxcox(s)
        normality_diagnostic(s_boxcox)
        print ('Optimal Lambda for Box-Cox transformation is :', lambda_param )
        print ()

        print ('6. Yeo Johnson Transformation')
        s = s.astype('float')
        s_yeojohnson, lambda_param = stats.yeojohnson(s)
        normality_diagnostic(s_yeojohnson)
        print ('Optimal Lambda for Yeo Johnson transformation is :', lambda_param )
        print ()

        
        
    #### -------- Categorical Variables ------- #####
    
    def eda_categorical_variable(self, variable, add_missing=False, add_rare=False, tol=0.05):
        """
        """
        c = variable
        df = self.__df__
        s = self.__df__[variable]
        target = self.__target__
        model = self.__model__
        
        # 1. Basic Statistics
        printmd ('**<u>Basic Info :</u>**')
        print ('Total Number of observations : ', len(s))
        print ()
        
        # 2. Cardinality
        printmd ('**<u>Cardinality of the variable :</u>**')
        print ('Number of Distinct Categories (Cardinality): ', len(s.unique()))
        print ('Distinct Values : ', s.unique())
        print ()
        
        
        # 3. Missing Values

        printmd ('**<u>Missing Values :</u>**')
        
        nmiss = s.isnull().sum()
        print ('  Number :', s.isnull().sum())
        print ('  Percentage :', s.isnull().mean()*100, '%')

        # 4. Plot Categories
        
        printmd ('**<u>Category Plots :</u>**')
        plot_categories(df, c)

        # 5. Plot Categories by including Missing Values
        
        if nmiss:
            printmd ('**<u>Category plot by including Missing Values**')
            plot_categories(df, c, add_missing = True)
            
        # 6. Plot categories by combining Rare label
        
        printmd ('**<u>Category plot by including missing (if any) and Rare labels**')
        print (f'Categories less than {tol} value are clubbed in Rare label')
        plot_categories(df, c, add_missing = True, add_rare = True)
        
        #7. Plot categories with target
        
        if target:
            printmd ('**<u>Category Plot and Mean Target value:</u>**')
            plot_categories_with_target(df, c, target)
               

       #8. Plot distribution of target variable for each categories
    
        if target:
            printmd ('**<u>Distribution of Target variable for all categories:</u>**')
            plot_target_with_categories(df, c, target)
               
    
        
    