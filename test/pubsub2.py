"""
One listener is subscribed to a topic called 'rootTopic'.
One 'rootTopic' message gets sent. 
"""

from pubsub import pub
import time

# ------------ create a listener ------------------

def listener1(arg1, arg2=None):
    print('Function listener1 received:')
    print('  arg1 =', arg1)
    print('  arg2 =', arg2)


# ------------ register listener ------------------

pub.subscribe(listener1, 'rootTopic')

# ---------------- send a message ------------------

print('Publish something via pubsub')
anObj = dict(a=456, b='abc')
while True:
	time.sleep(0.1)
	pass
#pub.sendMessage('rootTopic', arg1=123, arg2=anObj)