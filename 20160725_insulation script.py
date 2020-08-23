import rhinoscriptsyntax as rs
import Rhino
import math

Other_Option = False

# Select the surface to clad with insulation
surf = Rhino.Input.RhinoGet.GetOneObject("Select the surface to clad with insulation",False,Rhino.DocObjects.ObjectType.Surface)

# Select the window sill line
window_sillLine = Rhino.Input.RhinoGet.GetOneObject("Select the window sill line",False,Rhino.DocObjects.ObjectType.EdgeFilter)

rs.UnselectAllObjects()

# Select the window Left line
window_leftLine = Rhino.Input.RhinoGet.GetOneObject("Select the window Left line",False,Rhino.DocObjects.ObjectType.EdgeFilter)

rs.UnselectAllObjects()

# Select Ground line
groundLine = Rhino.Input.RhinoGet.GetOneObject("Select the ground line",False,Rhino.DocObjects.ObjectType.EdgeFilter)

# input the length of insulation panel
#ipLength = rs.GetInteger("Input the lenght of insulation panel in millimeter")
ipLength = 1000

# input the height of insulation panel
#ipHeight = rs.GetInteger("Input the height of insulation panel in millimeter")
ipHeight = 500

# input the thickness of insulation panel
#ipThick = rs.GetInteger("Input the thickness of insulation panel in millimeter")
ipThick = 100

# Surface Bounding Box
bbox = rs.BoundingBox(surf[1])

def HorizontalLines():
    #Course = rs.OffsetCurve(,bbox[3],sill_remain)
    
    Surf_Height = rs.Distance(bbox[0],bbox[3])
    
    #number of horizontal cources
    hori_no = Surf_Height / ipHeight
    
    #convert to intiger
    hori_no = int(hori_no)
    
    Course_All = []
    
    Course = rs.AddLine(bbox[0],bbox[1])
    
    Course_start = rs.ExtendCurveLength(Course,0,0,ipThick)
    Course_end = rs.ExtendCurveLength(Course,0,1,ipThick)
    
    Course = rs.JoinCurves((Course_start,Course,Course_end),True)
    Course1 = Course
    
    Course_All.append(Course)
    for index in range(0,hori_no,1):
        Course = rs.OffsetCurve(Course,bbox[3],ipHeight)
        Course_All.append(Course)
    
    Course = rs.OffsetCurve(Course1,bbox[3],Surf_Height)
    Course_All.append(Course)
    
    rs.ObjectColor(Course_All,[255,0,0])
    
    return Course_All

#Horizontal_Lines = HorizontalLines()
surf_norm = rs.SurfaceNormal(surf[1],(0.5,0.5))
surf_norm = (surf_norm)



def WindowFrame():
    
    surf_int_edge_all = rs.DuplicateSurfaceBorder(surf[1],type = 2)
    print len(surf_int_edge_all)
    window_frame_all = []
    
    for item in range(0,len(surf_int_edge_all),1):
        surf_int_edge = surf_int_edge_all[item]
        
        surf_int_edge = rs.ExplodeCurves(surf_int_edge,True)
        
        trans1 = rs.XformTranslation((0,0,2*ipThick))
        trans2 = rs.XformTranslation((0,0,-2*ipThick))
        
        point_1 = rs.CurveStartPoint(surf_int_edge[0])
        point_2 = rs.CurveStartPoint(surf_int_edge[1])
        point_3 = rs.CurveStartPoint(surf_int_edge[2])
        point_4 = rs.CurveStartPoint(surf_int_edge[3])
        
        point_5 = rs.PointTransform(point_1,trans1)
        point_6 = rs.PointTransform(point_2,trans1)
        point_7 = rs.PointTransform(point_3,trans1)
        point_8 = rs.PointTransform(point_4,trans1)
        
        point_1 = rs.PointTransform(point_1,trans2)
        point_2 = rs.PointTransform(point_2,trans2)
        point_3 = rs.PointTransform(point_3,trans2)
        point_4 = rs.PointTransform(point_4,trans2)
        
        frame_points = []
        frame_points.append(point_1)
        frame_points.append(point_2)
        frame_points.append(point_3)
        frame_points.append(point_4)
        frame_points.append(point_5)
        frame_points.append(point_6)
        frame_points.append(point_7)
        frame_points.append(point_8)
        
        
        window_frame = rs.AddBox(frame_points)
        window_frame_all.append(window_frame)
    
    return window_frame_all

