#!/usr/bin/env python3
# 
# Create a configuration file for simulating in cooja
# 
# output is a .csc file which is an xml file recognized by Cooja
# 
# specify test to run, by default a udp network is used
import xml.etree.cElementTree as ET
import xml.dom.minidom as MD
import math
import sys

PROJ_DIR = "[CONTIKI_DIR]/tests/21-energy-security/code/"
FILE_NAME = ""
SERVER_SRC = "server-node"
CLIENT_SRC = "client-node"
N_CLIENTS = 3

# get program arguments
try:
	test = sys.argv[1]
	if(test == 'dtls'):
		testnum = 2
		CLIENT_SRC = "dtls-"+CLIENT_SRC
		SERVER_SRC = "dtls-"+SERVER_SRC
		FILE_NAME = '{0:02d}-{1}-udp-network'.format(testnum, test)
	else:
		testnum = 1
		FILE_NAME = '{0:02d}-base-{1}-network'.format(testnum, test)
except IndexError:
	print('usage: python3 {} [udp | dtls]'.format(__file__))
	sys.exit(1)

print('[-] generating {0}'.format(FILE_NAME))

# root of configuration file
root = ET.Element("simconf")
# project configs default
ET.SubElement(root, "project", EXPORT="discard").text = "[APPS_DIR]/mrm"
ET.SubElement(root, "project", EXPORT="discard").text = "[APPS_DIR]/mspsim"
ET.SubElement(root, "project", EXPORT="discard").text = "[APPS_DIR]/avrora"
ET.SubElement(root, "project", EXPORT="discard").text = "[APPS_DIR]/serial_socket"
ET.SubElement(root, "project", EXPORT="discard").text = "[APPS_DIR]/powertracker"
# main simulation
sim = ET.SubElement(root, "simulation")
# project title
ET.SubElement(sim, "title").text = "Basic UDP WSN"
ET.SubElement(sim, "randomseed").text = "123456"
ET.SubElement(sim, "motedelay_us").text = "1000000"
# radio characteristics
radio = ET.SubElement(sim, "radiomedium")
radio.text = "org.contikios.cooja.radiomediums.UDGM"
ET.SubElement(radio, "transmitting_range").text = "100"
ET.SubElement(radio, "interference_range").text = "0"
ET.SubElement(radio, "success_ratio_tx").text = "1.0"
ET.SubElement(radio, "success_ratio_rx").text = "1.0"
events = ET.SubElement(sim, "events")
ET.SubElement(events, "logoutput").text = "40000"
# add server mote type
server_mote_type = ET.SubElement(sim, "motetype")
server_mote_type.text = "org.contikios.cooja.mspmote.SkyMoteType"
ET.SubElement(server_mote_type, "identifier").text = "sky1"
ET.SubElement(server_mote_type, "description").text = "server sky"
ET.SubElement(server_mote_type, "source", EXPORT="discard").text = PROJ_DIR+SERVER_SRC+".c"
ET.SubElement(server_mote_type, "commands", EXPORT="discard").text = "make "+SERVER_SRC+".sky TARGET=sky"
ET.SubElement(server_mote_type, "firmware", EXPORT="copy").text = PROJ_DIR+SERVER_SRC+".sky"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.Position"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.RimeAddress"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.IPAddress"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.Mote2MoteRelations"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.MoteAttributes"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspClock"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspMoteID"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyButton"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyFlash"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyCoffeeFilesystem"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.Msp802154Radio"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspSerial"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyLED"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspDebugOutput"
ET.SubElement(server_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyTemperature"
# add client mote type    
client_mote_type = ET.SubElement(sim, "motetype")
client_mote_type.text = "org.contikios.cooja.mspmote.SkyMoteType"
ET.SubElement(client_mote_type, "identifier").text = "sky2"
ET.SubElement(client_mote_type, "description").text = "client sky"
ET.SubElement(client_mote_type, "source", EXPORT="discard").text = PROJ_DIR+CLIENT_SRC+".c"
ET.SubElement(client_mote_type, "commands", EXPORT="discard").text = "make "+CLIENT_SRC+".sky TARGET=sky"
ET.SubElement(client_mote_type, "firmware", EXPORT="copy").text = PROJ_DIR+CLIENT_SRC+".sky"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.Position"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.RimeAddress"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.IPAddress"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.Mote2MoteRelations"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.interfaces.MoteAttributes"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspClock"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspMoteID"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyButton"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyFlash"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyCoffeeFilesystem"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.Msp802154Radio"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspSerial"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyLED"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.MspDebugOutput"
ET.SubElement(client_mote_type, "moteinterface").text = "org.contikios.cooja.mspmote.interfaces.SkyTemperature"
# add actual server mote
server_mote = ET.SubElement(sim, "mote")
s_pos_int_conf = ET.SubElement(server_mote, "interface_config")
s_pos_int_conf.text = "org.contikios.cooja.interfaces.Position"
ET.SubElement(s_pos_int_conf, "x").text = "0"
ET.SubElement(s_pos_int_conf, "y").text = "0"
ET.SubElement(s_pos_int_conf, "z").text = "0"
s_clk_int_conf = ET.SubElement(server_mote, "interface_config")
s_clk_int_conf.text = "org.contikios.cooja.mspmote.interfaces.MspClock"
ET.SubElement(s_clk_int_conf, "deviation").text = "1.0"
s_id_int_conf = ET.SubElement(server_mote, "interface_config")
s_id_int_conf.text = "org.contikios.cooja.mspmote.interfaces.MspMoteID"
ET.SubElement(s_id_int_conf, "id").text = "1"
ET.SubElement(server_mote, "motetype_identifier").text = "sky1"
# make N client nodes
deg = math.radians(360.0 / N_CLIENTS)
dist = 25
for node in range(N_CLIENTS):
	client_mote = ET.SubElement(sim, "mote")
	c_pos_int_conf = ET.SubElement(client_mote, "interface_config")
	c_pos_int_conf.text = "org.contikios.cooja.interfaces.Position"
	ET.SubElement(c_pos_int_conf, "x").text = str(dist*math.cos(deg*node))
	ET.SubElement(c_pos_int_conf, "y").text = str(dist*math.sin(deg*node))
	ET.SubElement(c_pos_int_conf, "z").text = "0"
	c_clk_int_conf = ET.SubElement(client_mote, "interface_config")
	c_clk_int_conf.text = "org.contikios.cooja.mspmote.interfaces.MspClock"
	ET.SubElement(c_clk_int_conf, "deviation").text = "1.0"
	c_id_int_conf = ET.SubElement(client_mote, "interface_config")
	c_id_int_conf.text = "org.contikios.cooja.mspmote.interfaces.MspMoteID"
	ET.SubElement(c_id_int_conf, "id").text = str(node + 2)
	ET.SubElement(client_mote, "motetype_identifier").text = "sky2"
# write GUI plugins and script runner
plugin = ET.SubElement(root, "plugin")
plugin.text = "org.contikios.cooja.plugins.SimControl"
ET.SubElement(plugin, "width").text = "280"
ET.SubElement(plugin, "z").text = "1"
ET.SubElement(plugin, "height").text = "160"
ET.SubElement(plugin, "location_x").text = "5"
ET.SubElement(plugin, "location_y").text = "405"

plugin = ET.SubElement(root, "plugin")
plugin.text = "org.contikios.cooja.plugins.Visualizer"
plugin_config = ET.SubElement(plugin, "plugin_config")
ET.SubElement(plugin_config, "moterelations").text = "true"
ET.SubElement(plugin_config, "skin").text = "org.contikios.cooja.plugins.skins.IDVisualizerSkin"
ET.SubElement(plugin_config, "skin").text = "org.contikios.cooja.plugins.skins.GridVisualizerSkin"
ET.SubElement(plugin_config, "skin").text = "org.contikios.cooja.plugins.skins.TrafficVisualizerSkin"
ET.SubElement(plugin_config, "skin").text = "org.contikios.cooja.plugins.skins.UDGMVisualizerSkin"
ET.SubElement(plugin_config, "viewport").text = "4.722167701066176 0.0 0.0 4.722167701066176 -26.241678027219393 25.649157907619177"
ET.SubElement(plugin, "width").text = "400"
ET.SubElement(plugin, "z").text = "3"
ET.SubElement(plugin, "height").text = "400"
ET.SubElement(plugin, "location_x").text = "1"
ET.SubElement(plugin, "location_y").text = "1"

plugin = ET.SubElement(root, "plugin")
plugin.text = "org.contikios.cooja.plugins.ScriptRunner"
plugin_config = ET.SubElement(plugin, "plugin_config")
ET.SubElement(plugin_config, "scriptfile").text = "[CONFIG_DIR]/js/logger.js"
ET.SubElement(plugin_config, "active").text = "true"
ET.SubElement(plugin, "width").text = "600"
ET.SubElement(plugin, "z").text = "0"
ET.SubElement(plugin, "height").text = "632"
ET.SubElement(plugin, "location_x").text = "31"
ET.SubElement(plugin, "location_y").text = "31"
# get xml file as a string
xml_string = ET.tostring(root, encoding="UTF-8", method="xml")

# make document look pretty
dom = MD.parseString(xml_string)
pretty_xml_string = dom.toprettyxml(indent="  ", newl="\n", encoding="UTF-8")

# write changes to file
with open(FILE_NAME+".csc", "wb") as xml_file:
	xml_file.write(pretty_xml_string)