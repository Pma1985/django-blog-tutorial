from django.shortcuts import render
from .forms import InputForm
from math import sin, tan

def As(b,d,fc,fy,Mu):
    phi=0.9
    Ru=Mu/(phi*b*d**2)*1000000
    rho_req=0.85*fc/fy*(1-(1-2*Ru/(0.85*fc))**0.5)
    rho_min=max(1.4/fy,0.25*fc**0.5/fy)
    beta_1=0.85-0.05*(fc-27.6)/6.9
    if beta_1<0.65:
        beta_1=0.65
    if beta_1>0.85:
        beta_1=0.85
    rho_max=0.43*0.85*fc/fy*beta_1
    rho=max(min(rho_min,1.33*rho_req),rho_req)
    if rho<=rho_max:
        return round(rho*b*d,0)
    else:
        return "Increase beam section"
def Vstotal(b,d,fc,fy,Vu):
    Vc=2*fc**0.5*b*d
    phi=0.85
    Vsreq=(Vu*1000-phi*Vc)/phi
    return round(Vsreq/(fy*d))


def compute(request):
    if request.method == 'POST':
        form=InputForm(data=request.POST,auto_id="%s")
        if form.is_valid():
            fc = form.cleaned_data['fc']
            fy = form.cleaned_data['fy']
            gamma = form.cleaned_data['gamma']
            #d = form.cleaned_data['d']

            Cx = form.cleaned_data['Cx']
            Cy = form.cleaned_data['Cy']

            dp = form.cleaned_data['dp']
            S = form.cleaned_data['S']
            H = form.cleaned_data['H']
            c = form.cleaned_data['c']
            e = form.cleaned_data['e']
            t = form.cleaned_data['t']
            Pc = form.cleaned_data['Pc']
            Pt = form.cleaned_data['Pt']

            #Fxd = form.cleaned_data['Fxd']
            Fzd = form.cleaned_data['Fzd']
            Myd = form.cleaned_data['Myd']
            Mxd = form.cleaned_data['Mxd']
            #Fxl = form.cleaned_data['Fxl']
            Fzl = form.cleaned_data['Fzl']
            Myl = form.cleaned_data['Myl']
            Mxl = form.cleaned_data['Mxl']
            #Fxw = form.cleaned_data['Fxw']
            Fzw = form.cleaned_data['Fzw']
            Myw = form.cleaned_data['Myw']
            Mxw = form.cleaned_data['Mxw']
            #Fxe = form.cleaned_data['Fxe']
            Fze = form.cleaned_data['Fze']
            Mye = form.cleaned_data['Mye']
            Mxe = form.cleaned_data['Mxe']

            # Pile Cap Dimensions
            L = round(sin(1.047)*S+dp+2*e,1)
            B = S+dp+2*e
            w1 = dp+2*e
            w2 = dp+2*e
            Ldiag = round(((L-w1)**2+(B-w2)**2)**0.5,1)
            d = H - c
            So = S*(3.0)**0.5/2
            Y1 = 2*So/3
            Y2 = So/3
            ay = round(Y1-Cy/2+t,1)
            X = 0.5*(S-Cx)
            m = Y2-Cy/2
            ax = round(((X+m/tan(1.047))*sin(1.047))+t,1)
            radio_x = round(ax/d,3)
            radio_y = round(ay/d,3)
            Bs = 2*(Cx+Cy)
            A = dp/2+e


            # Pile capacity check
            Acap = L*B-sin(1.047)*Ldiag**2/2
            Gc = gamma*(H*0.001)*(Acap*0.000001)
            Gc = round(Gc,2)

            Fv1 = 1.0 * (Fzd + Gc) + 1.0 * Fzl
            My1 = Myd + Myl
            Mx1 = Mxd + Mxl
            x1 = 0.0; x2 = -0.5 * S; x3 = 0.5 *S
            y1 = 0.578 * S; y2 = -0.288 * S; y3 = -0.288 * S
            sum_xx = x1**2+x2**2+x3**2
            sum_yy = y1**2+y2**2+y3**2
            def Rp(F,Mx,My,n,x,y):
                return F/n+1000*Mx*y/sum_yy+1000*My*x/sum_xx
            Rp_1 = round(Rp(Fv1, Mx1, My1, 3, x1, y1))
            Rp_2 = round(Rp(Fv1, Mx1, My1, 3, x2, y2))
            Rp_3 = round(Rp(Fv1, Mx1, My1, 3, x3, y3))

            if Rp_1 <= Pc and Rp_1>=Pt and Rp_2 <= Pc and Rp_2>=Pt and Rp_3 <= Pc and Rp_3>=Pt:
                VS1 = 'orange'
                result1 = 'Satisfied'
            else:
                VS1 = "red"
                result1 = "Failed"
            # Pile reaction
            #Cx1 = 1.4 * Fxd
            Cz1 = 1.4 * Fzd
            Czg1 = 1.4 * (Fzd + Gc)
            Cmy1 = 1.4 * Myd
            Cmx1 = 1.4 * Mxd

            #Cx2 = 1.2 * Fxd + 1.6 * Fxl
            Cz2 = 1.2 * Fzd + 1.6 * Fzl
            Czg2 = 1.2 * (Fzd + Gc) + 1.6 * Fzl
            Cmy2 = 1.2 * Myd + 1.6 * Myl
            Cmx2 = 1.2 * Mxd + 1.6 * Mxl

            #Cx3 = 1.2 * Fxd + 1.6 * Fxw + 1.0 * Fxl
            Cz3 = 1.2 * Fzd + 1.6 * Fzw + 1.0 * Fzl
            Czg3 = 1.2 * (Fzd + Gc) + 1.6 * Fzw + 1.0 * Fzl
            Cmy3 = 1.2 * Myd + 1.6 * Myw + 1.0 * Myl
            Cmx3 = 1.2 * Mxd + 1.6 * Mxw + 1.0 * Mxl

            #Cx4 = 1.2 * Fxd + 1.0 * Fxe + 1.0 * Fxl
            Cz4 = 1.2 * Fzd + 1.0 * Fze + 1.0 * Fzl
            Czg4 = 1.2 * (Fzd + Gc) + 1.0 * Fze + 1.0 * Fzl
            Cmy4 = 1.2 * Myd + 1.0 * Mye + 1.0 * Myl
            Cmx4 = 1.2 * Mxd + 1.0 * Mxe + 1.0 * Mxl

            #Cx5 = 0.9 * Fxd + 1.6 * Fxw
            Cz5 = 0.9 * Fzd + 1.6 * Fzw
            Czg5 = 0.9 * (Fzd + Gc) + 1.6 * Fzw
            Cmy5 = 0.9 * Myd + 1.6 * Myw
            Cmx5 = 0.9 * Mxd + 1.6 * Mxw

            #Cx6 = 0.9 * Fxd + 1.6 * Fxe
            Cz6 = 0.9 * Fzd + 1.6 * Fze
            Czg6 = 0.9 * (Fzd + Gc) + 1.6 * Fze
            Cmy6 = 0.9 * Myd + 1.6 * Mye
            Cmx6 = 0.9 * Mxd + 1.6 * Mxe

            Rp11 = round(Rp(Czg1, Cmx1, Cmy1, 3, x1, y1), 1)
            Rp21 = round(Rp(Czg1, Cmx1, Cmy1, 3, x2, y2), 1)
            Rp31 = round(Rp(Czg1, Cmx1, Cmy1, 3, x3, y3), 1)
            Rp12 = round(Rp(Czg2, Cmx2, Cmy2, 3, x1, y1), 1)
            Rp22 = round(Rp(Czg2, Cmx2, Cmy2, 3, x2, y2), 1)
            Rp32 = round(Rp(Czg2, Cmx2, Cmy2, 3, x3, y3), 1)
            Rp13 = round(Rp(Czg3, Cmx3, Cmy3, 3, x1, y1), 1)
            Rp23 = round(Rp(Czg3, Cmx3, Cmy3, 3, x2, y2), 1)
            Rp33 = round(Rp(Czg3, Cmx3, Cmy3, 3, x3, y3), 1)
            Rp14 = round(Rp(Czg4, Cmx4, Cmy4, 3, x1, y1), 1)
            Rp24 = round(Rp(Czg4, Cmx4, Cmy4, 3, x2, y2), 1)
            Rp34 = round(Rp(Czg4, Cmx4, Cmy4, 3, x3, y3), 1)
            Rp15 = round(Rp(Czg5, Cmx5, Cmy5, 3, x1, y1), 1)
            Rp25 = round(Rp(Czg5, Cmx5, Cmy5, 3, x2, y2), 1)
            Rp35 = round(Rp(Czg5, Cmx5, Cmy5, 3, x3, y3), 1)
            Rp16 = round(Rp(Czg6, Cmx6, Cmy6, 3, x1, y1), 1)
            Rp26 = round(Rp(Czg6, Cmx6, Cmy6, 3, x2, y2), 1)
            Rp36 = round(Rp(Czg6, Cmx6, Cmy6, 3, x3, y3), 1)

            # Two way shear design
            phiVc = round(0.85 *d/max(ax,ay) * (1+2*d/(Cx+Cy)) * (0.17 * (fc) ** 0.5 * Bs * d) * 0.001, 2)

            VV1 = '%.2f' % (Czg1 / phiVc)
            if (Czg1 / phiVc) < 1:
                vs1 = "Pass"
                co_vs1 = "orange"
            else:
                vs1 = "Fail"
                co_vs1 = "red"
            VV2 = '%.2f' % (Czg2 / phiVc)
            if (Czg2 / phiVc) < 1:
                vs2 = "Pass"
                co_vs2 = "orange"
            else:
                vs2 = "Fail"
                co_vs2 = "red"
            VV3 = '%.2f' % (Czg3 / phiVc)
            if (Czg3 / phiVc) < 1:
                vs3 = "Pass"
                co_vs3 = "orange"
            else:
                vs3 = "Fail"
                co_vs3 = "red"
            VV4 = '%.2f' % (Czg4 / phiVc)
            if (Czg4 / phiVc) < 1:
                vs4 = "Pass"
                co_vs4 = "orange"
            else:
                vs4 = "Fail"
                co_vs4 = "red"
            VV5 = '%.2f' % (Czg5 / phiVc)
            if (Czg5 / phiVc) < 1:
                vs5 = "Pass"
                co_vs5 = "orange"
            else:
                vs5 = "Fail"
                co_vs5 = "red"
            VV6 = '%.2f' % (Czg6 / phiVc)
            if (Czg6 / phiVc) < 1:
                vs6 = "Pass"
                co_vs6 = "orange"
            else:
                vs6 = "Fail"
                co_vs6 = "red"

            # One Way Shear
            if radio_x >= 1:
                Lcx = (0.5 * (X + A + (A + m) / tan(1.047)-d/sin(1.047)) * tan(1.047) + A) / sin(1.047)
                phiVc_x = round(0.85 * (0.17 * (fc) ** 0.5 * Lcx * d) * 0.001, 1)
                check1 = "Concrete shear strength for one way wide beam action:"
                check2 = "$\phi V_c=0.85\cdot(0.17\sqrt{f'_c} \cdot L_{cx}\cdot d)=$"+str(phiVc_x)+"kN"
                check3 = "$L_{cx}=(0.5(X+A+(A+m)ctg(\pi/3)-d/sin(\pi/3))*tan(\pi/3)+A)/sin(\pi/3)=$"+str(round(Lcx))+"mm"
            else:
                kx = min(round(d/ax * (3.5-2.5*ax/d),2),10)
                Lcx = (0.5 * (X + A + (A + m) / tan(1.047)) * tan(1.047) + A) / sin(1.047)
                phiVc_x = round(0.85 * kx * (0.17 * (fc) ** 0.5 * Lcx * d) * 0.001, 1)
                check1 = "Concrete shear strength for one way deep beam action:"
                check2 = "$\phi V_c=0.85k\cdot(0.17\sqrt{f'_c} \cdot L_{cx}\cdot d)=$"+str(phiVc_x)+"kN;"+"$\quad k=\cfrac{d}{a}\cdot (3.5-2.5 \cfrac {a}{d})$"
                check3 = "$L_{cx}=(0.5(X+A+(A+m)ctg(\pi/3))*tan(\pi/3)+A)/sin(\pi/3)=$"+str(round(Lcx))+"mm"
            Vux1 = max(Rp21, Rp31)
            Vux2 = max(Rp22, Rp32)
            Vux3 = max(Rp23, Rp33)
            Vux4 = max(Rp24, Rp34)
            Vux5 = max(Rp25, Rp35)
            Vux6 = max(Rp26, Rp36)
            V1 = '%.2f' % (Vux1 / phiVc_x)
            if (Vux1 / phiVc_x) < 1:
                s1 = "Pass"
                co_s1 = "orange"
            else:
                s1 = "Fail"
                co_s1 = "red"
            V2 = '%.2f' % (Vux2 / phiVc_x)
            if (Vux2 / phiVc_x) < 1:
                s2 = "Pass"
                co_s2 = "orange"
            else:
                s2 = "Fail"
                co_s2 = "red"
            V3 = '%.2f' % (Vux3 / phiVc_x)
            if (Vux3 / phiVc_x) < 1:
                s3 = "Pass"
                co_s3 = "orange"
            else:
                s3 = "Fail"
                co_s3 = "red"
            V4 = '%.2f' % (Vux4 / phiVc_x)
            if (Vux4 / phiVc_x) < 1:
                s4 = "Pass"
                co_s4 = "orange"
            else:
                s4 = "Fail"
                co_s4 = "red"
            V5 = '%.2f' % (Vux5 / phiVc_x)
            if (Vux5 / phiVc_x) < 1:
                s5 = "Pass"
                co_s5 = "orange"
            else:
                s5 = "Fail"
                co_s5 = "red"
            V6 = '%.2f' % (Vux6 / phiVc_x)
            if (Vux6 / phiVc_x) < 1:
                s6 = "Pass"
                co_s6 = "orange"
            else:
                s6 = "Fail"
                co_s6 = "red"
            if radio_y >= 1:
                Lcy = 2 * A + 2 * ((ay - t - d) + A) / tan(1.047)
                phiVc_y = round(0.85 * (0.17 * (fc) ** 0.5 * Lcy * d) * 0.001, 1)
                check4 = "Concrete shear strength for one way wide beam action:"
                check5 = "$\phi V_c=0.85\cdot(0.17\sqrt{f'_c} \cdot L_{cx}\cdot d)=$"+str(phiVc_y)+"kN"
                check6 = "$L_{cx}=2A+2((a_y-t-d)+A)/tan(\pi/3)=$"+str(round(Lcy))+"mm"
            else:
                ky = min(round(d/ax * (3.5-2.5*ax/d),2),10)
                Lcy = 2 * A + 2 * ((ay - t - d) + A) / tan(1.047)
                phiVc_y = round(0.85 * ky * (0.17 * (fc) ** 0.5 * Lcy * d) * 0.001, 1)
                check4 = "Concrete shear strength for one way deep beam action:"
                check5 = "$\phi V_c=0.85k\cdot(0.17\sqrt{f'_c} \cdot L_{cx}\cdot d)=$"+str(phiVc_y)+"kN;"+"$\quad k=\cfrac{d}{a}\cdot (3.5-2.5 \cfrac {a}{d})$"
                check6 = "$L_{cx}=2A+2((a_y-t-d)+A)/tan(\pi/3)==$"+str(round(Lcy))+"mm"
            VVV1 = '%.2f' % (Rp11 / phiVc_y)
            if (Rp11 / phiVc_y) < 1:
                vvs1 = "Pass"
                co_vvs1 = "orange"
            else:
                vvs1 = "Fail"
                co_vvs1 = "red"
            VVV2 = '%.2f' % (Rp12 / phiVc_y)
            if (Rp12 / phiVc_y) < 1:
                vvs2 = "Pass"
                co_vvs2 = "orange"
            else:
                vvs2 = "Fail"
                co_vvs2 = "red"
            VVV3 = '%.2f' % (Rp13 / phiVc_y)
            if (Rp13 / phiVc_y) < 1:
                vvs3 = "Pass"
                co_vvs3 = "orange"
            else:
                vvs3 = "Fail"
                co_vvs3 = "red"
            VVV4 = '%.2f' % (Rp14 / phiVc_y)
            if (Rp14 / phiVc_y) < 1:
                vvs4 = "Pass"
                co_vvs4 = "orange"
            else:
                vvs4 = "Fail"
                co_vvs4 = "red"
            VVV5 = '%.2f' % (Rp15 / phiVc_y)
            if (Rp15 / phiVc_y) < 1:
                vvs5 = "Pass"
                co_vvs5 = "orange"
            else:
                vvs5 = "Fail"
                co_vvs5 = "red"
            VVV6 = '%.2f' % (Rp16 / phiVc_y)
            if (Rp16 / phiVc_y) < 1:
                vvs6 = "Pass"
                co_vvs6 = "orange"
            else:
                vvs6 = "Fail"
                co_vvs6 = "red"

            # Bending Reinforcement
            def As(M,B):
                rho_min = 0.0018
                As_min=rho_min*B*H
                R = M * 10 ** 6 / (0.9 * B * d ** 2)
                rho_req = 0.85 * fc / fy * (1 - (1 - 2 * R / (0.85 * fc)) ** 0.5)
                As_req = rho_req * B * (H-c)
                return max(As_min,As_req)

            BX = round(A * (1.5 + 0.5 * tan(1.047))/sin(1.047), 1)
            Mux1 = round(max(Rp21,Rp31) * ax * 0.001, 1)
            Mux2 = round(max(Rp22,Rp32) * ax * 0.001, 1)
            Mux3 = round(max(Rp23,Rp33) * ax * 0.001, 1)
            Mux4 = round(max(Rp24,Rp34) * ax * 0.001, 1)
            Mux5 = round(max(Rp25,Rp35) * ax * 0.001, 1)
            Mux6 = round(max(Rp26,Rp36) * ax * 0.001, 1)

            Asx1 = '%.0f' % float(As(Mux1, BX))
            Asx2 = '%.0f' % float(As(Mux2, BX))
            Asx3 = '%.0f' % float(As(Mux3, BX))
            Asx4 = '%.0f' % float(As(Mux4, BX))
            Asx5 = '%.0f' % float(As(Mux5, BX))
            Asx6 = '%.0f' % float(As(Mux6, BX))

            BY = round(2*A*(1+1/tan(1.047)),1)
            Muy1 = round(Rp11*ay*0.001,1)
            Muy2 = round(Rp12 * ay * 0.001, 1)
            Muy3 = round(Rp13 * ay * 0.001, 1)
            Muy4 = round(Rp14 * ay * 0.001, 1)
            Muy5 = round(Rp15 * ay * 0.001, 1)
            Muy6 = round(Rp16 * ay * 0.001, 1)


            Asy1 = '%.0f' % float(As(Muy1,BY))
            Asy2 = '%.0f' % float(As(Muy2,BY))
            Asy3 = '%.0f' % float(As(Muy3,BY))
            Asy4 = '%.0f' % float(As(Muy4,BY))
            Asy5 = '%.0f' % float(As(Muy5,BY))
            Asy6 = '%.0f' % float(As(Muy6,BY))

            Czg1 = round(Czg1,1)
            Czg2 = round(Czg2, 1)
            Czg3 = round(Czg3, 1)
            Czg4 = round(Czg4, 1)
            Czg5 = round(Czg5, 1)
            Czg6 = round(Czg6, 1)


            return render(request, 'pile_cap_3.html', {'form': form,'Gc':Gc,'Fv1':Fv1,'My1':My1,'Mx1':Mx1,
                                                       'L':L,'B':B,'w1':w1,'w2':w2,'Ldiag':Ldiag,'d':d,'ax':ax,'ay':ay,'radio_x':radio_x,'radio_y':radio_y,
                                                       'Rp_1':Rp_1,'Rp_2':Rp_2,'Rp_3':Rp_3,'VS1':VS1,'result1':result1,
                                                       'Rp11':Rp11,'Rp21':Rp21,'Rp31':Rp31,'Rp12':Rp12,'Rp22':Rp22,'Rp32':Rp32,
                                                       'Rp13':Rp13,'Rp23':Rp23,'Rp33':Rp33,'Rp14':Rp14,'Rp24':Rp24,'Rp34':Rp34,
                                                       'Rp15': Rp15, 'Rp25': Rp25, 'Rp35': Rp35, 'Rp16': Rp16,
                                                       'Rp26': Rp26, 'Rp36': Rp36,
                                                       'phiVc':phiVc,'Czg1':Czg1,'Czg2':Czg2,'Czg3':Czg3,'Czg4':Czg4,'Czg5':Czg5,'Czg6':Czg6,
                                                       'VV1': VV1, 'VV2': VV2, 'VV3': VV3, 'VV4': VV4, 'VV5': VV5,
                                                       'VV6': VV6, 'vs1': vs1, 'vs2': vs2, 'vs3': vs3, 'vs4': vs4,
                                                       'vs5': vs5, 'vs6': vs6,
                                                       'co_vs1': co_vs1, 'co_vs2': co_vs2, 'co_vs3': co_vs3,
                                                       'co_vs4': co_vs4, 'co_vs5': co_vs5, 'co_vs6': co_vs6,
                                                       'check1':check1,'check2':check2,'check3':check3,'check4':check4,'check5':check5,'check6':check6,
                                                       'Vux1':Vux1,'Vux2':Vux2,'Vux3':Vux3,'Vux4':Vux4,'Vux5':Vux5,'Vux6':Vux6,
                                                       'V1': V1, 'V2': V2, 'V3': V3, 'V4': V4, 'V5': V5,
                                                       'V6': V6, 's1': s1, 's2': s2, 's3': s3, 's4': s4,
                                                       's5': s5, 's6': s6,
                                                       'co_s1': co_s1, 'co_s2': co_s2, 'co_s3': co_s3,
                                                       'co_s4': co_s4, 'co_s5': co_s5, 'co_s6': co_s6,
                                                       'VVV1': VVV1, 'VVV2': VVV2, 'VVV3': VVV3, 'VVV4': VVV4, 'VVV5': VVV5,
                                                       'VVV6': VVV6, 'vvs1': vvs1, 'vvs2': vvs2, 'vvs3': vvs3, 'vvs4': vvs4,
                                                       'vvs5': vvs5, 'vvs6': vvs6,
                                                       'co_vvs1': co_vvs1, 'co_vvs2': co_vvs2, 'co_vvs3': co_vvs3,
                                                       'co_vvs4': co_vvs4, 'co_vvs5': co_vvs5, 'co_vvs6': co_vvs6,
                                                       'BX':BX,'BY':BY,
                                                       'Mux1': Mux1, 'Mux2': Mux2, 'Mux3': Mux3, 'Mux4': Mux4,
                                                       'Mux5': Mux5, 'Mux6': Mux6,
                                                       'Asx1': Asx1, 'Asx2': Asx2, 'Asx3': Asx3, 'Asx4': Asx4,
                                                       'Asx5': Asx5, 'Asx6': Asx6,
                                                       'Muy1':Muy1,'Muy2':Muy2,'Muy3':Muy3,'Muy4':Muy4,'Muy5':Muy5,'Muy6':Muy6,
                                                       'Asy1':Asy1,'Asy2':Asy2,'Asy3':Asy3,'Asy4':Asy4,'Asy5':Asy5,'Asy6':Asy6,})
    else:
        form = InputForm(auto_id="%s")
        return render(request,'pile_cap_3.html',{'form':form})
