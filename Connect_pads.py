from ihp_photonic.technology import *
from ihp_photonic.trace.waveguide import WaveguideBasic
from ihp_photonic.trace.waveguide import WaveguideRounded

from ihp_photonic.components.waveguide.waveguide_basic import Straight, Offset, OffsetHorzFit, Spiral, RouteAlongPoints, Arc, Arc90Up, Arc90Down
from ihp_photonic.components.waveguide.phaseshifter import PhaseShifter
from ihp_photonic.components.waveguide.transition import Transition
from ihp_photonic.components.mmi import MMI2x2
from ihp_photonic.components.diode.photodiode import PhotoDiodeM2 as PD
from ihp_photonic.components.grating_coupler.grating_coupler_foc1d import  GC1DFoc1550 as GratingCoupler



from ihp_photonic.trace.trace_template_optic import WireWGTemplate, RibWGTemplate, ModWGTemplate, PhaseShifterTemplate
from ihp_photonic.trace.trace_template_backend import WGContactStackTemplate
from ihp_photonic.trace.trace_template_lvs import EmptyTemplate
from ihp_photonic.trace.transition import TransitionLinear

from ihp_photonic.components.backend.pad import DC as Pad
from ihp_photonic.components.backend.heater import Heater
from ihp_photonic.components.backend.contact_plug import ConnectedStack

import math
import numpy as np
import pylab as plt
import os

#from si_fab.components.phase_shifter.simulation.simulate import simulate_phaseshifter
from ipkiss3 import all as i3
import ihp_photonic as ihp




### Components
tt_wg_strip = WireWGTemplate(name='tt_wg_strip').Layout(core_width=0.450)
tt_wg_mod = ModWGTemplate(name='tt_wg_mod')
#tt_wg_backend = WGContactStackTemplate(name="tt_wg_backend")
tt_wg_backend = EmptyTemplate(name="tt_wg_backend")
tt_transition_strip_mod = TransitionLinear(name='tt_transition_strip_mod', trace_template_in=tt_wg_strip,trace_template_out=tt_wg_mod)

wire_tt = i3.ElectricalWireTemplate()


layout_cell = i3.LayoutCell(name="PadsLayout").Layout()

straight_arm_long = Straight(name="straight_arm_long", trace_template=tt_wg_mod)
ps = PhaseShifter(name="ps_straight_long", waveguide_template=straight_arm_long, trace_template_backend=tt_wg_backend)
pad = Pad(name="pad")

num_pads, num_ps = 5, 5

class ConnectPads(i3.Circuit):
    _name_prefix = "CONNECT_PADS"
    waveguide_tt = i3.ChildCellProperty(doc="Waveguide trace template")
    dc_pad_spacing = i3.PositiveNumberProperty(default=100, doc="Spacing between pads")

    def _default_waveguide_tt(self):
        waveguide_tt = tt_wg_strip
        return waveguide_tt

    def _default_insts(self):
        insts = dict()

        insts['ps1'] = ps
        insts['ps2'] = ps

        return insts

    class CircuitModel(i3.CircuitModelView):
        def _generate_model(self):
            return i3.HierarchicalModel.from_netlistview(self.netlist_view)

    class Netlist(i3.NetlistFromLayout):
        pass


    def _default_specs(self):
        specs = []
        dc_pad_spacing = self.dc_pad_spacing
        tt_wg_strip = self.waveguide_tt

        specs.append(i3.Place('ps1', (0, 10)))
        specs.append(i3.Place('ps2', (0, -100)))
        specs.append(i3.ConnectElectrical('ps1:mod_in', 'ps2:mod_in', trace_template=wire_tt))

        return specs

    def _default_exposed_ports(self):
        exposed_ports = dict()
        return exposed_ports


connect_pads = ConnectPads()
connect_pads_lo = connect_pads.Layout()
connect_pads_lo.visualize()

