import csv
from opentrons import protocol_api
#CSV
conjugants_csv = '''
A1;P5A9
A2;P8A1
A3;P8A2
A4;P9A4
'''

e_coli_csv = '''
A1;mcherry
A2;gfp
A3;sarp
A4;globalR
B1;csreg
'''
mixture_csv = '''
A1;P5A9;mcherry
A2;P8A1;mcherry
A3;P8A2;mcherry
A4;P9A4;mcherry
A5;P5A9;gfp
A6;P8A1;gfp
B1;P8A2;gfp
B2;P9A4;gfp
B3;P5A9;sarp
B4;P8A1;sarp
B5;P8A2;sarp
B6;P9A4;sarp
C1;P5A9;globalR
C2;P8A1;globalR
C3;P8A2;globalR
C4;P9A4;globalR
C5;P5A9;csreg
C6;P8A1;csreg
D1;P8A2;csreg
D2;P9A4;csreg
'''

# metadata
metadata = {
    'protocolName': 'Conjugation v 0.0.1',
    'author': 'Thom Booth <thoboo@biosustain.dtu.dk>',
    'description': 'Protocol for transformation of Streptomcyes spores by conjugation with E.coli',
    'apiLevel': '2.12'
}

def read_csv(csv_input):
    rows = []
    csv_data = csv_input.splitlines()[1:]
    csv_reader = csv.reader(csv_data)
    rows = []
    for row in csv_reader:
        print(row)
        rows.append(row[0].split(';'))
    return rows 
    

def get_order_of_operations():
    conjugants = read_csv(conjugants_csv)
    e_colis = read_csv(e_coli_csv)
    mixture = read_csv(mixture_csv)
    e_coli_coordinates = []
    conjugant_coordinates = []
    mixture_coordinates = []
    for line in mixture:
        e_coli_position = [e_coli[0] for e_coli in e_colis if e_coli[1] == line[2]]
        e_coli_coordinates.extend(e_coli_position)
        conjuagant_position = [conjugant[0] for conjugant in conjugants if conjugant[1] == line[1]]
        conjugant_coordinates.extend(conjuagant_position)
        mixture_coordinates.append(line[0])
    return e_coli_coordinates, conjugant_coordinates, mixture_coordinates

def get_string(list_):
    string_ = ''.join([str(item) for item in list_])

def run(protocol: protocol_api.ProtocolContext):
    #labware -----update
    conjugant_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')
    e_coli_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
    mixture_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '4')
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', '9')
    #pippettes
    left_pipette = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tiprack_20])
    right_pipette = protocol.load_instrument('p1000_single_gen2', 'right', tip_racks=[tiprack_1000])
    #get operations from file
    e_coli_coordinates, conjugant_coordinates, mixture_coordinates = get_order_of_operations()
    #run commands
    #transfer e_coli
    for e_coli in set(e_coli_coordinates):
        right_pipette.pick_up_tip()
        for i in range(0,len(e_coli_coordinates)):
            if e_coli_coordinates[i] == e_coli:
                right_pipette.aspirate(200, e_coli_plate[e_coli])
                right_pipette.dispense(200, mixture_plate[mixture_coordinates[i]])
                pipette.blow_out()
        right_pipette.drop_tip()
    #transfer conjugants
    for conjugant in set(conjugant_coordinates):
        right_pipette.pick_up_tip()
        for i in range(0,len(conjugant_coordinates)):
            if conjugant_coordinates[i] == conjugant:
                right_pipette.aspirate(200, conjugant_plate[conjugant].bottom(+2))
                right_pipette.dispense(200, mixture_plate[mixture_coordinates[i]].top(-2))
                pipette.blow_out()
        right_pipette.drop_tip()

    