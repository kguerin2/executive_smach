#!/usr/bin/env python
import roslib; roslib.load_manifest('smach_ros')
import rospy
import smach
import smach_ros
from smach import State
from smach_ros import TransitionPublisher

# define state Foo
class Foo(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=['to_bar','to_finish'])
    self.counter = 0

  def execute(self, userdata):
    rospy.loginfo('Publisher Machine: Executing state FOO_P')
    if self.counter < 3:
      self.counter += 1
      rospy.sleep(2)
      return 'to_bar'
    else:
      rospy.sleep(2)
      return 'to_finish'

# define state Bar
class Bar(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=['to_foo'])

  def execute(self, userdata):
    rospy.loginfo('Publisher Machine: Executing state BAR_P')
    rospy.sleep(2)
    return 'to_foo'


# define state Finish
class Finish(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=['finished'])

  def execute(self, userdata):
    rospy.loginfo('Publisher Machine: Executing state FINISH_P')
    rospy.sleep(2)
    return 'finished'
        
def main():
  rospy.init_node('smach_publisher_state_machine')

  # Create a SMACH state machine
  sm = smach.StateMachine(outcomes=['done'])

  # Open the container
  with sm:
    # Add states to the container
    smach.StateMachine.add('FOO_P', Foo(), 
                           transitions={'to_bar':'BAR_P', 'to_finish':'FINISH_P'})
    smach.StateMachine.add('BAR_P', Bar(), 
                           transitions={'to_foo':'FOO_P'})
    smach.StateMachine.add('FINISH_P', Finish(), 
                           transitions={'finished':'done'})
  
  tp = TransitionPublisher("smach_publisher_state_machine",sm)
  tp.start()

  # Execute SMACH plan
  outcome = sm.execute()

  # Wait for ctrl-c to stop the application
  rospy.spin()
  tp.stop()

if __name__ == '__main__':
    main()