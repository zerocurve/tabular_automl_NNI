# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import nni
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import logging
import numpy as np
import pandas as pd
import json
from fe_util import *
from model import *

LOG = logging.getLogger('sklearn_classification')


# def unit_test_fe():
#     file_name = 'train.tiny.csv'
#     target_name = 'Label'
#     id_index = 'Id'
    
#     # list is a column_name generate from tuner
#     df = pd.read_csv(file_name)

#     import json
#     with open('search_space.json', 'r') as file:	
#         data= json.load(file)

#     from autofe_tuner import AutoFETuner
#     tuner = AutoFETuner()
#     tuner.update_search_space(data)
#     config = tuner.generate_parameters(1)
#     print("generate params\n", config)
    
#     sample_col = config['sample_feature']
    
#     # raw feaure + sample_feature
#     df = name2feature(df, sample_col, target_name)
#     feature_imp, val_score = lgb_model_train(df,  _epoch = 1000, target_name = target_name, id_index = id_index)

#     value = {
#         "default":val_score, 
#         "feature_importance":feature_imp
#     }
    
#     tuner.receive_trial_result(0, config, value)
#     config = tuner.generate_parameters(2)
#     print("generate params\n", config)


if __name__ == '__main__':

    file_name = 'train.tiny.csv'
    target_name = 'Label'
    id_index = 'Id'

    # get parameters from tuner
    RECEIVED_PARAMS = nni.get_next_parameter()
    LOG.info("Received params:\n", RECEIVED_PARAMS)
    
    # list is a column_name generate from tuner
    df = pd.read_csv(file_name)
    sample_col = RECEIVED_PARAMS['sample_feature']
    
    # raw feaure + sample_feature
    df = name2feature(df, sample_col, target_name)
    feature_imp, val_score = lgb_model_train(df,  _epoch = 1000, target_name = target_name, id_index = id_index)
    nni.report_final_result({
        "default":val_score, 
        "feature_importance":feature_imp
    })
