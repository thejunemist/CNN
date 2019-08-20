from torch.nn import Conv3d

_hidden_size = 100
batch_size = 100
_max_sequence = 100
_linear_size =100

class ConvNet(torch.nn):
​
    def __init__(self, _input_size, _output_size, _hidden_size, _batch_size, _max_sequence, _linear_size):
        # hyperparams and layers
        super(CharConv, self).__init__()
        self.hidden_size = _hidden_size
        self.batch_size = _batch_size
        self.max_sequence = _max_sequence
        self.linear_size = _linear_size
        # Layer 1
        self.conv1 = torch.nn.Conv3d(_input_size, self.hidden_size, kernel_size=(3,3,3), stride=1, padding=(1,1,1))
        self.conv1_bn = torch.nn.BatchNorm3d(self.hidden_size)
        self.relu1 = nn.ReLU()
        self.pool1 = torch.nn.MaxPool3d(kernel_size=(3,3,3), stride=(1,2,2))
        # Layer 2
        self.conv2 = torch.nn.Conv3d(self.hidden_size, self.hidden_size, kernel_size=(,,), stride=1, padding=(1,1,1))
        self.conv2_bn = torch.nn.BatchNorm3d(self.hidden_size)
        self.relu2 = nn.ReLU()
        self.pool2 = torch.nn.MaxPool3d(kernel_size=(,,), stride=(2,2,2))
        # Layer 3
        self.conv3 = torch.nn.Conv3d(self.hidden_size, self.hidden_size, kernel_size=(,,), stride=1, padding=(1,1,1))
        self.conv3_bn = torch.nn.BatchNorm3d(self.hidden_size)
        # Layer 4
        self.conv4 = torch.nn.Conv3d(self.hidden_size, self.hidden_size, kernel_size=(,,), stride=1, padding=(1,1,1))
        self.conv4_bn = torch.nn.BatchNorm3d(self.hidden_size)
        # Layer 5
        self.conv5 = torch.nn.Conv3d(self.hidden_size, self.hidden_size, kernel_size=(,,), stride=1, padding=(1,1,1))
        self.conv5_bn = torch.nn.BatchNorm3d(self.hidden_size)
        # Layer 6
        self.conv6 = torch.nn.Conv3d(self.hidden_size, self.hidden_size, kernel_size=(,,), stride=1, padding=(1,1,1))
        self.conv6_bn = torch.nn.BatchNorm3d(self.hidden_size)
        self.relu3 = nn.ReLU()
        self.pool3 = torch.nn.MaxPool3d(kernel_size=(,,), stride=(2,2,2))
        # Fully Connected Outputs
        input_hidden_size = (self.max_sequence - 96) // 27 * self.hidden_size
        self.fc1 = torch.nn.Linear(input_hidden_size, self.linear_size)
        self.fc1_bn = torch.nn.BatchNorm3d(self.linear_size)
        self.drop1 = nn.Dropout(0.5)
        self.fc2 = torch.nn.Linear(self.linear_size, self.linear_size)
        self.fc2_bn = torch.nn.BatchNorm3d(self.linear_size)
        self.softmax = nn.LogSoftmax(dim=1)
​
    def forward(self, _input):
        # arch
        layer1 = self.conv1(_input)
        layer1 = self.conv1_bn(layer1)
        layer1 = self.pool1(layer1)
        layer1 = self.relu1(layer1)
        layer2 = self.conv2(layer1)
        layer2 = self.conv2_bn(layer2)
        layer2 = self.pool2(layer2)
        layer2 = self.relu2(layer2)
        cout_1 = self.conv3(layer2)
        cout_1 = self.conv3_bn(cout_1)
        cout_2 = self.conv4(cout_1)
        cout_2 = self.conv4_bn(cout_2)
        cout_3 = self.conv5(cout_2)
        cout_3 = self.conv5_bn(cout_3)
        cout_4 = self.conv6(cout_3)
        cout_4 = self.conv6_bn(cout_4)
        pout_1 = self.pool3(cout_4)
        rout_1 = self.relu3(pout_1)
        fc_out = rout_1.view(rout_1.size(0), -1)
        full_1 = self.fc1(fc_out)
        full_1_bn = self.fc1_bn(full_1)
        drop_1 = self.drop1(full_1_bn)
        full_2 = self.fc2(drop_1)
        full_2_bn = self.fc2_bn(full_2)
        out_soft = self.softmax(full_2_bn)
        return out_soft