#!/usr/bin/env python
import roslib; roslib.load_manifest('smach_ros')
import rospy
import smach
import smach_ros
from smach_ros import TransitionListener
from smach_ros import TransitionListenerState

class Foo(TransitionListenerState):
  def __init__(self,trans_listener):
    TransitionListenerState.__init__(self,trans_listener, outcomes=['to_bar','finish'])
    self.counter = 0

  def execute(self, userdata):
    rospy.loginfo('Subscriber Machine: Executing state FOO_S')
    if 'FINISH_P' in self.transition_listener_.get_active_states():
      if 'to_finish' in self.transition_listener_.get_active_outcomes(): 
        return 'finish'
      else:
        rospy.sleep(.5)
        return 'to_bar'
    else:
      rospy.sleep(.5)
      return 'to_bar'

class Bar(TransitionListenerState):
  def __init__(self,trans_listener):
    TransitionListenerState.__init__(self,trans_listener, outcomes=['to_foo'])

  def execute(self, userdata):
    rospy.loginfo('Subscriber Machine: Executing state BAR_S')
    rospy.sleep(.5)
    return 'to_foo'
        
def main():
  rospy.init_node('smach_listener_state_machine')

  # Create a SMACH state machine
  sm = smach.StateMachine(outcomes=['finished'])

  trans_listener = TransitionListener("smach_publisher_state_machine")

  # Open the container
  with sm:
    # Add states to the container
    smach.StateMachine.add('FOO_S', Foo(trans_listener), 
                           transitions={'to_bar':'BAR_S', 'finish':'finished'})
    smach.StateMachine.add('BAR_S', Bar(trans_listener), 
                           transitions={'to_foo':'FOO_S'})
  
  # Execute SMACH plan
  outcome = sm.execute()

  # Wait for ctrl-c to stop the application
  rospy.spin()
  sis.stop()

if __name__ == '__main__':
    main()