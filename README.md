# Retiming_Using_ML

Register manipulation algorithms which are in use today are heuristic based and they don’t provide the global optimum always. 
So in order to achieve something we may have to try different ways to get things done.

And if the circuit is large enough then finding thing and fine tuning all these by hand is not near to possible.

## Background : 

- Machine learning has been widely used in nearly all aspects in modern time
- Starting form drug design to friendship recommendation it has given tremendous results in all fields
- The domain of CAD for VLSI is no different, and has also potential to adapt the power of machine learning to generate fruitful results.
- Here we aim to generate a unsupervised model for the task

## Aim : 

- We aim to develop a model that can enable register motion and provide the optimum timing results every time
- We aim to test some potential models and compare the results to get the best model suitable for the task	

## Challenges : 

- The first one is how to represent the circuit so that it is easy to extract the features even when the circuit is large 
- Secondly what are the features that has to be chosen for training the model so that the accuracy is more
- What must be the output of the model so as to serve the purpose 
- How to verify whether the produced circuit follows the norms of retiming 
- How to process the input and the output, how to convert from netlist to Verilog 
- What must be the loss function for proper learning of the algorithm
- Finally the samples available in hand are too aren’t enough for the model to get trained
