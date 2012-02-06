from sasi.habitat.habitat import Habitat
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
import sasi.conf.conf as conf
import sasi.conf.feature_assignments as feature_assignments
import sasi.conf.substrate_mappings as substrate_mappings
import sasi.conf.energy_mappings as energy_mappings

def generate_habitats(n):
	energy_codes = list(set(energy_mappings.shp_to_va.values()))

	substrate_codes = list(set(substrate_mappings.shp_to_va.values()))

	habitats = []
	for i in range(n):
		energy = energy_codes[i % len(energy_codes)]
		
		substrate_id = substrate_codes[i % len(substrate_codes)]
		substrate = Substrate(id=substrate_id, name=substrate_id)

		assignments = feature_assignments.assignments[(substrate_id, energy)]
		features = [Feature(id=a,name=a) for a in assignments]

		h = Habitat(
				id = i,
				id_km100 = i,
				id_km1000 = i,
				id_vor = i,
				z = i * -1.0,
				energy = energy,
				substrate = substrate,
				features = features,
				area = i,
				geom = None
				)
		habitats.append(h)

	return habitats

