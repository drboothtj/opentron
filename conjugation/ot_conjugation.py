from csv import reader
from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Conjugation v 0.0.1',
    'author': 'Thom Booth <thoboo@biosustain.dtu.dk>',
    'description': 'Protocol for transformation of Streptomcyes spores by conjugation with E.coli',
    'apiLevel': '2.12'
}

def read_csv(filename):
    rows = []
    with open(filename, 'r') as read_object:
        csv_reader = reader(read_object, delimiter = ';')
        for row in csv_reader:
            rows.append(row)
    return rows

def get_order_of_operations():
    conjugants = read_csv('conjugants.csv')
    e_colis = read_csv('e_coli.csv')
    mixture = read_csv('mixture.csv')
    operations = []
    for line in mixture:
        e_coli_position = [e_coli[0] for e_coli in e_colis if e_coli[1] == line[2]]
        conjuagant_position = [conjugant[0] for conjugant in conjugants if conjugant[1] == line[1]]
        operations.append([e_coli_position, conjuagant_position])
    return operations

def run(protocol: protocol_api.ProtocolContext):
    #labware -----update
    conjugant_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '1')###FIX
    e_coli_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2')###FIX
    mixture_plate = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', '4')###FIX
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', '9')
    #pippettes
    left_pipette = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tiprack_20])
    right_pipette = protocol.load_instrument('p1000_single_gen2', 'right', tip_racks=[tiprack_1000])
    #get operations from file
    operations = get_order_of_operations()
    #run commands
    for operation in operations:
        right_pipette.pick_up_tip()
        position = ''.join([str(item) for item in operation[0]])
        right_pipette.aspirate(500, e_coli_plate[position])
        right_pipette.dispense(500, mixture_plate['A1']) ##fix
        right_pipette.drop_tip()
        right_pipette.pick_up_tip()
        position = str(operation[1])
        position = ''.join([str(item) for item in operation[1]])
        right_pipette.aspirate(500, conjugant_plate[position])
        right_pipette.dispense(500, mixture_plate['A1']) ##fix
        right_pipette.drop_tip()