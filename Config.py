#data
trainfile = './data/train.txt'
validfile = './data/valid.txt'
testfile = './data/test.txt'
restfile = './data/rest.txt'


tmpfile = './tmp/test.txt'

#path
rnnpath = './bin-rnnlm'
scorepath = './tmp'

#model
rnnmodel = './model/rnnmodel.txt'

#run parameters
hidden_size = 50
class_size = 370
bptt_steps = 5
lambda_value = 0.8

# data partition
train_portion = 0.2
valid_portion = 0.05
test_portion = 0.05
rest_portion = 0.7


