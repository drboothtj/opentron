from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Heat Shock',
    'author': 'Thom Booth <thoboo@biosustain.dtu.dk>',
    'description': 'Protocol for the transformation of chemical competent E.coli.',
    'apiLevel': '2.12'
}

def run(protocol: protocol_api.ProtocolContext):
    # labware
    dna_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '1')
    ecoli_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2')
    media_rack = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', '4')
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', '9')

    # modules
    heat_block = protocol.load_module('temperature module', 3)
    heat_plate = heat_block.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul')

    # pipettes
    left_pipette = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tiprack_20])
    right_pipette = protocol.load_instrument('p1000_single_gen2', 'right', tip_racks=[tiprack_1000])

    # commands
    #Step 1 - Get the heatblock to temp and wait for user
    heat_block.set_temperature(42) #Note new version waits automatically.

    #Step 2 - Add DNA to E.coli and wait 10 mins
    left_pipette.pick_up_tip()
    left_pipette.aspirate(2, dna_plate['A1'])
    left_pipette.dispense(2, ecoli_plate['A1'].bottom())
    left_pipette.mix(3, 10)
    left_pipette.drop_tip()
    protocol.delay(minutes=10)

    #Step 3 - Transfer to headblock and incubate for 45s
    left_pipette.pick_up_tip()
    left_pipette.aspirate(20, ecoli_plate['A1'])
    left_pipette.dispense(20, heat_plate['A1'])
    left_pipette.drop_tip()
    protocol.delay(seconds=45)

    #Step 4 - Transfer back to block
    left_pipette.pick_up_tip()
    left_pipette.aspirate(20, heat_plate['A1'])
    left_pipette.dispense(20, ecoli_plate['A1'])
    left_pipette.drop_tip()

    #Step 5 - Add LB
    row = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
    right_pipette.pick_up_tip()
    right_pipette.aspirate(1000, media_rack['A1'])
    for well in row:
        right_pipette.dispense(150, ecoli_plate[well])
    right_pipette.drop_tip()
    