window_frame_all = WindowFrame()


def WindowLeftDistance():
    # Find midpoint of window left line
    midpoint_windowLeft = rs.CurveMidPoint(window_leftLine[1])
    
    # Find closest point in curve window left
    parameterLeftLine = rs.CurveClosestPoint(window_leftLine[1],midpoint_windowLeft)
    
    # Find curve window left Tangent
    windowLeft_Tangent = rs.CurveTangent(window_leftLine[1],parameterLeftLine)
    
    # find window left normal plane
    windowLeft_plane = rs.PlaneFromNormal(midpoint_windowLeft,windowLeft_Tangent)
    
    # find start and end points of ground line
    points_ll = []
    start_ll = bbox[0]
    end_ll = bbox[3]
    points_ll.append(start_ll)
    points_ll.append(end_ll)
    
    #find point on Surface Left line
    point_SurfLeftLine = rs.LinePlaneIntersection(points_ll,windowLeft_plane)
    #point_SurfLeftLine = rs.AddPoint(point_SurfLeftLine)
    
    Window_leftDistance = rs.Distance(midpoint_windowLeft,point_SurfLeftLine)
    
    return Window_leftDistance

Window_leftDistance = WindowLeftDistance()


"""
# Change definition to change vertical cuts
def VerticalLines2():
    start_ll = bbox[0]
    end_ll = bbox[3]
    
    groundLine_distance = rs.Distance(bbox[0],bbox[1])
    
    gl_remain = groundLine_distance % ipLength
    
    vert_no = groundLine_distance / (ipLength/2)
    vert_no = int(vert_no)
    
    vert_no_l = vert_no/2
    vert_no_r = (vert_no/2 - 1)
    
    #Add first line in the left 
    surfLeftLine = rs.AddLine(start_ll,end_ll)
    VerticalLine_All = []
    VerticalLine_All.append(surfLeftLine)
    
    Vertical = surfLeftLine
    
    if gl_remain < (ipLength/4):
        for index in range(0,vert_no_l,1):
            Vertical = rs.OffsetCurve(Vertical,bbox[2],ipLength)
            VerticalLine_All.append(Vertical)
        for index in range(0,2,1):
            Vertical = rs.OffsetCurve(Vertical,bbox[2],(ipLength + gl_remain)/2)
            VerticalLine_All.append(Vertical)
        for index in range (0,vert_no_r,1):
            Vertical = rs.OffsetCurve(Vertical,bbox[2],ipLength)
            VerticalLine_All.append(Vertical)
            
            
    print gl_remain
    return VerticalLine_All

Vertical_Lines = VerticalLines2()
"""



def VerticalLines():
    start_ll = bbox[0]
    end_ll = bbox[3]
    
    #Add first line in the left 
    surfLeftLine = rs.AddLine(start_ll,end_ll)
    VerticalLine_All = []
    
    # Add Vertical line for finger joint
    Ver_Line = rs.OffsetCurve(surfLeftLine,-bbox[2],ipThick)
    VerticalLine_All.append(Ver_Line)
    
    #Add Second line
    Ver_Line = rs.OffsetCurve(Ver_Line,bbox[2],ipThick)
    VerticalLine_All.append(Ver_Line)
    
    Window_leftRemain = Window_leftDistance % (ipLength/2)
    
    #Ver_Line = rs.OffsetCurve(surfLeftLine,bbox[2],Window_leftRemain)
    #VerticalLine_All.append(Ver_Line)
    
    vertLeft_no = Window_leftDistance / (ipLength/2)
    
    vertLeft_no = int(vertLeft_no)
    
    groundLine_distance = rs.Distance(bbox[0],bbox[1])
    
    vert_no = groundLine_distance / (ipLength/2)
    vert_no = int(vert_no)
    
    Vertical = surfLeftLine
    
    for index in range(0,vert_no,1):
        Vertical = rs.OffsetCurve(Vertical,bbox[2],(ipLength/2))
        VerticalLine_All.append(Vertical)
    
    last_finger = rs.AddLine(bbox[1],bbox[2])
    VerticalLine_All.append(last_finger)
    
    last_line = rs.OffsetCurve(surfLeftLine,bbox[2],groundLine_distance + ipThick)
    VerticalLine_All.append(last_line)
    
    #Start_sill = rs.CurveStartPoint(window_sillLine[1])
    #End_sill = rs.CurveEndPoint(window_sillLine[1])
    #sillLine_Distance = rs.Distance(Start_sill,End_sill)
    
    #Sill_Remain = sillLine_Distance % (ipLength/2)
    
    
    #Sillvert_no = sillLine_Distance / (ipLength/2)
    #Sillvert_no = int(vertLeft_no)
    
    
    rs.DeleteObject(surfLeftLine)
    
    return VerticalLine_All

