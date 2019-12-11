/* a simulation configuration file */
#ifndef SIM_CONF_H_
#define SIM_CONF_H_

#define MAX_PKT_COUNT   100
#define UDP_CLIENT_PORT	8765
#define UDP_SERVER_PORT	5678

/* send interval of the client process */
#define SEND_INTERVAL 	(60 * CLOCK_SECOND) // every minute

#endif /* SIM_CONF_H_ */
