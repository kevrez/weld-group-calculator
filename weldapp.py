# from tkinter import *
from tkinter import (
    Label,
    StringVar,
    Entry,
    OptionMenu,
    LabelFrame,
    Radiobutton,
    Frame,
)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from weldgroup import WeldGroup
from datetime import datetime


class Application(Frame):

    def __init__(self, master, version):
        self.VERSION = version
        super().__init__(master)
        self.grid()
        self.draw_ui()

    def draw_ui(self):
        self.title_status = Label(self, text="Weld Type: E70XX  -  AISC 360")
        self.title_status.grid(row=30, column=3, sticky='se', padx=(0, 25))

        self.year = datetime.today().strftime("%Y")
        self.title_copyright = Label(
            self, text=f"© Kevin Reznicek {self.year}  -  V{self.VERSION}")
        self.title_copyright.grid(
            row=30, column=0, columnspan=2, sticky='sw', padx=(25, 0))

        # draw labelframes and widgets
        self.draw_weldtype()
        self.draw_weldgroup()
        self.draw_units()
        self.draw_loads()
        self.draw_results()
        self.draw_preview()

        # add trace functions to Tk inputs
        self.add_traces()

        # draw CALCULATE button
        # self.run_button = Button(self, text="RECALCULATE", command=self.recalc_full, pady=5, padx=10)
        # self.run_button.grid(row=3, column=2, pady=(5, 0), padx=(15, 10), sticky='nesw')
        # # self.run_button["state"] = "normal"

        # # draw RESET PLOT buton
        # self.reset_plot_button = Button(self, text="RESET PLOT", command=self.reset_plot, pady=5, padx=10)
        # self.reset_plot_button.grid(row=3, column=3, pady=(5, 0), padx=(5, 25), sticky='nesw')

        # enable resizing to follow window size
        for i in range(3):
            self.rowconfigure(i, weight=1)
        for i in range(2):
            self.columnconfigure(i, weight=2)
        for i in range(2, 4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)

    def draw_weldtype(self):

        ##### set up Weld Type LabelFrame, variables, widgets #####

        ### LabelFrame ###
        self.f_weld_type = LabelFrame(
            self, text="Weld Type")  # height=230, width=230
        self.f_weld_type.grid(row=0, column=0, padx=(
            25, 5), pady=(10, 0), sticky='nesw')

        ### variables ###
        # options for hss thickness
        self.hss_thickness_options = ["1/8\"",
                                      "3/16\"",
                                      "1/4\"",
                                      "5/16\"",
                                      "3/8\"",
                                      "7/16\"",
                                      "1/2\"",
                                      ]

        # options for fillet weld throats
        self.fillet_options = ["1/8\"",
                               "3/16\"",
                               "1/4\"",
                               "5/16\"",
                               "3/8\"",
                               "7/16\"",
                               "1/2\"",
                               ]

        # formulas for fillet weld strengths use weld throat in self.sixteenths.
        # this allows us to convert from the selection directly to self.sixteenths
        self.sixteenths = {"1/8\"": 2,
                           "3/16\"": 3,
                           "1/4\"": 4,
                           "5/16\"": 5,
                           "3/8\"": 6,
                           "7/16\"": 7,
                           "1/2\"": 8,
                           }

        # set up variable for weld type
        self.weldtype = StringVar(self)
        self.weldtype.set("f")  # default value

        # set up variable for hss thickness
        self.selected_hss_thickness = StringVar(self)
        self.selected_hss_thickness.set(
            self.hss_thickness_options[2])  # default value

        # fillet weld size variable
        self.selected_throat = StringVar(self)
        self.selected_throat.set(self.fillet_options[1])  # default value

        # set up master variable for selected weld strength
        self.text_weld_strength = StringVar(self)
        self.text_weld_strength.set("-- kip/in")

        ### widgets ###

        self.PADX_WELD_TYPE = (5, 0)
        self.PADY_WELD_TYPE = (0, 0)
        self.DROPDOWN_WIDTH = 4

        # fillet weld radio button
        self.radio_fillet = Radiobutton(
            self.f_weld_type, text="Fillet", value="f", variable=self.weldtype)
        self.radio_fillet.grid(row=1, column=0, padx=(
            10, 130), pady=self.PADY_WELD_TYPE, sticky='w', columnspan=3)

        # fillet weld size text box
        self.label_fillet_throat = Label(
            self.f_weld_type, text="Throat in 1/16\":", padx=10)
        self.label_fillet_throat.grid(
            row=2, column=0, padx=self.PADX_WELD_TYPE, pady=(0, 0), sticky='ew')

        # set up and draw dropdown menu for fillet weld size
        self.dropdown_fillet = OptionMenu(
            self.f_weld_type, self.selected_throat, *self.fillet_options)
        self.dropdown_fillet.grid(row=2, column=1, pady=(
            0, 0), sticky='ew', padx=(0, 10))
        self.dropdown_fillet.config(width=self.DROPDOWN_WIDTH)

        # flare bevel radio button
        self.radio_fb = Radiobutton(
            self.f_weld_type, text="Flare Bevel", value="fb", variable=self.weldtype)
        self.radio_fb.grid(row=3, column=0, padx=(10, 0), sticky='w')

        # flare bevel - hss thickness label
        self.label_hss_thickness = Label(
            self.f_weld_type, text="HSS Thickness:", padx=10)
        self.label_hss_thickness.grid(
            row=4, column=0, padx=self.PADX_WELD_TYPE, pady=(0, 0), sticky='ew')

        # flare bevel - hss thickness dropdown
        self.dropdown_hss_thickness = OptionMenu(
            self.f_weld_type, self.selected_hss_thickness, *self.hss_thickness_options)
        self.dropdown_hss_thickness.grid(
            row=4, column=1, pady=(0, 0), sticky='ew', padx=(0, 10))
        self.dropdown_hss_thickness.config(width=self.DROPDOWN_WIDTH)

        # selected weld strength text boxes
        self.label_weld_strength = Label(
            self.f_weld_type, text="Selected\nWeld Strength:")
        self.label_weld_strength.grid(
            row=5, column=0, sticky='ew', pady=(0, 10))

        # weld klf label
        self.label_linear_strength = Label(
            self.f_weld_type, textvariable=self.text_weld_strength, font="helvetica 9 bold")
        self.label_linear_strength.grid(
            row=5, column=1, pady=(0, 10), sticky='nsw')

        for i in range(10):
            self.f_weld_type.rowconfigure(i, weight=1)
            self.f_weld_type.columnconfigure(i, weight=1)

        # self.columnconfigure(1, weight=2)

    def draw_weldgroup(self):

        ##### set up Weld Group LabelFrame, variables, widgets #####

        ### LabelFrame ###
        self.f_weld_group = LabelFrame(
            self, text="Weld Group")  # height=230, width=230
        self.f_weld_group.grid(row=1, column=0, padx=(
            25, 5), pady=(10, 0), sticky='nesw')

        ### variables ###
        self.weld_group_options = ['|',
                                   '-',
                                   '||',
                                   '=',
                                   '▯',
                                   '⨅',
                                   '╥',
                                   '╦',
                                   '⌶',
                                   ]

        # variable for selected weld group
        self.selected_weld_group = StringVar(self)
        self.selected_weld_group.set(
            self.weld_group_options[self.weld_group_options.index("=")])  # default value

        ### widgets ###

        # tuple that allows correct placement of the widgets
        self.PADX_WELD_GROUP = (25, 0)
        self.PADY_WELD_GROUP = (5, 0)

        # weld group dropdown
        self.dropdown_weld_group = OptionMenu(
            self.f_weld_group, self.selected_weld_group, *self.weld_group_options)
        self.dropdown_weld_group.grid(
            row=0, column=1, pady=self.PADY_WELD_GROUP, columnspan=5, padx=(40, 0), sticky='ew')
        self.dropdown_weld_group.config(width=1)

        # weld group selection label
        self.label_group = Label(self.f_weld_group, text='Group:')
        self.label_group.grid(row=0, column=0, padx=(
            self.PADX_WELD_GROUP), pady=self.PADY_WELD_GROUP, sticky='w')

        # b and d text variables for property entry boxes
        self.var_b = StringVar(self)
        self.var_b.set("0")
        self.var_d = StringVar(self)
        self.var_d.set("0")

        # b label
        self.label_b = Label(self.f_weld_group, text="b:")
        self.label_b.grid(row=2, column=0, padx=(self.PADX_WELD_GROUP))

        # b entry box
        self.entry_b = Entry(self.f_weld_group, width=5,
                             textvariable=self.var_b)
        self.entry_b.grid(row=2, column=1)

        # b units label
        self.label_b_units = Label(self.f_weld_group, text="in")
        self.label_b_units.grid(row=2, column=2)

        # d label
        self.label_d = Label(self.f_weld_group, text="d:")
        self.label_d.grid(row=3, column=0, padx=(self.PADX_WELD_GROUP))

        # d entry box
        self.entry_d = Entry(self.f_weld_group, width=5,
                             textvariable=self.var_d)
        self.entry_d.grid(row=3, column=1)

        # d units label
        self.label_d_units = Label(self.f_weld_group, text="in")
        self.label_d_units.grid(row=3, column=2)

        for i in range(10):
            self.f_weld_group.rowconfigure(i, weight=1)
            self.f_weld_group.columnconfigure(i, weight=1)

        self.f_weld_group.rowconfigure(1, weight=2)

    def draw_units(self):

        ##### set up Weld Group LabelFrame, variables, widgets #####

        ### LabelFrame ###
        self.f_units = LabelFrame(self, text="Units")  # height=230, width=230
        self.f_units.grid(row=2, column=0, padx=(25, 5),
                          pady=(10, 0), rowspan=3, sticky='nesw')

        self.units = StringVar(self)
        self.units.set('in')  # default value

        self.radio_units = Radiobutton(
            self.f_units, text="kip-in", value="in", variable=self.units)
        self.radio_units.grid(row=0, column=0, padx=(
            10, 0), pady=(5, 5), sticky='nsew')

        self.radio_units = Radiobutton(
            self.f_units, text="kip-ft", value="ft", variable=self.units)
        self.radio_units.grid(row=0, column=1, padx=(
            0, 25), pady=(5, 5), sticky='nsew')

        for i in range(2):
            self.f_units.rowconfigure(i, weight=1)
            self.f_units.columnconfigure(i, weight=1)

    def draw_loads(self):

        ##### set up Loads LabelFrame, widgets #####

        ### LabelFrame ###
        self.f_loads = LabelFrame(self, text="Loads")  # height=230, width=230
        self.f_loads.grid(row=0, column=1, padx=(5, 5),
                          pady=(10, 0), sticky='nesw')

        ### widgets ###

        self.PADX_LOADING = (30, 0)
        self.PADY_LOADING = (3, 0)

        # property titles
        self.title_Mux = Label(self.f_loads, text="Mu-x:")
        self.title_Mux.grid(row=0, column=0, padx=self.PADX_LOADING,
                            pady=self.PADY_LOADING, sticky='ns')
        self.title_Muy = Label(self.f_loads, text="Mu-y:")
        self.title_Muy.grid(row=1, column=0, padx=self.PADX_LOADING,
                            pady=self.PADY_LOADING, sticky='ns')
        self.title_Vux = Label(self.f_loads, text="Vu-x:")
        self.title_Vux.grid(row=2, column=0, padx=self.PADX_LOADING,
                            pady=self.PADY_LOADING, sticky='ns')
        self.title_Vuy = Label(self.f_loads, text="Vu-y:")
        self.title_Vuy.grid(row=3, column=0, padx=self.PADX_LOADING,
                            pady=self.PADY_LOADING, sticky='ns')
        self.title_Au = Label(self.f_loads, text="Au:")
        self.title_Au.grid(row=4, column=0, padx=self.PADX_LOADING,
                           pady=self.PADY_LOADING, sticky='ns')
        self.title_Tu = Label(self.f_loads, text="Tu:")
        self.title_Tu.grid(row=5, column=0, padx=self.PADX_LOADING,
                           pady=self.PADY_LOADING, sticky='ns')

        # text variables for property entry boxes
        self.var_Mux = StringVar(self)
        self.var_Muy = StringVar(self)
        self.var_Vux = StringVar(self)
        self.var_Vuy = StringVar(self)
        self.var_Au = StringVar(self)
        self.var_Tu = StringVar(self)

        # set default values for
        self.var_Mux.set("0")
        self.var_Muy.set("0")
        self.var_Vux.set("0")
        self.var_Vuy.set("0")
        self.var_Au.set("0")
        self.var_Tu.set("0")

        # property entry boxes
        self.ENTRY_WIDTH = 7
        self.entry_Mux = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Mux)
        self.entry_Mux.grid(row=0, column=3, pady=self.PADY_LOADING)
        self.entry_Muy = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Muy)
        self.entry_Muy.grid(row=1, column=3, pady=self.PADY_LOADING)
        self.entry_Vux = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Vux)
        self.entry_Vux.grid(row=2, column=3, pady=self.PADY_LOADING)
        self.entry_Vuy = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Vuy)
        self.entry_Vuy.grid(row=3, column=3, pady=self.PADY_LOADING)
        self.entry_Au = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Au)
        self.entry_Au.grid(row=4, column=3, pady=self.PADY_LOADING)
        self.entry_Tu = Entry(
            self.f_loads, width=self.ENTRY_WIDTH, textvariable=self.var_Tu)
        self.entry_Tu.grid(row=5, column=3, pady=self.PADY_LOADING)

        # property units
        self.units_moment = StringVar(self)
        self.units_moment.set('kip-in')
        self.label_units1 = Label(self.f_loads, textvariable=self.units_moment)
        self.label_units1.grid(
            row=0, column=4, pady=self.PADY_LOADING, sticky='ns')
        self.label_units2 = Label(self.f_loads, textvariable=self.units_moment)
        self.label_units2.grid(
            row=1, column=4, pady=self.PADY_LOADING, sticky='ns')
        self.label_units3 = Label(self.f_loads, text="kip")
        self.label_units3.grid(
            row=2, column=4, pady=self.PADY_LOADING, sticky='ns')
        self.label_units4 = Label(self.f_loads, text="kip")
        self.label_units4.grid(
            row=3, column=4, pady=self.PADY_LOADING, sticky='ns')
        self.label_units5 = Label(self.f_loads, text="kip")
        self.label_units5.grid(
            row=4, column=4, pady=self.PADY_LOADING, sticky='ns')
        self.label_units6 = Label(self.f_loads, textvariable=self.units_moment)
        self.label_units6.grid(
            row=5, column=4, pady=self.PADY_LOADING, sticky='ns')

        for i in range(10):
            self.f_loads.rowconfigure(i, weight=1)
            self.f_loads.columnconfigure(i, weight=1)

    def draw_results(self):

        ##### set up Results LabelFrame, variables, widgets #####

        ### LabelFrame ###
        self.f_results = LabelFrame(self, text="Results")

        for i in range(10):
            self.f_results.rowconfigure(i, weight=2)
            self.f_results.columnconfigure(i, weight=2)

        self.f_results.grid(row=1, column=1, rowspan=3,
                            padx=(5, 5), pady=(10, 0), sticky='nesw')

        ### widgets ###

        self.PADX_RESULTS = (5, 0)
        self.PADY_RESULTS = (5, 0)
        self.PADX_RESULTS_UNITS = (10, 0)
        self.PADY_UTIL_RATIO_TOTAL = (0, 10)
        self.PADX_PROPERTY_UTILIZATION = (45, 45)
        self.PADY_PROPERTY_UTILIZATION = (5, 0)

        # results - section property labels
        self.title_properties = Label(self.f_results, text="Property")
        self.title_properties.grid(row=0, column=0, columnspan=3,
                                   padx=self.PADX_PROPERTY_UTILIZATION, pady=self.PADY_PROPERTY_UTILIZATION)
        self.title_indiv_ratio = Label(self.f_results, text="% Utilization")
        self.title_indiv_ratio.grid(
            row=0, column=3, pady=self.PADY_PROPERTY_UTILIZATION)
        self.label_phiMnx = Label(self.f_results, text="ϕMn-x: ")
        self.label_phiMnx.grid(
            row=1, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')
        self.label_phiMny = Label(self.f_results, text="ϕMn-y: ")
        self.label_phiMny.grid(
            row=2, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')
        self.label_phiVnx = Label(self.f_results, text="ϕVn-x: ")
        self.label_phiVnx.grid(
            row=3, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')
        self.label_phiVny = Label(self.f_results, text="ϕVn-y: ")
        self.label_phiVny.grid(
            row=4, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')
        self.label_phiAn = Label(self.f_results, text="ϕAn: ")
        self.label_phiAn.grid(
            row=5, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')
        self.label_phiTn = Label(self.f_results, text="ϕTn: ")
        self.label_phiTn.grid(
            row=6, column=0, padx=self.PADX_RESULTS, pady=self.PADY_RESULTS, sticky='nsw')

        self.label_utilization = Label(
            self.f_results, text="Utilization\nRatio Total:")
        self.label_utilization.grid(
            row=16, column=0, columnspan=2, pady=self.PADY_UTIL_RATIO_TOTAL)

        # section property default values
        self.var_phiMnx = StringVar()
        self.var_phiMnx.set("0.0")
        self.label_phiMnx_val = Label(
            self.f_results, textvariable=self.var_phiMnx)
        self.label_phiMnx_val.grid(
            row=1, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiMny = StringVar()
        self.var_phiMny.set("0.0")
        self.label_phiMny_val = Label(
            self.f_results, textvariable=self.var_phiMny)
        self.label_phiMny_val.grid(
            row=2, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiVnx = StringVar()
        self.var_phiVnx.set("0.0")
        self.label_phiVnx_val = Label(
            self.f_results, textvariable=self.var_phiVnx)
        self.label_phiVnx_val.grid(
            row=3, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiVny = StringVar()
        self.var_phiVny.set("0.0")
        self.label_phiVny_val = Label(
            self.f_results, textvariable=self.var_phiVny)
        self.label_phiVny_val.grid(
            row=4, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiAn = StringVar()
        self.var_phiAn.set("0.0")
        self.label_phiAn_val = Label(
            self.f_results, textvariable=self.var_phiAn)
        self.label_phiAn_val.grid(
            row=5, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiTn = StringVar()
        self.var_phiTn.set("0.0")
        self.label_phiTn_val = Label(
            self.f_results, textvariable=self.var_phiTn)
        self.label_phiTn_val.grid(
            row=6, column=1, padx=self.PADX_RESULTS_UNITS, pady=self.PADY_RESULTS, sticky='nsew')

        # section property units
        self.label_phiMnx_unit = Label(
            self.f_results, textvariable=self.units_moment)
        self.label_phiMnx_unit.grid(
            row=1, column=2, pady=self.PADY_RESULTS, sticky='nse')
        self.label_phiMny_unit = Label(
            self.f_results, textvariable=self.units_moment)
        self.label_phiMny_unit.grid(
            row=2, column=2, pady=self.PADY_RESULTS, sticky='nse')
        self.label_phiVnx_unit = Label(self.f_results, text="kip")
        self.label_phiVnx_unit.grid(
            row=3, column=2, pady=self.PADY_RESULTS, sticky='nse')
        self.label_phiVny_unit = Label(self.f_results, text="kip")
        self.label_phiVny_unit.grid(
            row=4, column=2, pady=self.PADY_RESULTS, sticky='nse')
        self.label_phiAn_unit = Label(self.f_results, text="kip")
        self.label_phiAn_unit.grid(
            row=5, column=2, pady=self.PADY_RESULTS, sticky='nse')
        self.label_phiTn_unit = Label(
            self.f_results, textvariable=self.units_moment)
        self.label_phiTn_unit.grid(
            row=6, column=2, pady=self.PADY_RESULTS, sticky='nse')

        # individual utilization default values
        self.var_phiMnx_util = StringVar()
        self.var_phiMnx_util.set("0.0 %")
        self.label_phiMnx_util = Label(
            self.f_results, textvariable=self.var_phiMnx_util)
        self.label_phiMnx_util.grid(
            row=1, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiMny_util = StringVar()
        self.var_phiMny_util.set("0.0 %")
        self.label_phiMny_util = Label(
            self.f_results, textvariable=self.var_phiMny_util)
        self.label_phiMny_util.grid(
            row=2, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiVnx_util = StringVar()
        self.var_phiVnx_util.set("0.0 %")
        self.label_phiVnx_util = Label(
            self.f_results, textvariable=self.var_phiVnx_util)
        self.label_phiVnx_util.grid(
            row=3, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiVny_util = StringVar()
        self.var_phiVny_util.set("0.0 %")
        self.label_phiVny_util = Label(
            self.f_results, textvariable=self.var_phiVny_util)
        self.label_phiVny_util.grid(
            row=4, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiAn_util = StringVar()
        self.var_phiAn_util.set("0.0 %")
        self.label_phiAn_util = Label(
            self.f_results, textvariable=self.var_phiAn_util)
        self.label_phiAn_util.grid(
            row=5, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_phiTn_util = StringVar()
        self.var_phiTn_util.set("0.0 %")
        self.label_phiTn_util = Label(
            self.f_results, textvariable=self.var_phiTn_util)
        self.label_phiTn_util.grid(
            row=6, column=3, pady=self.PADY_RESULTS, sticky='nsew')

        self.var_total_util = StringVar()
        self.var_total_util.set("0.0 %")
        self.label_total_utilization = Label(
            self.f_results, textvariable=self.var_total_util)
        self.label_total_utilization.grid(
            row=16, column=3, pady=self.PADY_UTIL_RATIO_TOTAL, sticky='nsew')

        for i in range(10):
            self.f_results.rowconfigure(i, weight=1)
            self.f_results.columnconfigure(i, weight=1)

    def draw_preview(self):
        ##### set up Plot LabelFrame, variables, widgets #####

        ### LabelFrame ###
        self.f_plot = LabelFrame(self, text="Preview")

        for i in range(10):
            self.f_plot.rowconfigure(i, weight=1)
            self.f_plot.columnconfigure(i, weight=1)

        self.f_plot.grid(row=0, column=2, padx=(5, 25), pady=(
            10, 0), rowspan=3, columnspan=2, sticky='nse')

        # draw plot
        self.draw_plot()

    def draw_plot(self):
        self.fig1, self.ax1 = plt.subplots(
            figsize=(3.8, 10))  # figsize=(4.6, 4.3)
        self.fig1.set_tight_layout(True)
        self.ax1.axvline(color='black', linestyle=':')
        self.ax1.axhline(color='black', linestyle=':')

        self.ax1.set(xlabel='Y', ylabel='X')
        self.ax1.axis('equal')
        self.ax1.set_xlim(-5, 5)
        self.ax1.set_ylim(-5, 5)
        self.ax1.minorticks_on()

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.f_plot)
        self.canvas.draw()

        self.toolbar = None

        self.tkwidget = self.canvas.get_tk_widget()
        self.tkwidget.grid(sticky='nsew')

    def add_traces(self):
        self.weldtype.trace_add('write', self.recalc_results)
        self.selected_hss_thickness.trace_add('write', self.recalc_results)
        self.selected_throat.trace_add('write', self.recalc_results)
        self.selected_weld_group.trace_add('write', self.recalc_full)

        self.var_b.trace_add('write', self.recalc_full)
        self.var_d.trace_add('write', self.recalc_full)

        self.units.trace_add('write', self.recalc_results)

        self.var_Mux.trace_add('write', self.recalc_results)
        self.var_Muy.trace_add('write', self.recalc_results)
        self.var_Vux.trace_add('write', self.recalc_results)
        self.var_Vuy.trace_add('write', self.recalc_results)
        self.var_Au.trace_add('write', self.recalc_results)
        self.var_Tu.trace_add('write', self.recalc_results)

    def plot_weld(self, fig1, ax1, group: str = "=", b: float = 0, d: float = 0, canvas=None):

        ax1.clear()

        ax1.axvline(color='black', linestyle=':')
        ax1.axhline(color='black', linestyle=':')
        ax1.set(xlabel='Y', ylabel='X')
        ax1.minorticks_on()
        spa = max(b, d) / 60
        self.ax1.relim()

        # calculate different properties based on weld group
        if group == '|':
            x1 = [0, 0]
            y1 = [-d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)

        elif group == '-':
            x1 = [-b/2, b/2]
            y1 = [0, 0]

            ax1.plot(x1, y1, color='navy', linewidth=3)

        elif group == '||':
            x1 = [-b/2, -b/2]
            y1 = [-d/2, d/2]

            x2 = [b/2, b/2]
            y2 = [-d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)

        elif group == '=':
            x1 = [-b/2, b/2]
            y1 = [-d/2, -d/2]

            x2 = [-b/2, b/2]
            y2 = [d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)

        elif group == '▯':
            x1 = [-b/2, -b/2]
            y1 = [-d/2, d/2]

            x2 = [b/2, b/2]
            y2 = [-d/2, d/2]

            x3 = [-b/2, b/2]
            y3 = [-d/2, -d/2]

            x4 = [-b/2, b/2]
            y4 = [d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)
            ax1.plot(x3, y3, color='navy', linewidth=3)
            ax1.plot(x4, y4, color='navy', linewidth=3)

        elif group == '⨅':
            x1 = [-b/2, -b/2]
            y1 = [-d/2, d/2]

            x2 = [b/2, b/2]
            y2 = [-d/2, d/2]

            x3 = [-b/2, b/2]
            y3 = [d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)
            ax1.plot(x3, y3, color='navy', linewidth=3)

        elif group == '╥':
            x1 = [-b/2, b/2]
            y1 = [d/2, d/2]

            x2 = [-spa, -spa]
            y2 = [-d/2, d/2]

            x3 = [spa, spa]
            y3 = [-d/2, d/2]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)
            ax1.plot(x3, y3, color='navy', linewidth=3)

        elif group == '╦':
            x1 = [-b/2, b/2]
            y1 = [d/2, d/2]

            x2 = [-b/2, -spa]
            y2 = [d/2 - 2*spa, d/2 - 2*spa]

            x3 = [-spa, -spa]
            y3 = [-d/2, d/2 - 2*spa]

            x4 = [spa, spa]
            y4 = [-d/2, d/2 - 2*spa]

            x5 = [spa, b/2]
            y5 = [d/2 - 2*spa, d/2 - 2*spa]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)
            ax1.plot(x3, y3, color='navy', linewidth=3)
            ax1.plot(x4, y4, color='navy', linewidth=3)
            ax1.plot(x5, y5, color='navy', linewidth=3)

        elif group == "⌶":
            x1 = [-b/2, b/2]
            y1 = [-d/2, -d/2]

            x2 = [-b/2, b/2]
            y2 = [d/2, d/2]

            x3 = [-b/2, -spa]
            y3 = [d/2 - 2*spa, d/2 - 2*spa]

            x4 = [spa, b/2]
            y4 = [d/2 - 2*spa, d/2 - 2*spa]

            x5 = [-b/2, -spa]
            y5 = [-d/2 + 2*spa, -d/2 + 2*spa]

            x6 = [spa, b/2]
            y6 = [-d/2 + 2*spa, -d/2 + 2*spa]

            x7 = [-spa, -spa]
            y7 = [-d/2 + 2*spa, d/2 - 2*spa]

            x8 = [spa, spa]
            y8 = [-d/2 + 2*spa, d/2 - 2*spa]

            ax1.plot(x1, y1, color='navy', linewidth=3)
            ax1.plot(x2, y2, color='navy', linewidth=3)
            ax1.plot(x3, y3, color='navy', linewidth=3)
            ax1.plot(x4, y4, color='navy', linewidth=3)
            ax1.plot(x5, y5, color='navy', linewidth=3)
            ax1.plot(x6, y6, color='navy', linewidth=3)
            ax1.plot(x7, y7, color='navy', linewidth=3)
            ax1.plot(x8, y8, color='navy', linewidth=3)

        # toolbar.update()
        canvas.draw()

    def reset_plot(self):
        self.tkwidget.destroy()
        self.draw_plot()
        self.recalc_full()
        # self.plot_weld(self.fig1, self.ax1, group=wg, b=b, d=d, tk_master=self.f_plot, works=works, canvas=self.canvas, toolbar=None)

    def set_results_NA(self):
        self.var_total_util.set("N/A")
        self.label_total_utilization.config(font="helvetica 9 bold", fg="red")
        self.var_phiMnx_util.set(f"N/A")
        self.var_phiMny_util.set(f"N/A")
        self.var_phiVnx_util.set(f"N/A")
        self.var_phiVny_util.set(f"N/A")
        self.var_phiAn_util.set(f"N/A")
        self.var_phiTn_util.set(f"N/A")

    def recalc_results(self, works=True, *args):

        ##########  WELD TYPE  ##########
        # take in variables
        wg = self.selected_weld_group.get()
        throat = self.sixteenths[self.selected_throat.get()]
        hss_thickness = self.sixteenths[self.selected_hss_thickness.get()]
        try:
            b = float(self.var_b.get())
            d = float(self.var_d.get())
        except ValueError:
            # print("Tried to get b or d but value was empty")
            pass

        # set isFlareBevel
        isFlareBevel = self.weldtype.get() == "fb"

        ##########  SECTION PROPERTIES & LOADS  ##########

        # create instance of weld group to pull section properties
        try:
            weld_group = WeldGroup(t=throat, group=wg, b=b, d=d,
                                   isFlareBevel=isFlareBevel, t_HSS=hss_thickness)
        except:
            self.set_results_NA()
            return

        # calculate section properties based on inputs
        phiMnx, phiMny, phiVnx, phiVny, phiAn, phiTn = weld_group.calculate_properties(
            group=wg, b=b, d=d, weld_strength=weld_group.weld_strength)

        # get all loading inputs
        Mux = abs(float(self.var_Mux.get())) if self.var_Mux.get() else 0
        Muy = abs(float(self.var_Muy.get())) if self.var_Muy.get() else 0
        Vux = abs(float(self.var_Vux.get())) if self.var_Vux.get() else 0
        Vuy = abs(float(self.var_Vuy.get())) if self.var_Vuy.get() else 0
        Au = abs(float(self.var_Au.get())) if self.var_Au.get() else 0
        Tu = abs(float(self.var_Tu.get())) if self.var_Tu.get() else 0

        # update moment unit variables to unit selection
        if self.units.get() == 'ft':
            self.units_moment.set('kip-ft')
            phiMnx /= 12
            phiMny /= 12
            phiTn /= 12
        else:
            self.units_moment.set('kip-in')

        # update variable for selected weld linear strength, section properties
        self.text_weld_strength.set(f"{weld_group.weld_strength:.2f} kip/in")
        try:
            self.var_phiMnx.set(f"{phiMnx:.1f}")
            self.var_phiMny.set(f"{phiMny:.1f}")
            self.var_phiVnx.set(f"{phiVnx:.1f}")
            self.var_phiVny.set(f"{phiVny:.1f}")
            self.var_phiAn.set(f"{phiAn:.1f}")
            self.var_phiTn.set(f"{phiTn:.1f}")
        except AttributeError:
            print("Strength variables selected but do not exist")

        ##########  UTILIZATION   ##########
        # First, need to determine whether to even run calcs. The program should
        # not run calcs if any input is > 0 when the associated property is zero.
        # In that case, set 'works' to False and the total output will be 'N/A'

        # for each section property: check for the case mentioned above,
        # calculate utilization, draw utilization
        # Mnx
        if works:
            if (phiMnx == 0) and (Mux != 0):  # force inputted but zero for the section property
                self.var_phiMnx_util.set("N/A")
                works = False
            else:
                try:
                    util_phiMnx = Mux / phiMnx * 100  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiMnx = 0
                    # delete for deployment
                    # print("phiMnx is 0 and force provided is 0")
                self.var_phiMnx_util.set(f"{util_phiMnx:.1f} %")

            # Mny
            if (phiMny == 0) and (Muy != 0):  # force inputted but zero for the section property
                self.var_phiMny_util.set("N/A")
                works = False
            else:
                try:
                    util_phiMny = Muy / phiMny * 100  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiMny = 0
                    # delete for deployment
                    # print("phiMny is 0 and force provided is 0")
                self.var_phiMny_util.set(f"{util_phiMny:.1f} %")

            # Vnx
            if (phiVnx == 0) and (Vux != 0):  # force inputted but zero for the section property
                self.var_phiVnx_util.set("N/A")
                works = False
            else:
                try:
                    util_phiVnx = Vux / phiVnx * 100  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiVnx = 0
                    # delete for deployment
                    # print("phiVnx is 0 and force provided is 0")
                self.var_phiVnx_util.set(f"{util_phiVnx:.1f} %")

            # Vny
            if (phiVny == 0) and (Vuy != 0):  # force inputted but zero for the section property
                self.var_phiVny_util.set("N/A")
                works = False
            else:
                try:
                    util_phiVny = Vuy / phiVny * 100  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiVny = 0
                    # delete for deployment
                    # print("phiVny is 0 and force provided is 0")
                self.var_phiVny_util.set(f"{util_phiVny:.1f} %")

            # An
            if (phiAn == 0) and (Au != 0):  # force inputted but zero for the section property
                self.var_phiAn_util.set("N/A")
                works = False
            else:
                try:
                    util_phiAn = Au / phiAn * 100  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiAn = 0
                    # delete for deployment
                    # print("An is 0 and force provided is 0")
                self.var_phiAn_util.set(f"{util_phiAn:.1f} %")

            # Tn
            if (phiTn == 0) and (Tu != 0):  # force inputted but zero for the section property
                self.var_phiTn_util.set("N/A")
                works = False
            else:
                try:
                    util_phiTn = (Tu / phiTn * 100)  # individual utilization
                except ZeroDivisionError:  # in case we get a 0/0
                    util_phiTn = 0
                    # delete for deployment
                    # print("Tn is 0 and force provided is 0")
                self.var_phiTn_util.set(f"{util_phiTn:.1f} %")

        if works:
            # calculate total utilization as sum of individual utilizations
            total_ratio = util_phiMnx + util_phiMny + \
                util_phiVnx + util_phiVny + util_phiAn + util_phiTn

            # draw utilization value in different colors depending on percentage
            if total_ratio <= 90:  # yellow text for percentages above 90
                self.var_total_util.set(f"{total_ratio:.1f} %")
                self.label_total_utilization.config(
                    font="helvetica 9 bold", fg="green")

            elif total_ratio <= 100:  # red text for percentages above 100
                self.var_total_util.set(f"{total_ratio:.1f} %")
                self.label_total_utilization.config(
                    font="helvetica 9 bold", fg="orange")

            else:  # green text when weld is ok
                self.var_total_util.set(f"{total_ratio:.1f} %")
                self.label_total_utilization.config(
                    font="helvetica 9 bold", fg="red")

        else:
            self.set_results_NA()

    def recalc_full(self, *args):  # *args is necessary to trace variables with function
        """
        Take in inputs from GUI, calculate outputs, draw outputs.
        """
        works = True
        wg = self.selected_weld_group.get()
        try:
            b = float(self.var_b.get())
            d = float(self.var_d.get())
        except ValueError:
            b = 0
            d = 0
            works = False
            pass

        # plot preview of weld group
        self.plot_weld(self.fig1, self.ax1, group=wg, b=b, d=d,
                       canvas=self.canvas)
        self.recalc_results(works=works)

    def print_summary(self, wg, weldtype, throat, weld_strength, phiMnx, phiMny,
                      phiVnx, phiVny, phiAn, phiTn, Mux, Muy, Vux, Vuy, Au, Tu, isFlareBevel, hss_thickness):

        print(f"weld group is {wg}")
        print(f"weld type is {weldtype.get()}")
        print(f"throat is {throat}")
        print(f"weld strength is {weld_strength}")
        print(f"phiMnx = {phiMnx:.1f}")
        print(f"phiMny = {phiMny:.1f}")
        print(f"phiVnx = {phiVnx:.1f}")
        print(f"phiVny = {phiVny:.1f}")
        print(f"phiAn = {phiAn:.1f}")
        print(f"phiTn = {phiTn:.1f}")
        print(f"Mux = {Mux}")
        print(f"Muy = {Muy}")
        print(f"Vux = {Vux}")
        print(f"Vuy = {Vuy}")
        print(f"Au = {Au}")
        print(f"Tu = {Tu}")
        print(f"isFlareBevel is {isFlareBevel}")
        print(f"HSS thickness is {hss_thickness}")
        print()
