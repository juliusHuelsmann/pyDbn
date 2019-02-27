

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

These 7 lines of code create the following two outputs:



