# Copyright 2025 Joe Bears
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from numpy import isclose

from structuraltools import aisc, materials, unit

from structuraltools.aisc import chapter_F


def test_eq_F2_1():
    string, M_p = chapter_F.eq_F2_1(
        F_y=50*unit.ksi,
        Z_x=20*unit.inch**3,
        return_string=True)
    assert isclose(M_p, 1000/12*unit.kipft)
    assert M_p.units == "kipft"
    assert string == r"M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 20\ \mathrm{in}^{3} &= 83.333\ \mathrm{kipft}"

def test_eq_F2_2():
    string, M_ltb = chapter_F.eq_F2_2(
        C_b=1,
        M_p=83*unit.kipft,
        F_y=50*unit.ksi,
        S_x=15*unit.inch**3,
        L_b=5*unit.ft,
        L_p=3*unit.ft,
        L_r=10*unit.ft,
        return_string=True)
    assert isclose(M_ltb, 71.78571429*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= 1 \cdot \left(83\ \mathrm{kipft} - \left(83\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 15\ \mathrm{in}^{3}\right) \cdot \left(\frac{5\ \mathrm{ft} - 3\ \mathrm{ft}}{10\ \mathrm{ft} - 3\ \mathrm{ft}}\right)\right)
    \\
    &= 71.786\ \mathrm{kipft}"""

def test_eq_F2_3():
    string, M_ltb = chapter_F.eq_F2_3(
        F_cr=17*unit.ksi,
        S_x=25.4*unit.inch**3,
        return_string=True)
    assert isclose(M_ltb, 35.98333333*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"M_{ltb} &= F_{cr} \cdot S_x = 17\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3} &= 35.983\ \mathrm{kipft}"

def test_eq_F2_4():
    string, F_cr = chapter_F.eq_F2_4(
        C_b=1,
        E=29000*unit.ksi,
        L_b=15*unit.ft,
        r_ts=1.04*unit.inch,
        J=0.293*unit.inch**4,
        c=1,
        S_x=25.4*unit.inch**3,
        h_o=11.9*unit.inch,
        return_string=True)
    assert isclose(F_cr, 17.26466339*unit.ksi, atol=1e-8*unit.ksi)
    assert F_cr.units == "ksi"
    assert string == r"""F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
    \\
    &= \frac{1 \cdot \pi^2 \cdot 29000\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
    \\
    &= 17.265\ \mathrm{ksi}"""

def test_eq_F2_5():
    string, L_p = chapter_F.eq_F2_5(
        r_y=0.848*unit.inch,
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        return_string=True)
    assert isclose(L_p, 2.995306513*unit.ft, atol=1e-8*unit.ft)
    assert L_p.units == "ft"
    assert string == r"L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}"

def test_eq_F2_6():
    string, L_r = chapter_F.eq_F2_6(
        r_ts=1.04*unit.inch,
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        J=0.293*unit.inch**4,
        c=1,
        S_x=25.4*unit.inch**3,
        h_o=11.9*unit.inch,
        return_string=True)
    assert isclose(L_r, 9.132623412*unit.ft, atol=1e-9*unit.ft)
    assert L_r.units == "ft"
    assert string == r"""L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot 1.04\ \mathrm{in} \frac{29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
    \\
    &= 9.133\ \mathrm{ft}"""

def test_eq_F2_8b():
    string, c = chapter_F.eq_F2_8b(
        h_o=9.56*unit.inch,
        I_y=2.8*unit.inch**4,
        C_w=56.9*unit.inch**6,
        return_string=True)
    assert isclose(c, 1.060353756, atol=1e-9)
    assert isinstance(c, float)
    assert string == r"c &= \frac{h_o}{2} \cdot \sqrt{\frac{I_y}{C_w}} = \frac{9.56\ \mathrm{in}}{2} \cdot \sqrt{\frac{2.8\ \mathrm{in}^{4}}{56.9\ \mathrm{in}^{6}}} &= 1.06"

def test_sec_F2_1():
    shape = aisc.WideFlange("W12X22", materials.Steel("A992"))
    string, M_p = chapter_F.sec_F2_1(shape, return_string=True)
    assert isclose(M_p, 122.0833333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_p.units == "kipft"
    assert string == r"""\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.083\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_plastic_WideFlange():
    shape = aisc.WideFlange("W12X22", materials.Steel("A992"))
    M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=2*unit.ft,
        M_p=M_p,
        C_b=1,
        return_string=True)
    assert isclose(M_ltb, 122.0833333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 2\ \mathrm{ft} \leq 2.995\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= M_p = 122.083\ \mathrm{kipft} &= 122.083\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_inelastic_WideFlange():
    shape = aisc.WideFlange("W12X22", materials.Steel("A992"))
    M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=7*unit.ft,
        M_p=M_p,
        C_b=1,
        return_string=True)
    assert isclose(M_ltb, 90.7*unit.kipft, atol=1*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot 1.04\ \mathrm{in} \frac{29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
    \\
    &= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow 2.995\ \mathrm{ft} < 7\ \mathrm{ft} \leq 9.133\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= 1 \cdot \left(122.083\ \mathrm{kipft} - \left(122.083\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \left(\frac{7\ \mathrm{ft} - 2.995\ \mathrm{ft}}{9.133\ \mathrm{ft} - 2.995\ \mathrm{ft}}\right)\right)
    \\
    &= 90.763\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_elastic_WideFlange():
    shape = aisc.WideFlange("W12X22", materials.Steel("A992"))
    M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=15*unit.ft,
        M_p=M_p,
        C_b=1,
        return_string=True)
    assert isclose(M_ltb, 36.5*unit.kipft, atol=1*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot 1.04\ \mathrm{in} \frac{29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
    \\
    &= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow 15\ \mathrm{ft} > 9.133\ \mathrm{ft}\right):
        \\[10pt]
        F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
    \\
    &= \frac{1 \cdot \pi^2 \cdot 29000\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
    \\
    &= 17.265\ \mathrm{ksi}
        \\[10pt]
        M_{ltb} &= F_{cr} \cdot S_x = 17.265\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3} &= 36.544\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2():
    shape = aisc.WideFlange("W12X22", materials.Steel("A992"))
    string, M_n = chapter_F.sec_F2(
        shape=shape,
        L_b=7*unit.ft,
        C_b=1,
        return_string=True)
    assert isclose(M_n, 90.7*unit.kipft, atol=0.1*unit.kipft)
    assert M_n.units == "kipft"
    assert string == r"""#### Plastic Moment Capacity
$$ \begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.083\ \mathrm{kipft}
\end{aligned} $$
<br/>
#### Lateral-Torsional Buckling Moment Capacity
$$ \begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot 1.04\ \mathrm{in} \frac{29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
    \\
    &= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow 2.995\ \mathrm{ft} < 7\ \mathrm{ft} \leq 9.133\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= 1 \cdot \left(122.083\ \mathrm{kipft} - \left(122.083\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \left(\frac{7\ \mathrm{ft} - 2.995\ \mathrm{ft}}{9.133\ \mathrm{ft} - 2.995\ \mathrm{ft}}\right)\right)
    \\
    &= 90.763\ \mathrm{kipft}
\end{aligned} $$
<br/>
#### Nominal Moment Capacity
$$ \begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(122.083\ \mathrm{kipft},\ 90.763\ \mathrm{kipft}\right) &= 90.763\ \mathrm{kipft}
\end{aligned} $$"""

def test_eq_F3_1():
    string, M_flb = chapter_F.eq_F3_1(
        M_p=122*unit.kipft,
        F_y=50*unit.ksi,
        S_x=25.4*unit.inch**3,
        lamb_f=15,
        lamb_pf=9,
        lamb_rf=24,
        return_string=True)
    assert isclose(M_flb, 102.8333333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_flb.units == "kipft"
    assert string == r"""M_{flb} &= M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
    \\
    &= 122\ \mathrm{kipft} - \left(122\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \left(\frac{15 - 9}{24 - 9}\right)
    \\
    &= 102.833\ \mathrm{kipft}"""

def test_eq_F3_2():
    string, M_flb = chapter_F.eq_F3_2(
        E=29000*unit.ksi,
        k_c=0.5,
        S_x=25*unit.inch**3,
        lamb_f=30,
        return_string=True)
    assert isclose(M_flb, 30.20833333*unit.kipft, atol=1e-8*unit.kipft)
    assert M_flb.units == "kipft"
    assert string == r"M_{flb} &= \frac{0.9 \cdot E \cdot k_c \cdot S_x}{\lambda_f^2} = \frac{0.9 \cdot 29000\ \mathrm{ksi} \cdot 0.5 \cdot 25\ \mathrm{in}^{3}}{30^2} &= 30.208\ \mathrm{kipft}"

def test_eq_F3_2a_low():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=250, return_string=True)
    assert k_c == 0.35
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{250}}\right),\ 0.76\right) &= 0.35"

def test_eq_F3_2a_calculated():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=100, return_string=True)
    assert isclose(k_c, 0.4)
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{100}}\right),\ 0.76\right) &= 0.4"

def test_eq_F3_2a_high():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=20, return_string=True)
    assert k_c == 0.76
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{20}}\right),\ 0.76\right) &= 0.76"
