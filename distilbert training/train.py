import ktrain
import csv
from ktrain import text as txt
import re

x_train = []
x_test = []
y_train = []
y_test = []
with open('clue_types.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        x_test.append(row[0])
        y_test.append(row[1])

with open('clue_types_extra_test.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        x_test.append(row[0])
        y_test.append(row[1])

with open('clue_types_extra_test_na.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        x_test.append(row[0])
        y_test.append(row[1])

with open('clue_types_extra_train.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        x_train.append(row[0])
        y_train.append(row[1])

trn, val, preproc = txt.texts_from_array(x_train=x_train, y_train=y_train,
                                          x_test=x_test, y_test=y_test,
                                          class_names=['0', '1', '2', '3', '4'],
                                          preprocess_mode='distilbert',
                                          maxlen=30)

model = txt.text_classifier('distilbert', train_data=trn, preproc=preproc)
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=6)

learner.fit_onecycle(3e-5, 5)

"""
predictor = ktrain.get_predictor(learner.model, preproc)
predictor.save('category')
"""
