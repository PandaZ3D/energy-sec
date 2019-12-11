/*
 * Example Contiki test script (JavaScript).
 * A Contiki test script acts on mote output, such as via printf()'s.
 * The script may operate on the following variables:
 *  Mote mote, int id, String msg
 */

// we want to run the simulation until all nodes are done sending their messages
// clients will send messages to sink node and sink will log when a node is done
var node_id_of_sink = 1
var num_cli_nodes = 3
var num_cli_done = 0
var data_string = 'NaN'
var done_string = 'DONE'

TIMEOUT(6060000, log.testFailed()); // ms

// log csv header
log.log("time,node,ticks,interval,cpu,lpm,dlpm,rx,tx,idle\n");

while (true) {
  YIELD();
  if(msg.contains(data_string)) {
      log.log(time + "," + id + "," + msg + "\n");
  }
  if(id == node_id_of_sink) {
  	if(msg.contains(done_string)) {
  		num_cli_done++;
  	}
  }
  if(num_cli_done == num_cli_nodes) {
  	log.testOK();
  	break;
  }
}