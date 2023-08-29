'''
Temporary protocol for opentron bioassays

Functions:
    !!!
'''

from opentrons import protocol_api

VOLUME_TO_ASSAY = 100

#metadata needs to be defined outside of a function
metadata = {
    'protocolName': 'Bioassay',
    'author': 'Thom Booth <thoboo@biosustain.dtu.dk>',
    'description': 'Protocol for pairwise bioassays.',
    'apiLevel': '2.12'
}

def get_labware(protocol):
    '''
    returns labware specific to this protocol
        arguments:
            protocol
        returns:
            library_plates: !!!
            test_plates: !!!
            tip_racks: !!!
            pipette: 
    '''
    library_plate_1 = protocol.load_labware('corning_12_wellplate_6.9ml_flat', 1)
    library_plate_2 =protocol.load_labware('corning_12_wellplate_6.9ml_flat', 2)
    library_plate_3 = protocol.load_labware('corning_12_wellplate_6.9ml_flat', 3)
    library_plates = [library_plate_1, library_plate_2, library_plate_3]
    test_plate_1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 4)
    test_plate_2 = protocol.load_labware('corning_96_wellplate_360ul_flat', 5)
    test_plate_3 = protocol.load_labware('corning_96_wellplate_360ul_flat', 6)
    test_plates =[test_plate_1, test_plate_2, test_plate_3]
    tip_rack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 7)
    tip_rack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    tip_racks = [tip_rack_1, tip_rack_2]
    pipette = protocol.load_instrument(
        instrument_name='p300_single_gen2',
        mount='right',
        tip_racks=tip_racks
        )
    return library_plates, test_plates, tip_racks, pipette

def get_destinations(plates, counter):
    '''
    gets wells of a specific index from multiple test plates
        arguments:
            plates: a list of plate objects
            counter: the index to get from all plates 
                (e.g. 0 will return the first well of all plates in the list)
        returns:
            destinations: a list of wells
    '''
    destinations = []
    for plate in plates:
        destinations.append(plate.wells()[counter])
    return destinations

def run(protocol):
    '''
    run is called by the opentron and defines the labware and each step
        arguments:
            protocol: this argument is required by the opentron and is used to specify the run
        returns:
            None
    '''
    library_plates, test_plates, tip_racks, pipette = get_labware(protocol)
    library_wells = [well for library_plate in library_plates for well in library_plate.wells()]
    #we use a counter as we only need to use test wells for as long as we have library wells
    well_counter = 0
    for well in library_wells:
        #distribute method takes a list of wells
        destinations = get_destinations(test_plates, well_counter)
        pipette.distribute(volume=VOLUME_TO_ASSAY, source=well, dest=destinations) 
        well_counter +=1
