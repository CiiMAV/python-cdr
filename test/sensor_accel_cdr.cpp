#include <iostream>
#include <fastcdr/Cdr.h>
#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/publisher/PublisherListener.h>
#include <fastrtps/subscriber/SubscriberListener.h>
#include <fastrtps/subscriber/SampleInfo.h>

class sensor_accel
{
	public:
		sensor_accel();
		void deserialize(char data_buffer[], size_t len);
		uint64_t get_m_integral_dt();
    	uint64_t get_m_error_count();
    	float get_m_x();
    	float get_m_y();
    	float get_m_z();
    	float get_m_x_integral();
    	float get_m_y_integral();
    	float get_m_z_integral();
    	float get_m_temperature();
    	float get_m_range_m_s2();
    	float get_m_scaling();
    	uint32_t get_m_device_id();
    	int16_t get_m_x_raw();
    	int16_t get_m_y_raw();
    	int16_t get_m_z_raw();
    	int16_t get_m_temperature_raw();
	private:
    	uint64_t m_integral_dt;
    	uint64_t m_error_count;
    	float m_x;
    	float m_y;
    	float m_z;
    	float m_x_integral;
    	float m_y_integral;
    	float m_z_integral;
    	float m_temperature;
    	float m_range_m_s2;
    	float m_scaling;
    	uint32_t m_device_id;
    	int16_t m_x_raw;
    	int16_t m_y_raw;
    	int16_t m_z_raw;
    	int16_t m_temperature_raw;
};

sensor_accel::sensor_accel()
{
	m_integral_dt = 0;
    m_error_count = 0;
    m_x = 0;
    m_y = 0;
    m_z = 0;
    m_x_integral = 0;
    m_y_integral = 0;
    m_z_integral = 0;
    m_temperature = 0;
    m_range_m_s2 = 0;
    m_scaling = 0;
    m_device_id = 0;
    m_x_raw = 0;
    m_y_raw = 0;
    m_z_raw = 0;
    m_temperature_raw = 0;
}

void sensor_accel::deserialize(char data_buffer[], size_t len)
{
	eprosima::fastcdr::FastBuffer cdrbuffer(data_buffer, len);
	eprosima::fastcdr::Cdr cdr_des(cdrbuffer);
	
	cdr_des >> m_integral_dt;
    cdr_des >> m_error_count;
    cdr_des >> m_x;
    cdr_des >> m_y;
    cdr_des >> m_z;
    cdr_des >> m_x_integral;
    cdr_des >> m_y_integral;
    cdr_des >> m_z_integral;
    cdr_des >> m_temperature;
    cdr_des >> m_range_m_s2;
    cdr_des >> m_scaling;
    cdr_des >> m_device_id;
    cdr_des >> m_x_raw;
    cdr_des >> m_y_raw;
    cdr_des >> m_z_raw;
    cdr_des >> m_temperature_raw;
}

uint64_t sensor_accel::get_m_integral_dt()
{
	return m_integral_dt;
}
uint64_t sensor_accel::get_m_error_count()
{
	return m_error_count;
}
float sensor_accel::get_m_x()
{
	return m_x;
}
float sensor_accel::get_m_y()
{
	return m_y;
}
float sensor_accel::get_m_z()
{
	return m_z;
}
float sensor_accel::get_m_x_integral()
{
	return m_x_integral;
}
float sensor_accel::get_m_y_integral()
{
	return m_y_integral;
}
float sensor_accel::get_m_z_integral()
{
	return m_z_integral;
}
float sensor_accel::get_m_temperature()
{	
	return m_temperature;
}
float sensor_accel::get_m_range_m_s2()
{
	return m_range_m_s2;
}
float sensor_accel::get_m_scaling()
{
	return m_scaling;
}
uint32_t sensor_accel::get_m_device_id()
{
	return m_device_id;
}
int16_t sensor_accel::get_m_x_raw()
{
	return m_x_raw;
}
int16_t sensor_accel::get_m_y_raw()
{
	return m_y_raw;
}
int16_t sensor_accel::get_m_z_raw()
{
	return m_z_raw;
}
int16_t sensor_accel::get_m_temperature_raw()
{
	return m_temperature_raw;
}

extern "C"
{
	sensor_accel* sensor_accel_new(){return new sensor_accel();}
	void sensor_accel_deserialize(sensor_accel* sensor_accel_t,char data_buffer[],size_t len){sensor_accel_t->deserialize(data_buffer,len);}

	uint64_t get_integral_dt(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_integral_dt();}
   	uint64_t get_error_count(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_error_count();}
   	float get_x(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_x();}
   	float get_y(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_y();}
   	float get_z(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_z();}
   	float get_x_integral(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_x_integral();}
   	float get_y_integral(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_y_integral();}
   	float get_z_integral(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_z_integral();}
   	float get_temperature(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_temperature();}
   	float get_range_m_s2(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_range_m_s2();}
   	float get_scaling(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_scaling();}
   	uint32_t get_device_id(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_device_id();}
   	int16_t get_x_raw(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_x_raw();}
   	int16_t get_y_raw(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_y_raw();}
   	int16_t get_z_raw(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_z_raw();}
   	int16_t get_temperature_raw(sensor_accel* sensor_accel_t){return sensor_accel_t->get_m_temperature_raw();}
}