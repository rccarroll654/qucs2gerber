<Qucs Schematic 0.0.19>
<Properties>
  <View=56,38,1552,1177,1,0,60>
  <Grid=10,10,1>
  <DataSet=demo.dat>
  <DataDisplay=demo.dpl>
  <OpenDisplay=1>
  <Script=demo.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <MLIN MS1 1 220 340 -26 15 0 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MSTEP MS2 1 350 340 -26 17 0 0 "Subst1" 1 "2 mm" 1 "1 mm" 1 "Hammerstad" 0 "Kirschning" 0>
  <MTEE MS3 1 490 340 15 -26 0 3 "Subst1" 1 "1 mm" 1 "1 mm" 1 "2 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0 "showNumbers" 0>
  <MLIN MS5 1 490 480 15 -26 0 1 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS4 1 490 230 15 -26 0 1 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MCORN MS9 1 490 130 -7 -72 0 1 "Subst1" 1 "1 mm" 1>
  <MLIN MS10 1 670 130 -26 15 0 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS12 1 920 230 15 -26 0 1 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MTEE MS14 1 920 340 -115 -26 0 1 "Subst1" 1 "1 mm" 1 "1 mm" 1 "2 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0 "showNumbers" 0>
  <MLIN MS13 1 920 430 15 -26 0 1 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MCROSS MS6 1 490 570 -26 34 0 0 "Subst1" 1 "1 mm" 1 "2 mm" 1 "1 mm" 1 "2 mm" 1 "Hammerstad" 0 "Kirschning" 0 "showNumbers" 0>
  <MLIN MS7 1 730 560 -26 15 0 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MCORN MS8 1 920 561 -26 15 0 3 "Subst1" 1 "1 mm" 1>
  <MLIN MS15 1 360 570 -26 15 0 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS17 1 1070 340 -26 -91 1 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS16 1 490 770 15 -26 0 1 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MGAP MS18 1 1180 340 -26 15 0 0 "Subst1" 1 "1 mm" 1 "1 mm" 1 "1 mm" 1 "Hammerstad" 0 "Kirschning" 0>
  <MLIN MS19 1 1290 340 -26 -91 1 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MMBEND MS20 1 920 130 15 -7 0 0 "Subst1" 1 "1 mm" 1>
  <MRSTUB MS21 1 1490 340 -114 -18 0 3 "Subst1" 1 "1 mm" 0 "10 mm" 1 "90" 1>
  <SUBST Subst1 1 270 1000 -30 24 0 0 "9.8" 1 "1 mm" 1 "35 um" 1 "2e-4" 1 "0.022e-6" 1 "0.15e-6" 1>
  <MCORN MS23 1 490 870 -115 -26 0 2 "Subst1" 1 "1 mm" 1>
  <MLIN MS26 1 620 870 -26 -91 1 0 "Subst1" 1 "1 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <Pac P1 1 140 410 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P2 1 280 630 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P3 1 810 910 18 -26 0 1 "3" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 140 460 0 0 0 0>
  <GND * 1 280 680 0 0 0 0>
  <GND * 1 810 960 0 0 0 0>
</Components>
<Wires>
  <490 260 490 310 "" 0 0 0 "">
  <380 340 460 340 "" 0 0 0 "">
  <250 340 320 340 "" 0 0 0 "">
  <490 370 490 450 "" 0 0 0 "">
  <490 160 490 200 "" 0 0 0 "">
  <520 130 640 130 "" 0 0 0 "">
  <700 130 890 130 "" 0 0 0 "">
  <920 160 920 200 "" 0 0 0 "">
  <920 260 920 310 "" 0 0 0 "">
  <920 370 920 400 "" 0 0 0 "">
  <920 460 920 531 "" 0 0 0 "">
  <760 560 890 560 "" 0 0 0 "">
  <700 560 700 570 "" 0 0 0 "">
  <520 570 700 570 "" 0 0 0 "">
  <490 510 490 540 "" 0 0 0 "">
  <390 570 460 570 "" 0 0 0 "">
  <490 600 490 740 "" 0 0 0 "">
  <950 340 1040 340 "" 0 0 0 "">
  <1100 340 1150 340 "" 0 0 0 "">
  <1210 340 1260 340 "" 0 0 0 "">
  <1320 340 1480 340 "" 0 0 0 "">
  <520 870 590 870 "" 0 0 0 "">
  <490 800 490 840 "" 0 0 0 "">
  <650 860 650 870 "" 0 0 0 "">
  <140 440 140 460 "" 0 0 0 "">
  <140 340 140 380 "" 0 0 0 "">
  <140 340 190 340 "" 0 0 0 "">
  <280 570 280 600 "" 0 0 0 "">
  <280 570 330 570 "" 0 0 0 "">
  <280 660 280 680 "" 0 0 0 "">
  <650 860 810 860 "" 0 0 0 "">
  <810 860 810 880 "" 0 0 0 "">
  <810 940 810 960 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
