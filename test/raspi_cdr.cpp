#include <iostream>
#include <fastcdr/Cdr.h>
#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/publisher/PublisherListener.h>
#include <fastrtps/subscriber/SubscriberListener.h>
#include <fastrtps/subscriber/SampleInfo.h>

class raspi
{
	public:
		raspi();
		void deserialize(char data_buffer[], size_t len);
		void serialize(char data_buffer[], size_t len);
		float get_m_value();
		uint16_t get_length();
		void set_m_value(float val);
	private:
		float m_value;

		uint16_t length;
};

raspi::raspi()
{	
	length = 0;
	m_value = 0;
}

void raspi::deserialize(char data_buffer[], size_t len)
{
	eprosima::fastcdr::FastBuffer cdrbuffer(data_buffer, len);
	eprosima::fastcdr::Cdr cdr_des(cdrbuffer);
	cdr_des >> m_value;
}

void raspi::serialize(char data_buffer[], size_t len)
{	
	eprosima::fastcdr::FastBuffer cdrbuffer(data_buffer, len);
	eprosima::fastcdr::Cdr scdr(cdrbuffer);
	scdr << m_value;
	length = scdr.getSerializedDataLength();
}

float raspi::get_m_value()
{
	return m_value;
}

uint16_t raspi::get_length()
{
	return length;
}

void raspi::set_m_value(float val)
{
	m_value = val;
}

extern "C"
{
	raspi* raspi_new(){return new raspi();}
	void raspi_deserialize(raspi* raspi_t,char data_buffer[],size_t len){raspi_t->deserialize(data_buffer,len);}
	void raspi_serialize(raspi* raspi_t,char data_buffer[],size_t len){raspi_t->serialize(data_buffer,len);}

	float get_m_value(raspi* raspi_t){return raspi_t->get_m_value();}
	uint16_t get_length(raspi* raspi_t){return raspi_t->get_length();}
	void set_m_value(raspi* raspi_t,float val){raspi_t->set_m_value(val);}
}