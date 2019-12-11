/*
 * Copyright (c) 2006, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

/**
 * \file
 *         A very simple Contiki application showing how Contiki programs look
 * \author
 *         Adam Dunkels <adam@sics.se>
 */

#include "contiki.h"
#include "sys/energest.h"
#include "sys/ctimer.h"

#include <stdio.h> /* For printf() */
/*---------------------------------------------------------------------------*/
PROCESS(energy_sec_process, "Energy Security process");
AUTOSTART_PROCESSES(&energy_sec_process);
/*---------------------------------------------------------------------------*/
static struct ctimer sample_timer;

static inline unsigned long
to_seconds(uint64_t time)
{
  return (unsigned long)(time / ENERGEST_SECOND);
}

/* callback function that prints energest times
* tracks amount of time CPU is in LPM, Deep LPM, or in use
* tracks radio if it is ON: Listening or Transmitting, and OFF
*/
static void
print_energest_times(void *ptr)
{
  ctimer_reset(&sample_timer);
    /*
   * Update all energest times. Should always be called before energest
   * times are read.
   */
  energest_flush();

  printf(" CPU %4lus LPM %4lus DEEP LPM %4lus  Total time %lus",
         to_seconds(energest_type_time(ENERGEST_TYPE_CPU)),
         to_seconds(energest_type_time(ENERGEST_TYPE_LPM)),
         to_seconds(energest_type_time(ENERGEST_TYPE_DEEP_LPM)),
         to_seconds(ENERGEST_GET_TOTAL_TIME()));
  printf(" Radio LISTEN %4lus TRANSMIT %4lus OFF      %4lus\n",
         to_seconds(energest_type_time(ENERGEST_TYPE_LISTEN)),
         to_seconds(energest_type_time(ENERGEST_TYPE_TRANSMIT)),
         to_seconds(ENERGEST_GET_TOTAL_TIME()
                    - energest_type_time(ENERGEST_TYPE_TRANSMIT)
                    - energest_type_time(ENERGEST_TYPE_LISTEN)));
}

/* intializes timer for callback function, expire ever 10 clock seconds (1/6 of a sec). */
void
print_energest_init(void)
{
  ctimer_set(&sample_timer, 10*CLOCK_SECOND, print_energest_times, NULL);
}

PROCESS_THREAD(energy_sec_process, ev, data)
{
  static struct etimer timer;

  PROCESS_BEGIN();

  /* initialize callback timer to print energest times */
  print_energest_init();

  /* Setup a periodic timer that expires after 1 second. */
  etimer_set(&timer, CLOCK_SECOND * 60);

  /* main process code */
  while(1) {
    printf("Hello, virtual world!\n");

    /* Wait for the periodic timer to expire and then restart the timer. */
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
    etimer_reset(&timer);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