Vertical_Lines = VerticalLines()

def splitVertical(St,ver_item):
    
    ver_param = rs.DivideCurveLength(ver_item,ipHeight,False,False)
    ver_Split = rs.SplitCurve(ver_item,ver_param,True)
    ver_line_split = []
    
    for ver_id in range(St,len(ver_Split),2):
         ver_item = ver_Split[ver_id]
         
         ver_line_split.append(ver_item)
         #rs.DeleteObject(ver_item)
    
    return ver_line_split



def Select():
    ver_line_split_even = []
    ver_line_split_odd = []
    
    if Other_Option == True:
        
        for ver_item_id in range(0,len(Vertical_Lines),2):
            ver_item = Vertical_Lines[ver_item_id]
            St = 0
            split_even = splitVertical(St,ver_item) 
            ver_line_split_even.append(split_even)
        for ver_item_id in range(1,len(Vertical_Lines),2):
            ver_item = Vertical_Lines[ver_item_id]
            St = 1
            split_odd = splitVertical(St,ver_item)
            ver_line_split_odd.append(split_odd)
    else:
        
        for ver_item_id in range(0,len(Vertical_Lines),2):
            ver_item = Vertical_Lines[ver_item_id]
            St = 1
            split_even = splitVertical(St,ver_item) 
            ver_line_split_even.append(split_even)
        for ver_item_id in range(1,len(Vertical_Lines),2):
            ver_item = Vertical_Lines[ver_item_id]
            St = 0
            split_odd = splitVertical(St,ver_item)
            ver_line_split_odd.append(split_odd)
    return (ver_line_split_even,ver_line_split_odd)

ver_line_split = Select()
ver_line_split_even = ver_line_split[0]
ver_line_split_odd =  ver_line_split[1]

next_even_Cource = len(ver_line_split_even[0])
next_odd_Cource = len(ver_line_split_odd[0])

def flat(unflat):
    flat = []
    for i in unflat:
        for j in i:
            
            flat.append(j)
    return flat

ver_line_split_even = flat(ver_line_split_even) 

ver_line_split_odd = flat(ver_line_split_odd)


def InsulationPanel(left_edge,right_edge):
    
    points = []
    #insulation_left = ver_line_split_even[i]
    point_1 = rs.CurveStartPoint(left_edge)
    point_2 = rs.CurveEndPoint(left_edge)
    #insulation_right = ver_line_split_even[i + next_even_Cource]
    point_3 = rs.CurveEndPoint(right_edge)
    point_4 = rs.CurveStartPoint(right_edge)
    
    trans = rs.XformTranslation((0,0,ipThick))
    point_5 = rs.PointTransform(point_1,trans)
    point_6 = rs.PointTransform(point_2,trans)
    point_7 = rs.PointTransform(point_3,trans)
    point_8 = rs.PointTransform(point_4,trans)
    
    points.append(point_1)
    points.append(point_2)
    points.append(point_3)
    points.append(point_4)
    points.append(point_5)
    points.append(point_6)
    points.append(point_7)
    points.append(point_8)
    
    insulation = rs.AddBox(points)
    
    return insulation



insulation_Panels = [] 

for i in range(0,len(ver_line_split_even) - next_even_Cource,1):
    left_edge = ver_line_split_even[i]
    right_edge = ver_line_split_even[i + next_even_Cource]
    insulation_even = InsulationPanel(left_edge,right_edge)
    insulation_Panels.append(insulation_even)


