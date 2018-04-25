#include <iostream>
#include <fastcdr/Cdr.h>
#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/publisher/PublisherListener.h>
#include <fastrtps/subscriber/SubscriberListener.h>
#include <fastrtps/subscriber/SampleInfo.h>

using namespace std;
using namespace eprosima::fastcdr;
extern "C" int foo(int val,char* data_buffer,size_t len)
{
	FastBuffer cdrbuffer(data_buffer, len);
	Cdr cdr_des(cdrbuffer);
	cout << "Hello World" << endl;
	return 0;
}