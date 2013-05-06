#!/usr/bin/env python
import roslib; roslib.load_manifest('smach_ros')
import rospy
import smach
import smach_ros
from threading import Thread
from smach_msgs.msg import SmachStateMachineStatus as Status

__all__ = ['TransitionListener', 'TransitionPublisher', 'TransitionListenerState']

class TransitionListener:
  def transition_cb(self,msg):
    self.active_states_ = msg.active_states
    self.active_transitions_ = msg.active_transitions
    self.active_outcomes_ = msg.active_outcomes
    pass

  def __init__(self,name):
    self.name_ = name
    self.active_states_ = ''
    self.active_transitions_ = ''
    self.active_outcomes_ = ''
    self.subscriber_ = rospy.Subscriber(self.name_+"/transistions",Status,self.transition_cb)

  def get_active_states(self):
    return self.active_states_

  def get_active_transitions(self):
    return self.active_transitions_
    
  def get_active_outcomes(self):
    return self.active_outcomes_

#####
class TransitionListenerState(smach.State):
  def __init__(self,transition_listener,outcomes):
    smach.State.__init__(self, outcomes)
    self.transition_listener_ = transition_listener


#####
class TransitionPublisher:
  def __init__(self,name,state_machine):
    self.name_ = name
    self.run_ = False
    self.publishing_thread_ = Thread(name=self.name_+':transition_publisher',target=self.publish_loop)
    self.publisher_ = rospy.Publisher(self.name_+"/transistions",Status)
    self.state_machine_ = state_machine
  
  def start(self):
    self.run_ = True
    self.publishing_thread_.start()

  def stop(self):
    self.run_ = False

  def publish_loop(self):
    while not rospy.is_shutdown() and self.run_ == True:

      msg = Status()
      msg.header.stamp = rospy.Time.now()
      msg.active_states = str(self.state_machine_.get_active_states())
      msg.active_transitions = str(self.state_machine_.get_current_transitions())
      msg.active_outcomes = str(self.state_machine_.get_current_outcome())

      self.publisher_.publish(msg)
      rospy.sleep(0.1)
      pass