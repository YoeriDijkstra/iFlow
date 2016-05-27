dpi = 120           # dpi for visualisation
savedpi = 150       # dpi for saving (only relevant for non-vector images)
wunit = 10./2.54    # single width unit (inch)
hunit = 7/2.54      # single height unit (inch)
fontsize = 11       # font size for title and axis labels
fontsize2 = 9      # font size for tick labels and legends
fontfamily = 'sans-serif'

names = {
    'zeta': '$\zeta$ total',
    'zeta0': '$\zeta^0$',
    'zeta1': '$\zeta^1$',
    'zeta2': '$\zeta^2$',
    'zeta3': '$\zeta^3$',
    'zeta4': '$\zeta^4$',
    'zeta5': '$\zeta^5$',
    'zeta6': '$\zeta^6$',
    'u': '$u$ total',
    'u0': '$u^0$',
    'u1': '$u^1$',
    'u2': '$u^2$',
    'u3': '$u^3$',
    'u4': '$u^4$',
    'u5': '$u^5$',
    'u6': '$u^6$',
    'w0': '$w^0$',
    'w1': '$w^1$',
    'w2': '$w^2$',
    'w3': '$w^3$',
    'w4': '$w^4$',
    'w5': '$w^5$',
    'w6': '$w^6$',
    's0': '$s^0$',
    's1': '$s^1$',
    's2': '$s^2$',
    's3': '$s^3$',
    'c0': '$c^0$',
    'c1': '$c^1$',
    'c2': '$c^2$',
    'c3': '$c^3$',
    'Av': '$A_v^0$',
    'Av1': '$A_v^1$',
    'Av2': '$A_v^2$',
    'Av3': '$A_v^3$',
    'Av4': '$A_v^4$',
    'Av5': '$A_v^5$',
    'Av6': '$A_v^6$',
    'x': 'x',
    'z': 'z',
    'f': 'f',
    'baroc': 'Baroclinic',
    'adv': 'Advection',
    'stokes': 'Tidal return flow',
    'mixing': 'Mixing',
    'tide': 'Tide',
    'river': 'River',
    'nostress': 'No-stress',
    'densitydrift': 'Density-induced return flow',
    'R': 'R'}

units = {
    'zeta': 'm',
    'zeta0': 'm',
    'zeta1': 'm',
    'zeta2': 'm',
    'zeta3': 'm',
    'zeta4': 'm',
    'zeta5': 'm',
    'zeta6': 'm',
    'u': 'm/s',
    'u0': 'm/s',
    'u1': 'm/s',
    'u2': 'm/s',
    'u3': 'm/s',
    'u4': 'm/s',
    'u5': 'm/s',
    'u6': 'm/s',
    'w0': 'm/s',
    'w1': 'm/s',
    'w2': 'm/s',
    'w3': 'm/s',
    'w4': 'm/s',
    'w5': 'm/s',
    'w6': 'm/s',
    's0': 'psu',
    's1': 'psu',
    's2': 'psu',
    's3': 'psu',
    'c0': 'mg/l',
    'c1': 'mg/l',
    'c2': 'mg/l',
    'c3': 'mg/l',
    'Av': '$m^2/s$',
    'Av1': '$m^2/s$',
    'Av2': '$m^2/s$',
    'Av3': '$m^2/s$',
    'Av4': '$m^2/s$',
    'Av5': '$m^2/s$',
    'Av6': '$m^2/s$',
    'x': 'km',
    'z': 'm',
    'f': '',
    'phase': '',
    'R': 'm'}

conversion = {
    'x': 1/1000.
}