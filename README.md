

Wrapper around daft for easily creating DBN.


### Install
```bash
pip install daft --user
```


### Usage
see examples

#### Example: Creating a Model
This example creates a HMM with two explicitely visualized parameters pi and Sigma:
```python
dbn = DBN()
dbn.attach(NodeProperties("X", 0, 0, parentsPrevious="X"))
dbn.attach(NodeProperties(name="Y",x=0, y=1,parentsNow="X", nodeType=NodeType.Observed, continuous=True))
dbn.attach(NodeProperties(name="\Sigma",x=0, y=2,parentsNow="Y", nodeType=NodeType.Variable))
dbn.attach(NodeProperties(name="\pi",x=0, y=2,parentsPrevious="Y", nodeType=NodeType.Variable))
```

#### Example: Exporting a Model
Depending on whether the first few time slices are to be visualized (1) or the time slices around 
the current time, the plot can be exported via
```python
k.export(sliceBefore=0, sliceAfter=3, centerSuffix="") #< variant 1:  export first few time slices
```
or (2):
```python
k.export(sliceBefore=2, sliceAfter=1, centerSuffix="\\tau") #< variant 2: export 2 before - 1
                                                            #  after the current time (referred
                                                            #  to as \tau)
```

These 7 lines of code create the following two vector graphics:

![hmm1](https://user-images.githubusercontent.com/9212314/53511004-9ab18300-3abf-11e9-862c-bbf7ae55cebc.jpg) 
[hmm1.pdf](https://github.com/juliusHuelsmann/pyDbn/files/2911551/hmm1.pdf)
and 
![hmm](https://user-images.githubusercontent.com/9212314/53511005-9ab18300-3abf-11e9-913d-54b7c297bf4f.jpg)
[hmm.pdf](https://github.com/juliusHuelsmann/pyDbn/files/2911552/hmm.pdf)
