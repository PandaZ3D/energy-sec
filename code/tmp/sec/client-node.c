#include "contiki.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"

#ifdef WITH_DTLS
#include "tinydtls.h"
#include "dtls.h"
#endif /* WITH_DTLS */

#include <stdio.h>
#include <string.h>

/* simulation configuraitions file */
#include "sim-config.h"

#define BUFFER_SIZE     32

static struct simple_udp_connection udp_conn;

#ifdef WITH_DTLS
//static dtls_handler_t cb;
//static dtls_context_t *dtls_context = NULL;

//static const coap_keystore_t *dtls_keystore = NULL;
//static struct uip_udp_conn *dtls_conn = NULL;
//static session_t *session = NULL;
#endif /* WITH_DTLS */

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&udp_client_process);
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer send_timer;
  static unsigned count;
  static char send_buffer[BUFFER_SIZE];
  static int send_len;
  uip_ipaddr_t dest_ipaddr;

  PROCESS_BEGIN();

  #ifdef WITH_DTLS
    printf("DTLS enabled\n");
    dtls_init();
  #endif /* WITH_DTLS */

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL,
                      UDP_SERVER_PORT, NULL);

  /* wait some some random time from within the SEND_INTERVAL */
  etimer_set(&send_timer, random_rand() % SEND_INTERVAL);
  //etimer_set(&send_timer, SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&send_timer));

    if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
      /* Send to DAG root (single server) */
      send_len = snprintf(send_buffer, sizeof(send_buffer), "HELLO %d", count);
      simple_udp_sendto(&udp_conn, send_buffer, send_len, &dest_ipaddr);
      count++;
      if(count == MAX_PKT_COUNT) {
        /* send the server a done message telling them you are done */
        send_len = snprintf(send_buffer, sizeof(send_buffer), "DONE %d", count);
        simple_udp_sendto(&udp_conn, send_buffer, send_len, &dest_ipaddr);  
        PROCESS_EXIT();
      }
    }
    /* reset the timer */
    //etimer_reset(&send_timer);
    //etimer_set(&send_timer, random_rand() % SEND_INTERVAL);
    etimer_set(&send_timer, SEND_INTERVAL
      - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));

  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