for i in range(0,len(ver_line_split_odd) - next_odd_Cource,1):
    left_edge = ver_line_split_odd[i]
    right_edge = ver_line_split_odd[i + next_odd_Cource]
    insulation_odd = InsulationPanel(left_edge,right_edge)
    insulation_Panels.append(insulation_odd)


all = rs.AllObjects(False,False,False,False)
for item in range(0,len(all),1):
    item = all[item]
    test = rs.IsCurve(item)
    if test == True:
        rs.DeleteObject(item)

insulation_Panels_temp = []


for i in range(0,len(insulation_Panels),1):
    item = insulation_Panels[i]
    for j in range(0,len(window_frame_all),1):
        window_frame = window_frame_all[j]
        split = rs.SplitBrep(item,window_frame,True)
        
        if split == None:
            insulation_Panels_temp.append(item)
            
        else :
            for pie in range(0,len(split),1):
                pie = split[pie]
                insulation_Panels_temp.append(pie)

insulation_Panels = insulation_Panels_temp
insulation_Panels_temp = []

#print insulation_Panels
for item in range(0,len(insulation_Panels),1):
    item = insulation_Panels[item]
    if item == None:
        rs.DeleteObject(item)
    else:
        insulation_Panels_temp.append(item)

insulation_Panels = insulation_Panels_temp
insulation_Panels_temp = []

#print insulation_Panels 

for i in range(0,len(insulation_Panels),1):
    item = insulation_Panels[i]
    face = rs.ExtractSurface(item,2,True)
    #print face
    for j in range(0,len(window_frame_all),1):
        window_frame = window_frame_all[j]
        window_frame_bbox = rs.BoundingBox(window_frame)
        
        test = rs.IsObjectInBox(item,window_frame_bbox,True)
        if test == False:
            insulation_Panels_temp.append(item)
            rs.DeleteObject(face)
        else:
            rs.DeleteObject(item)
            rs.DeleteObject(face)

insulation_Panels = insulation_Panels_temp
#print insulation_Panels

ideal_vol = ipLength * ipHeight * ipThick

rs.DeleteObject(window_frame)

yellow_Count = []
red_Count = []

for item in range(0,len(insulation_Panels),1):
    item = insulation_Panels[item]
    #test = rs.IsPolysurface(item)
    #print test
    item_vol = rs.SurfaceVolume(item)
    #print item_vol
    
    if item_vol != None:
        item_vol = item_vol[0]
        item_vol = math.ceil(item_vol)
        #print item_vol
        if item_vol < ideal_vol:
            rs.ObjectColor(item,(255,255,0))
            yellow_Count.append(item)
    else :
        rs.ObjectColor(item,(255,0,0))
        red_Count.append(item)

print "Total number of insulation panels required is %d" % len(insulation_Panels)
print "Number of straight cut pieces is %d" % len(yellow_Count) 
print "Number of Angle cut pieces is %d " % len(red_Count)




#    item_vol = item_vol[0]
#    print item_vol
#    item_vol = math.ceil(item_vol)
#    print item_vol
#    if item_vol < ideal_vol:
#        rs.ObjectColor(item,(255,255,0))





#rs.ObjectColor(ver_line_split_even,(255,255,0))

def SillHeight():
    # Find mid point of sill line 
    midpointSill = rs.CurveMidPoint(window_sillLine[1])
    #midpointSill = rs.AddPoint(midpointSill)
    
    # Find closest point in curve
    parameterSill = rs.CurveClosestPoint(window_sillLine[1],midpointSill)
    
    # Find curve Tangent
    sill_Tangent = rs.CurveTangent(window_sillLine[1],parameterSill)
    
    # find normal plane
    sill_plane = rs.PlaneFromNormal(midpointSill,sill_Tangent)
    
    # find start and end points of ground line
    points_gl = []
    start_gl = rs.CurveStartPoint(groundLine[1])
    end_gl = rs.CurveEndPoint(groundLine[1])
    points_gl.append(start_gl)
    points_gl.append(end_gl)
    
    #find point on ground line
    pointGroundLine = rs.LinePlaneIntersection(points_gl,sill_plane)
    #pointGroundLine = rs.AddPoint(pointGroundLine)
    
    sill_Height = rs.Distance(midpointSill,pointGroundLine)
    
    return sill_Height
