import numpy as np
import json
import math
from xml.dom import minidom
import copy


class Eval():
	def __init__(self, output_size):
		try:
			doc = minidom.parse('plugins/SerpentDonkeyKongNeatResultGameAgentPlugin/files/helpers/config.xml')
			filename = doc.getElementsByTagName("ann")[0].firstChild.nodeValue.strip()
			
			self.HEIGHT_RADIUS = int(doc.getElementsByTagName("height_radius")[0].firstChild.nodeValue.strip()) #2
			self.WIDTH_RADIUS = int(doc.getElementsByTagName("height_radius")[0].firstChild.nodeValue.strip()) #2
			self.INPUT_SIZE = (self.HEIGHT_RADIUS + 1) * (self.WIDTH_RADIUS * 2 + 1) + 1

			self.INPUTS = self.INPUT_SIZE + 1
			self.OUTPUTS = output_size

			self.MAX_NODES = int(doc.getElementsByTagName("max_nodes")[0].firstChild.nodeValue.strip()) #1000000

			with open('plugins/SerpentDonkeyKongNeatResultGameAgentPlugin/files/helpers/' + filename + '.json') as f:
				self.ann = json.load(f)
			self._generate_network(self.ann)

		except FileNotFoundError:
			self._create_config_file()
			print("Config file created. Modify it to load your ANN.")

	def _create_config_file(self):
		print("No config file found for Neuro-Evolution.\n Creation of the default config file.")
		doc = minidom.Document()

		config = doc.createElement('config')

		ann = doc.createElement('ann')
		ann.appendChild(doc.createTextNode("JSON FILE NAME HERE (without extension)"))

		inputs = doc.createElement('inputs')
		height_radius = doc.createElement('height_radius')
		height_radius.appendChild(doc.createTextNode("2"))
		width_radius = doc.createElement('width_radius')
		width_radius.appendChild(doc.createTextNode("2"))
		inputs.appendChild(height_radius)
		inputs.appendChild(width_radius)

		max_nodes = doc.createElement("max_nodes")
		max_nodes.appendChild(doc.createTextNode("1000000"))

		config.appendChild(ann)
		config.appendChild(inputs)
		config.appendChild(max_nodes)

		doc.appendChild(config)

		doc.writexml(open('plugins/SerpentDonkeyKongNeatResultGameAgentPlugin/files/helpers/config.xml', 'w'), indent="    ", addindent="  ", newl='\n')

	def _generate_network(self, genome):
		network = dict()
		network["neurons"] = dict()
	
		for i in range(self.INPUTS):
			network["neurons"][i] = self._new_neuron()
	
		for o in range(self.OUTPUTS):
			network["neurons"][self.MAX_NODES+o] = self._new_neuron()
	
		genome["genes"].sort(key=lambda x : x["out"])

		for gene in genome["genes"]:
			if (gene["enabled"]):
				if (not (gene["out"] in network["neurons"])):
					network["neurons"][gene["out"]] = self._new_neuron()
				neuron = network["neurons"][gene["out"]]
				neuron["incoming"].append(gene)
				if (not (gene["into"] in network["neurons"])):
					network["neurons"][gene["into"]] = self._new_neuron()
		
		genome["network"] = network

	def _new_neuron(self):
		neuron = dict()
		neuron["incoming"] = []
		neuron["value"] = 0.0

		return neuron

	def feed(self, inputs):
		#print(inputs)
		keys = self._evaluate_network(copy.deepcopy(self.ann["network"]), inputs)
		# print(keys)
		return keys

	def _evaluate_network(self, network, inputs):
		inputs = np.append(inputs, [1])

		if (len(inputs) != self.INPUTS):
			return [0,0,0,0,0]
		
		for i in range(self.INPUTS):
			network["neurons"][i]["value"] = inputs[i]
		
		for key, neuron in network["neurons"].items():
			total = 0
			for j in range(len(neuron["incoming"])):
				incoming = neuron["incoming"][j]
				other = network["neurons"][incoming["into"]]
				total = total + incoming["weight"] * other["value"]
			
			if (len(neuron["incoming"]) > 0):
				neuron["value"] = self._sigmoid(total)
		
		outputs = []
		for o in range(self.OUTPUTS):
			if (network["neurons"][self.MAX_NODES+o]["value"] > 0):
				outputs.append(1)
			else:
				outputs.append(0)
		
		return outputs

	def _sigmoid(self, x):
		return 2/(1+math.exp(-4.9*x))-1

	def fitness(self, scores):		
		score = 1000 * scores[0] + scores[1] + 100 * scores[2] - 10 * scores[3] + 500 * scores[4]
		print("Score : " + str(score))