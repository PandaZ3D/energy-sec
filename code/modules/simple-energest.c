/*
 * Copyright (c) 2018, RISE SICS.
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
 */

/**
* \addtogroup simple-energest
* @{
*/

/**
 * \file
 *         A process that periodically prints out the time spent in
 *         radio tx, radio rx, total time and duty cycle with clock tick precision.
 *
 * \author Simon Duquennoy <simon.duquennoy@ri.se>
 * 
 * \edit Allen Aboytes <aaboytes@ucsc.edu>
 */

#include "contiki.h"
#include "sys/energest.h"
#include "simple-energest.h"
#include <stdio.h>
#include <limits.h>

static unsigned long last_tx, last_rx, last_time, last_cpu, last_lpm, last_deep_lpm;
static unsigned long delta_tx, delta_rx, delta_time, delta_cpu, delta_lpm, delta_deep_lpm;
static unsigned long curr_tx, curr_rx, curr_time, curr_cpu, curr_lpm, curr_deep_lpm;

PROCESS(simple_energest_process, "Simple Energest");
/*---------------------------------------------------------------------------*/
static void
simple_energest_step(void)
{
  energest_flush();

  curr_time = ENERGEST_GET_TOTAL_TIME();
  curr_cpu = energest_type_time(ENERGEST_TYPE_CPU);
  curr_lpm = energest_type_time(ENERGEST_TYPE_LPM);
  curr_deep_lpm = energest_type_time(ENERGEST_TYPE_DEEP_LPM);
  curr_tx = energest_type_time(ENERGEST_TYPE_TRANSMIT);
  curr_rx = energest_type_time(ENERGEST_TYPE_LISTEN);
  
  delta_time = curr_time - last_time;
  delta_cpu = curr_cpu - last_cpu;
  delta_lpm = curr_lpm - last_lpm;
  delta_deep_lpm = curr_deep_lpm - last_deep_lpm;
  delta_tx = curr_tx - last_tx;
  delta_rx = curr_rx - last_rx;
  unsigned long time_idle = 0;
  if(delta_tx+delta_rx < delta_time)
    time_idle = delta_time - delta_tx - delta_rx;

  last_time = curr_time;
  last_cpu = curr_cpu;
  last_lpm = curr_lpm;
  last_deep_lpm = curr_deep_lpm;
  last_tx = curr_tx;
  last_rx = curr_rx;
  
  /*
  * time is in energest clock ticks
  * tracks amount of time CPU is in LPM, Deep LPM, or in use
  * tracks radio if it is ON: Listening (Rx) or Transmitting (Tx), and OFF (idle)
  */
  printf("NaN,%lu,%lu,%lu,%lu,%lu,%lu,%lu\n",
    delta_time, delta_cpu, delta_lpm, delta_deep_lpm, delta_rx, delta_tx, time_idle);
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(simple_energest_process, ev, data)
{
  static struct etimer periodic_timer;
  PROCESS_BEGIN();

  etimer_set(&periodic_timer, SIMPLE_ENERGEST_PERIOD);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
    etimer_reset(&periodic_timer);
    simple_energest_step();
  }
  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
void
simple_energest_init(void)
{
  energest_flush();
  last_time = ENERGEST_GET_TOTAL_TIME();
  last_cpu = energest_type_time(ENERGEST_TYPE_CPU);
  last_lpm = energest_type_time(ENERGEST_TYPE_LPM);
  curr_tx = energest_type_time(ENERGEST_TYPE_TRANSMIT);
  last_deep_lpm = energest_type_time(ENERGEST_TYPE_DEEP_LPM);
  last_rx = energest_type_time(ENERGEST_TYPE_LISTEN);
  printf("ENERGEST_SECOND %u\n", ENERGEST_SECOND);
  process_start(&simple_energest_process, NULL);
}

/** @} */
