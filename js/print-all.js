/*
 * A Contiki test script acts on mote output, such as via printf()'s.
 * The script may operate on the following variables:
 *  Mote mote, int id, String msg
 */
TIMEOUT(60000, log.testOK());

while (true) {
  log.log(time + ":" + id + ":" + msg + "\n");
  YIELD();
}