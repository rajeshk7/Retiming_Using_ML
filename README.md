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

### Why proper representation is important ? 

Here the circuit has to be represented properly so that we can extract all the essential features required
Without proper representation training of the model will be incomplete which will result in inaccurate prediction

Moreover, in representation learning, without having a proper representation of the circuit our model will oversimplify the problem (underfitting)

## Circuit representation :

The central problem in machine learning on graphs is finding a way to incorporate information about the structure of the graph into the machine learning model
Here we aim to represent our circuit using a method called DeepWalk method with a little modification
DeepWalk relies on direct encoding and use a decoder based on the inner product. 

### What are the features used for training and what is the expected the output ?

- Chain : A chain is a walk in a graph which starts form an input node and ends at a output node. 
  - I1, I1.2, I1.3, I1.5 is a chain 
- Input :
  - Top k chains of the circuit, here we can follow an approach where we can start with small k and keep on increasing it
  - Frequency
- Output : 
  - Final location of registers with coordinates 
  
### How do we verify the generated circuit ?

- A machine learning algorithm can have infinite ways to move the registers and can produce millions of circuits 
- Verifying each of them isn’t a good idea to begin with 
- In order to not take any invalid move, we try to teach the algorithm rules based on which it can move the registers
- Such machine learning algorithms are known as **rule based machine learning algorithm**

## Loss Funnctions :

- We will have two loss functions 
  - First one will be proportional to the latency achieved after the predicted motion of the registers. If the latency      increases we’ll incur high loss
  - Second one is how far a register is being moved, we want to achieve the optimum complexity with minimum dynamicity of the circuit  

