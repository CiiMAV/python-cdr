#include <iostream>
#include <fastcdr/Cdr.h>
#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/publisher/PublisherListener.h>
#include <fastrtps/subscriber/SubscriberListener.h>
#include <fastrtps/subscriber/SampleInfo.h>

class sensor_baro
{
	public:
		sensor_baro();
		void deserialize(char data_buffer[], size_t len);
		uint64_t get_m_error_count();
		float get_m_pressure();
		float get_m_altitude();
		float get_m_temperature();
		uint32_t get_m_device_id();
	private:
		uint64_t m_error_count;
		float m_pressure;
		float m_altitude;
		float m_temperature;
		uint32_t m_device_id;
};

sensor_baro::sensor_baro()
{

}

void sensor_baro::deserialize(char data_buffer[], size_t len)
{
	eprosima::fastcdr::FastBuffer cdrbuffer(data_buffer, len);
	eprosima::fastcdr::Cdr cdr_des(cdrbuffer);
	cdr_des >> m_error_count;
	cdr_des >> m_pressure;
	cdr_des >> m_altitude;
	cdr_des >> m_temperature;
	cdr_des >> m_device_id;

	//test
	cdr_des << (float)123.0;
}

uint64_t sensor_baro::get_m_error_count()
{
	return m_error_count;
}

float sensor_baro::get_m_pressure()
{
	return m_pressure;
}

float sensor_baro::get_m_altitude()
{
	return m_altitude;
}

float sensor_baro::get_m_temperature()
{
	return m_temperature;
}

uint32_t sensor_baro::get_m_device_id()
{
	return m_device_id;
}

extern "C"
{
	sensor_baro* sensor_baro_new(){return new sensor_baro();}
	void sensor_baro_deserialize(sensor_baro* sensor_baro_t,char data_buffer[],size_t len){sensor_baro_t->deserialize(data_buffer,len);}

	uint64_t get_error_count(sensor_baro* sensor_baro_t){return sensor_baro_t->get_m_error_count();}
	float get_pressure(sensor_baro* sensor_baro_t){return sensor_baro_t->get_m_pressure();}
	float get_altitude(sensor_baro* sensor_baro_t){return sensor_baro_t->get_m_altitude();}
	float get_temperature(sensor_baro* sensor_baro_t){return sensor_baro_t->get_m_temperature();}
	uint32_t get_device_id(sensor_baro* sensor_baro_t){return sensor_baro_t->get_m_device_id();}
}