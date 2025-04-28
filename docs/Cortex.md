# Cortex
Updated: Apr 28 2025

### Overview


**behavior.compute_heading** 
A custom computeHeading node which reads object detection data, as well as image and camera metadata, and computes heading and distance. It reads and writes everything from a global blackboard, which is populated by other BT nodes. 


**controller.computeHeadingTest** 
Tests the computeHeading node in a full BT, with other nodes that read metadata, subscribe to topics, and request services. 


### How to contribute

**Prerequisite** be familiar with the behavior_tree package

**cortex.behavior** contains custom BT behaviors. The convention is for these to subclass BehaviorTree.Action. Each custom behavior needs a name and an action, which is defined in it's scope. The action function should return True if everything executes correctly .


**cortex.controller** contains constructed behavior trees. The current convention is to construct the behavior tree in a rclpy.node subclass. To call the evaluate method of the root, the node can be spun with a timer callback or the evaluate() function called directly


### Build instructions

Everything depends on the **behavior_tree** package. Make sure this is built and sourced in your terminal

Custom behavior trees in **cortex.controller** may request services and subscribe to topics created by other packages, such as chimera_camera. To build the controllers, make sure the respective **custom_interfaces** package is built and sourced. To run the controllers, make sure the respective services and publishers are running. 

