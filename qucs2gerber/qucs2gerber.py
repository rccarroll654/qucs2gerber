#Copyright 2019 Russell Carroll
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from math import *
from numpy import *
import os

class Qucs2Gerber():

  # ----------------------------------------
  # General Class functions
  # ----------------------------------------

  def __init__(self):
    self.log_fn   = "qucs2grb_log.txt"
    self.out_fn   = "qucs_out.gbr"
    self.num_int  = 2
    self.num_decimals = 5
    self.unit_scale = 1.0 # Inches
    self.units = "in"
    self.verbose  = False
    self.out_fh   = None
    self.netlist_data = None
    self.log_print("-- QUCS to Gerber File Conversion Log --\n",'w')
  
  def __del__(self):
    self.kill()
  
  def kill(self):
    if self.out_fh:
      self.out_fh.close()
  
  def log_print(self,text,mode='a'):
    try:
      fh = open(self.log_fn,mode)
      fh.write(str(text) + "\n")
      fh.close()
    except:
      print("Error: Could not write to log file! " + self.log_fn)
      self.verbose = True
    
  # Print to screen and log
  def fprint(self,text,force=False):
    if self.verbose or force:
      print(str(text))
    self.log_print(text)

  # ----------------------------------------
  # Functions for Gerber File Generation
  # ----------------------------------------

  def SetDecimals(self,decimals,leading=2):
    try:
      self.num_decimals = int(decimals)
      self.num_int = int(leading)
    except:
      self.fprint("Error: Could not read number of decimals!")

  def SetUnits(self,units):
    if "in" in units:
      unit_scale = 1.0  # scale everything to inches
    elif "mm" in units:
      unit_scale = 0.0393701
    else:
      self.fprint("Error: Unknown units! " + units,force=True)
      return False
    self.units = units
    self.unit_scale = unit_scale

  def OpenOutpuFile(self,fn="output.grb"):
    self.out_fn = fn
    try:
      self.out_fh = open(self.out_fn,'w')
      return True
    except:
      self.fprint("Error: Could not output file! " + self.out_fn,force=True)
      self.verbose = True
      return False
    
  def out_write(self,text,append_str='\n'):
    try:
      self.out_fh.write(str(text) + append_str)
    except:
      self.fprint("Error: Could not write to output file! " + self.out_fn,force=True)
      self.verbose = True
    
  def GenerateHeader(self):
    header = [
      "G04 Generated using qucs2gerber.py*",
      "G04 Input file: {}*".format(self.netlist_fn),
      "%MO{}*%".format(self.units.upper()),             # Use relevant units
      "%LNTOP*%",                                       # Layer name TOP
      # Format specification, Leading zeros omitted, absolute coordinates, integer places, decimal places
      "%FSLAX{}{}Y{}{}*%".format(self.num_int,self.num_decimals,self.num_int,self.num_decimals),      
      "%ADD11C,0.0001*%"    # Define aperature, D11 is a circle with diameter of 0.0001 inch
    ]
    for l in header:
      self.out_write(l)
  
  def Finish(self):
    self.out_write("M02*",append_str='')
  
  def get_int(self,f):
    return int(round(f*10**self.num_decimals))
  
  # Draw rectangle with left edge at the origin
  def DrawRectangleLEO(self,width=1.0,length=1.0,x0=0.0,y0=0.0,rot=0.0):
    rot_rad = rot*pi/180.0
    R = [[cos(rot_rad),sin(rot_rad)],[-sin(rot_rad),cos(rot_rad)]]  # rotation matrix
    # initial coordinates
    a = [0, -width/2.0]
    b = [0, +width/2.0]
    c = [length, +width/2.0]
    d = [length, -width/2.0]
    # rotated coordinates
    at = dot(a,R)
    bt = dot(b,R)
    ct = dot(c,R)
    dt = dot(d,R)
    commands = [
      "G54D11*",    # Select aperature D11
      "G36*",       # Enable region mode
      "G01*",
      "X{}Y{}D02*".format(self.get_int(at[0]+x0),self.get_int(at[1]+y0)), 
      "X{}Y{}D01*".format(self.get_int(bt[0]+x0),self.get_int(bt[1]+y0)),
      "X{}Y{}D01*".format(self.get_int(ct[0]+x0),self.get_int(ct[1]+y0)),
      "X{}Y{}D01*".format(self.get_int(dt[0]+x0),self.get_int(dt[1]+y0)),
      "X{}Y{}D01*".format(self.get_int(at[0]+x0),self.get_int(at[1]+y0)),
      "G37*"        # Disable region mode
    ]
    for cmd in commands:
      self.out_write(cmd)

  # Draw polygon from list of corners
  def DrawPolygon(self,corners,x0=0.0,y0=0.0,rot=0.0):
    rot_rad = -rot*pi/180.0
    R = [[cos(rot_rad),sin(rot_rad)],[-sin(rot_rad),cos(rot_rad)]]  # rotation matrix
    # Generate transformed coordinates
    offset = array([x0,y0])
    ct = []
    for c in corners:
      ct.append(dot(R,c) + offset)
    ct.append(ct[0])
    # write the output
    self.out_write("G54D11*")  
    self.out_write("G36*")  
    self.out_write("G01*")  # Linear interpolation
    self.out_write("X{}Y{}D02*".format(self.get_int(ct[0][0]),self.get_int(ct[0][1])))
    for c in ct[1:]:
      cmd = "X{}Y{}D01*".format(self.get_int(c[0]),self.get_int(c[1]))
      self.out_write(cmd)
    self.out_write("G37*")

  def DrawMRSTUB(self,ri,ro,alpha,x0,y0,phi):
    # Calculate the paramters
    W = ri
    alpha_rad = alpha*pi/180.0
    l = W/(2*tan(alpha_rad/2))
    # Generate the relative points
    A = [0,W/2.0]
    B = [ro*cos(alpha_rad/2)-l,ro*sin(alpha_rad/2)]
    C = [ro*cos(alpha_rad/2)-l,-ro*sin(alpha_rad/2)]
    D = [0,-W/2.0]
    offset = array([-l,0])
    corners = [A,B,C,D,offset]
    # Rotate into the real coordinates
    rot_rad = -phi*pi/180.0
    R = array([[cos(rot_rad),sin(rot_rad)],[-sin(rot_rad),cos(rot_rad)]])  # rotation matrix
    ct = dot(R,array(corners).transpose()).transpose()
    for i in range(len(ct)):
      ct[i][0] = ct[i][0] + x0
      ct[i][1] = ct[i][1] + y0
    ct[4] = ct[4] - ct[1] # This makes the arc come out correctly in the gerber file
    # Initialize
    # write the output
    self.out_write("G54D11*")  
    self.out_write("G36*")  
    self.out_write("X{}Y{}D02*".format(self.get_int(ct[0][0]),self.get_int(ct[0][1])))
    self.out_write("X{}Y{}D01*".format(self.get_int(ct[1][0]),self.get_int(ct[1][1])))
    self.out_write("G75*")  # Multiquadrant
    self.out_write("G02*")  # Clockwise circular interpolation
    # Do the rotation
    self.out_write("X{}Y{}I{}J{}D01*".format(self.get_int(ct[2][0]),self.get_int(ct[2][1]),
      self.get_int(ct[4][0]),self.get_int(ct[4][1])))
    self.out_write("G01*")  # Linear interpolation
    self.out_write("X{}Y{}D01*".format(self.get_int(ct[2][0]),self.get_int(ct[2][1])))
    self.out_write("X{}Y{}D01*".format(self.get_int(ct[3][0]),self.get_int(ct[3][1])))
    self.out_write("X{}Y{}D01*".format(self.get_int(ct[0][0]),self.get_int(ct[0][1])))
    self.out_write("G37*")
    
  # ----------------------------------------
  # Functions for QUCS Netlist Parsing
  # ----------------------------------------
  
  def ReadNetlist(self,netlist_fn):
    self.netlist_fn = netlist_fn
    try:
      fh = open(netlist_fn,'r')
      self.netlist_data = fh.read()
      fh.close()
    except:
      self.fprint("Error: Could not read netlist file: " + netlist_fn,force=True)
  
  def GetParameter(self,line,param):
    try:
      param_list = line.split(" ")
      for a in param_list:
        if (param + "=") in a:
          return a.replace(param + "=","").replace("'","").replace('"','')
    except:
      self.fprint("Error: Could not find paramter: " + str(param),force=True)
      return False
  
  def RemoveSpaces(self,line):
    return line.replace(" mm","mm").replace(" mil","mil")
  
  def GetLength(self,length_str):
    if "mm" in length_str:
      return float(length_str.replace("mm",""))*0.0393701/self.unit_scale
    elif "mil" in length_str:
      return float(length_str.replace("mil",""))*0.001/self.unit_scale
    else:
      try:
        return float(length_str)
      except:
        self.fprint("Error: Unknown length unit! {}".format(length_str),force=True)
  
  def ParseNetlist(self):
    net_list = []
    elements = []
    lines = self.netlist_data.split("\n")
    for l in lines:
      l = self.RemoveSpaces(l)
      if "MLIN" in l:
        # MLIN:MLIN1 _net0 _net2 Subst="Subst1" W="1 mm" L="10 mm" Model="Hammerstad" DispModel="Kirschning" Temp="26.85"
        self.fprint("Found element: " + l)
        # Get parameters
        W = self.GetLength(self.GetParameter(l,"W"))
        L = self.GetLength(self.GetParameter(l,"L"))
        # Get nodes
        l = l.replace("MLIN:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        elements.append(["MLIN",l[0],l[1],l[2],W,L])
      elif "MTEE" in l:
        # MTEE:MS3 _net3 _net4 _net5 Subst="Subst1" W1="1 mm" W2="1 mm" W3="2 mm" MSModel="Hammerstad" MSDispModel="Kirschning" Temp="26.85"
        self.fprint("Found element: " + l)
        # Get parameters
        W1 = self.GetLength(self.GetParameter(l,"W1"))
        W2 = self.GetLength(self.GetParameter(l,"W2"))
        W3 = self.GetLength(self.GetParameter(l,"W3"))
        # Get nodes
        l = l.replace("MTEE:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        if l[3] not in net_list:
          net_list.append(l[3])
        elements.append(["MTEE",l[0],l[1],l[2],l[3],W1,W2,W3])
      elif "MCORN" in l:
        # MCORN:MS4 _net6 _net7 Subst="Subst1" W="1 mm"
        self.fprint("Found element: " + l)
        # Get parameters
        W = self.GetLength(self.GetParameter(l,"W"))
        # Get nodes
        l = l.replace("MCORN:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        elements.append(["MCORN",l[0],l[1],l[2],W])
      elif "MTAPER" in l:
        pass
      elif "MMBEND" in l:
        # MMBEND:MS5 _net8 _net9 Subst="Subst1" W="1 mm"
        self.fprint("Found element: " + l)
        # Get parameters
        W = self.GetLength(self.GetParameter(l,"W"))
        # Get nodes
        l = l.replace("MMBEND:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        elements.append(["MMBEND",l[0],l[1],l[2],W])
      elif "MSTEP" in l:
        # MSTEP:MS6 _net10 _net11 Subst="Subst1" W1="2 mm" W2="1 mm" MSModel="Hammerstad" MSDispModel="Kirschning"
        self.fprint("Found element: " + l)
        # Get parameters
        W1 = self.GetLength(self.GetParameter(l,"W1"))
        W2 = self.GetLength(self.GetParameter(l,"W2"))
        # Get nodes
        l = l.replace("MSTEP:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        elements.append(["MSTEP",l[0],l[1],l[2],W1,W2])
      elif "MSLIT" in l:
        pass
      elif "MGAP" in l:
        # MGAP:MS9 _net16 _net17 Subst="Subst1" W1="1 mm" W2="1 mm" S="1 mm" MSModel="Hammerstad" MSDispModel="Kirschning"
        self.fprint("Found element: " + l)
        # Get parameters
        W1 = self.GetLength(self.GetParameter(l,"W1"))
        W2 = self.GetLength(self.GetParameter(l,"W2"))
        S  = self.GetLength(self.GetParameter(l,"S"))
        # Get nodes
        l = l.replace("MGAP:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        elements.append(["MGAP",l[0],l[1],l[2],W1,W2,S])
      elif "MCURVE" in l:
        pass
      elif "MCURVE2" in l:
        pass
      elif "MRSTUB" in l:
        # MRSTUB:MS10 _net18 Subst="Subst1" ri="1 mm" ro="10 mm" alpha="90"
        self.fprint("Found element: " + l)
        # Get parameters
        ri = self.GetLength(self.GetParameter(l,"ri"))
        ro = self.GetLength(self.GetParameter(l,"ro"))
        a = self.GetLength(self.GetParameter(l,"alpha"))
        # Get nodes
        l = l.replace("MRSTUB:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        elements.append(["MRSTUB",l[0],l[1],ri,ro,a])
      elif "MBSTUB" in l:
        pass
      elif "MCFIL" in l:
        pass
      elif "MCOUPLED" in l:
        # MCOUPLED:MS5 _net8 _net9 _net7 _net10 Subst="Subst1" W="1 mm" L="10 mm" S="1 mm" Model="Kirschning" DispModel="Kirschning" Temp="26.85"
        self.fprint("Found element: " + l)
        # Get parameters
        W = self.GetLength(self.GetParameter(l,"W"))
        L = self.GetLength(self.GetParameter(l,"L"))
        S  = self.GetLength(self.GetParameter(l,"S"))
        # Get nodes
        l = l.replace("MCOUPLED:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        if l[3] not in net_list:
          net_list.append(l[3])
        if l[4] not in net_list:
          net_list.append(l[4])
        elements.append(["MCOUPLED",l[0],l[1],l[2],l[3],l[4],W,L,S])
        pass
      elif "MSABND" in l:
        pass
      elif "MSOBND" in l:
        pass
      elif "MCROSS" in l:
        # MCROSS:MS7 _net12 _net13 _net14 _net15 Subst="Subst1" W1="1 mm" W2="2 mm" W3="1 mm" W4="2 mm" MSModel="Hammerstad" MSDispModel="Kirschning"
        self.fprint("Found element: " + l)
        # Get parameters
        W1 = self.GetLength(self.GetParameter(l,"W1"))
        W2 = self.GetLength(self.GetParameter(l,"W2"))
        W3 = self.GetLength(self.GetParameter(l,"W3"))
        W4 = self.GetLength(self.GetParameter(l,"W4"))
        # Get nodes
        l = l.replace("MCROSS:","").strip().split(" ")
        if l[1] not in net_list:
          net_list.append(l[1])
        if l[2] not in net_list:
          net_list.append(l[2])
        if l[3] not in net_list:
          net_list.append(l[3])
        if l[4] not in net_list:
          net_list.append(l[4])
        elements.append(["MCROSS",l[0],l[1],l[2],l[3],l[4],W1,W2,W3,W4])
      elif "MCROSO" in l:
        pass
      elif "MSOP" in l:
        pass
      elif "VIAGND" in l:
        pass
      elif "VIA2" in l:
        pass
        
    self.net_list = net_list
    self.elements = elements
    self.fprint("Net List:")
    self.fprint(self.net_list)
    self.fprint("Elements:")
    self.fprint(self.elements)
    
    # Check the elements and netlist
    for net in self.net_list:
      used_cnt = 0
      used_list = []
      for e in elements:
        if net in e:
          used_cnt = used_cnt + 1
          used_list.append(e[1])
      if used_cnt > 2:
        self.fprint("Error: More than 2 components on a net! {} connected to {}".format(net,used_list),force=True)
  
  def GetNetIndex(self,net,element):
    if net in element:
      return element.index(net) - 2 # drop first two elements, reference to vector index
    else:
      return False
  
  def GetVectors(self,element):
    v = []  # gives [[x,y,phi],...]
    v.append([0,0,180]) # relative to first node
    l = element[0]
    if "MLIN" in l:
      L = element[5]
      v.append([L,0,0])  # Length in x direction
    elif "MTEE" in l:
      W1 = element[5]
      W2 = element[6]
      W3 = element[7]
      v.append([W3,0,0])
      v.append([W3/2,-max(W1,W2)/2.0,-90])
    elif "MCORN" in l:
      W = element[4]
      v.append([W/2.0,-W/2.0,-90])  # Length in x direction
    elif "MTAPER" in l:
      pass
    elif "MMBEND" in l:
      # elements.append(["MMBEND",l[0],l[1],l[2],W])
      W = element[4]
      v.append([W/2.0,-W/2.0,-90])  # Length in x direction
    elif "MSTEP" in l:
      # elements.append(["MSTEP",l[0],l[1],l[2],W1,W2])
      v.append([0,0,0])
    elif "MSLIT" in l:
      pass
    elif "MGAP" in l:
      # elements.append(["MGAP",l[0],l[1],l[2],W1,W2,S])
      S = element[6]
      v.append([S,0,0])  # Length in x direction
      pass
    elif "MCURVE" in l:
      pass
    elif "MCURVE" in l:
      pass
    elif "MCURVE2" in l:
      pass
    elif "MRSTUB" in l:
      pass
    elif "MBSTUB" in l:
      pass
    elif "MCFIL" in l:
      pass
    elif "MCLIN" in l:
      pass
    elif "MCOUPLED" in l:
      # elements.append(["MCOUPLED",l[0],l[1],l[2],l[3],l[4],W,L,S])
      W = element[6]
      L = element[7]
      S = element[8]
      v.append([0,-(W+S),180])
      v.append([L,-(W+S),0])
      v.append([L,0,0])
    elif "MSABND" in l:
      pass
    elif "MSOBND" in l:
      pass
    elif "MCROSS" in l:
      # elements.append(["MCROSS",l[0],l[1],l[2],l[3],l[4],W1,W2,W3,W4])
      W1 = element[6]
      W2 = element[7]
      W3 = element[8]
      W4 = element[9]
      x = max(W4,W2)
      y = max(W1,W3)
      v.append([x/2.0,y/2.0,90])
      v.append([x,0,0])
      v.append([x/2.0,-y/2.0,-90])
    elif "MCROSO" in l:
      pass
    elif "MSOP" in l:
      pass
    elif "VIAGND" in l:
      pass
    elif "VIA2" in l:
      pass
    return array(v)
  
  def InSlaveList(self,net="",elem=""):
    for s in self.slaves:
      if (net == s[0]) and (elem == s[1]):
        return True
    return False
  
  # This is the crazy function that actually decides how to route the microstrip lines by finding the coordinates
  def GetNextCoordinate(self):
    if len(self.coordinates) < 1:
      self.coordinates.append([self.elements[0][2],array([0,0,0])])  # Start with first element at the origin
      self.slaves.append([self.elements[0][2],self.elements[0][1]])
      return True
    # Look from the begining
    for c in self.coordinates:
      # Check each element
      for e in self.elements:
        v = self.GetVectors(e)
        L = len(v)
        # Look for new cordinates on this element
        if c[0] in e:
          for l in range(L):
            hit = False
            for s in self.coordinates:
              hit = hit or (e[l+2] == s[0])
            if not hit:
              # Check if the element is a slave of the coordinate
              slave = True
              for s in self.slaves:
                if (c[0] == s[0]) or (e[1] == s[1]):
                  slave = False
              if slave:
                self.slaves.append([c[0],e[1]])
              # New coordinate found. Add to list
              ind0 = self.GetNetIndex(c[0],e)
              va = v[l][0:2]
              vb = v[ind0][0:2]
              alpha = v[l][2]
              beta  = v[ind0][2]
              reverse_direction = False
              if self.InSlaveList(c[0],e[1]):
                self.fprint("{} is master of {}".format(e[1],e[l+2]))
                gamma = c[1][2]
              else:
                # Special slave case
                reverse_direction = True
                self.fprint("{} is slave of {}".format(e[1],e[l+2]))
                self.slaves.append([e[l+2],e[1]])
                gamma = c[1][2] -180
              theta =  180 - beta + gamma
              rot_rad = theta*pi/180.0
              R = [[cos(rot_rad),sin(rot_rad)],[-sin(rot_rad),cos(rot_rad)]]  # rotation matrix
              # rotated coordinates
              vt = dot(va-vb,R)
              v_new = array([vt[0],vt[1],0])
              new_c = v_new + c[1]
              if reverse_direction:
                phi = alpha + gamma - beta
              else:
                phi = alpha + gamma + 180 - beta
              while phi > 180.0: 
                phi = phi - 360.0
              while phi < -180.0: 
                phi = phi + 360.0
              
              new_c[2] = phi
              cor = [e[l+2],new_c]
              self.fprint("New coordinate: {} gives {}".format(e,cor))
              self.coordinates.append(cor)
              return True
    return False  # No more connections can be found

  def GetElement(self,refdes):
    for e in self.elements:
      if refdes == e[1]:
        return e
    self.fprintf("Error: Could not find element: {}".format(refdes),force=True)
    exit()

  def GetCoordinate(self,net):
    for c in self.coordinates:
      if net == c[0]:
        return c
    self.fprintf("Error: Could not find coordinate: {}".format(net),force=True)
    return False

  def WriteElement(self,element,x,y,phi):
    v = self.GetVectors(element)
    rot_rad = -phi*pi/180.0
    R = [[cos(rot_rad),sin(rot_rad)],[-sin(rot_rad),cos(rot_rad)]]  # rotation matrix
    l = element[0]
    if "MLIN" in l:
      W = element[4]
      L = element[5]
      self.DrawRectangleLEO(W,L,x,y,phi)
    elif "MTEE" in l:
      W1 = element[5]
      W2 = element[6]
      W3 = element[7]
      v21 = dot(R,v[1][0:2])
      v31 = dot(R,v[2][0:2])
      #self.fprint("MTEE {}: phi = {}, v = {}, v21 = {}, v31 {}".format(element[1],phi,v,v21,v31))
      self.DrawRectangleLEO(W1,W3/2.0,x,y,phi)  # Node 1
      self.DrawRectangleLEO(W2,W3/2.0,x+v21[0],y+v21[1],phi+180)  # Node 2
      self.DrawRectangleLEO(W3,max(W1,W2)/2.0,x+v31[0],y+v31[1],phi+90) # Node 3
    elif "MCORN" in l:
      W = element[4]
      self.DrawRectangleLEO(W,W,x,y,phi)
    elif "MTAPER" in l:
      pass
    elif "MMBEND" in l:
      # elements.append(["MMBEND",l[0],l[1],l[2],W])
      W = element[4]
      corners = [[0,W/2.0],[W,-W/2.0],[0,-W/2]]
      self.DrawPolygon(corners,x,y,phi)
      # TODO
    elif "MSTEP" in l:
      pass  # Draw nothing
    elif "MSLIT" in l:
      pass
    elif "MGAP" in l:
      pass
    elif "MCURVE" in l:
      pass
    elif "MCURVE2" in l:
      pass
    elif "MRSTUB" in l:
      # MRSTUB:MS10 _net18 Subst="Subst1" ri="1 mm" ro="10 mm" alpha="90"
      ri = element[3]
      ro = element[4]
      alpha = element[5]
      self.DrawMRSTUB(ri,ro,alpha,x,y,phi)
    elif "MBSTUB" in l:
      pass
    elif "MCFIL" in l:
      pass
    elif "MCLIN" in l:
      pass
    elif "MCOUPLED" in l:
      W = element[6]
      L = element[7]
      S = element[8]
      v21 = dot(R,v[1][0:2])
      self.DrawRectangleLEO(W,L,x,y,phi)
      self.DrawRectangleLEO(W,L,v21[0]+x,v21[1]+y,phi)
    elif "MSABND" in l:
      pass
    elif "MSOBND" in l:
      pass
    elif "MCROSS" in l:
      # elements.append(["MCROSS",l[0],l[1],l[2],l[3],l[4],W1,W2,W3,W4])
      W1 = element[6]
      W2 = element[7]
      W3 = element[8]
      W4 = element[9]
      x_m = max(W4,W2)
      y_m = max(W1,W3)
      v21 = dot(R,v[1][0:2])
      v31 = dot(R,v[2][0:2])
      v41 = dot(R,v[3][0:2])
      #self.fprint("MCROSS {}: phi = {}, v = {}, v21 = {}, v31 = {}, v41 = {}".format(element[1],phi,v,v21,v31,v41))
      self.DrawRectangleLEO(W1,x_m/2.0,x,y,phi)  # Node 1
      self.DrawRectangleLEO(W2,y_m/2.0,x+v21[0],y+v21[1],phi - 90)  # Node 2
      self.DrawRectangleLEO(W3,x_m/2.0,x+v31[0],y+v31[1],phi +180) # Node 3
      self.DrawRectangleLEO(W4,y_m/2.0,x+v41[0],y+v41[1],phi + 90) # Node 3
    elif "MCROSO" in l:
      pass
    elif "MSOP" in l:
      pass
    elif "VIAGND" in l:
      pass
    elif "VIA2" in l:
      pass
  
  def GetElementsUsingNet(self,net):
    connected = []
    for e in self.elements:
      L = len(self.GetVectors(e))
      for l in range(L):
        if net == e[2+l]:
          connected.append(e[1])
          break
    return connected
  
  def GenerateGerberElements(self):
    self.fprint("\nPlotting all elements with coordinates...")
    self.missed = []
    for e in self.elements:
      c = self.GetCoordinate(e[2])
      if c:
        x = c[1][0]
        y = c[1][1]
        phi = c[1][2]
        # Do final slave check
        slave = True
        for s in self.slaves:
          if (c[0] == s[0]) or (e[1] == s[1]):
            slave = False
        if slave:
          self.slaves.append([c[0],e[1]])
        # add extra 180 degrees is needed
        pair_not_in_slave_list = not self.InSlaveList(e[2],e[1])
        if pair_not_in_slave_list:
          phi = phi + 180
        self.WriteElement(e,x,y,phi)
      else:
        self.missed.append(e[1])
        # Report any elements that could not be connected
    if len(self.missed) > 0:
      self.fprint("Warning: These elements could not be connected! {}".format(self.missed),force=True)

  def ProcessNetlist(self):
    self.coordinates = []
    self.slaves = []
    self.ParseNetlist()
    while self.GetNextCoordinate(): pass
    
    # Do final slave check, this should add any connected elements missed the first time
    for e in self.elements:
      c = self.GetCoordinate(e[2])
      if c:
        # Do final slave check
        slave = True
        for s in self.slaves:
          if (c[0] == s[0]) or (e[1] == s[1]):
            slave = False
        if slave:
          self.slaves.append([c[0],e[1]])
          
    self.fprint("Coordinates: {}".format(self.coordinates))
    self.fprint("Slaves:      {}".format(self.slaves))
    self.GenerateGerberElements()
  
    
  # ----------------------------------------
  # Main function call
  # ----------------------------------------


  
