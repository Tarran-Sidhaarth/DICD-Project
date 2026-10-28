v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 170 -200 170 -170 {lab=q}
N 300 -200 300 -170 {lab=qb}
N 260 -230 260 -140 {lab=q}
N 210 -230 210 -140 {lab=qb}
N 170 -190 260 -190 {lab=q}
N 210 -180 300 -180 {lab=qb}
N 170 -140 170 -110 {lab=gnd}
N 300 -140 300 -110 {lab=gnd}
N 90 -180 170 -180 {lab=q}
N 300 -190 370 -190 {lab=qb}
N -30 -310 -30 -40 {lab=bl}
N 470 -310 470 -40 {lab=blb}
N -30 -180 30 -180 {lab=bl}
N 430 -190 470 -190 {lab=blb}
N 170 -260 300 -260 {lab=vdd}
N 230 -320 230 -260 {lab=vdd}
N 170 -110 300 -110 {lab=gnd}
N 240 -110 240 -70 {lab=gnd}
N 60 -70 400 -70 {lab=gnd}
N 60 -180 60 -70 {lab=gnd}
N 60 -70 60 -60 {lab=gnd}
N 400 -190 400 -60 {lab=gnd}
N 60 -420 60 -220 {lab=wl}
N 400 -420 400 -230 {lab=wl}
N 40 -420 420 -420 {lab=wl}
N 240 -70 240 -30 {lab=gnd}
N 230 -450 230 -420 {lab=wl}
N 170 -260 170 -230 {lab=vdd}
N 300 -260 300 -230 {lab=vdd}
N -60 -240 -30 -240 {lab=bl}
N 470 -250 490 -250 {lab=blb}
C {sky130_fd_pr/nfet_01v8.sym} 280 -140 0 0 {name=M1
W=1
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 280 -230 0 0 {name=M3
W=0.42
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 190 -230 0 1 {name=M4
W=0.42
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 190 -140 0 1 {name=M2
W=1
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 60 -200 3 1 {name=M5
W=0.5
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 400 -210 1 0 {name=M6
W=0.5
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {iopin.sym} 490 -250 0 0 {name=p4 lab=blb}
C {iopin.sym} -60 -240 2 0 {name=p5 lab=bl}
C {iopin.sym} 230 -320 3 0 {name=p6 lab=vdd}
C {iopin.sym} 240 -30 1 0 {name=p7 lab=gnd}
C {ipin.sym} 230 -450 1 0 {name=p1 lab=wl}
C {opin.sym} 130 -180 3 0 {name=p2 lab=q}
C {opin.sym} 350 -190 1 0 {name=p3 lab=qb}
