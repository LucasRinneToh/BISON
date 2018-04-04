# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:39:19 2018

@author: lrh
"""
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')



import xml.etree.ElementTree as ET
import uuid

def createRid():
    id = uuid.uuid1().int>>84
    string = '#'
    return string + str(id)


class DIS2:
    #This class is the Wrapper for the whole xml code
    def __init__(
            self, 
            dis_project = None,
            building = None
            ):
        
        self.XML = ET.Element("DIS2")
            
    def addProject(self,dis_project):
        for element in dis_project.XML_hierachy:
            self.XML.append(element)
                
    def addBuilding(self,building):
        for element in building.XML_hierachy:
            self.XML.append(element)
    

class DIS_PROJECT:
    #This class is the 'header' element for each project and contains
    #project data, simulation settings, view settings etc.
    #This element is the 'root' of the tree, however it must be wrapped in
    #the <DIS2> tag.
    def __init__(
            self,
            id = 'BS7040_001',
            description = '',
            database = 'path',
            tstep = '6',
            options = '0',
            scale = '50',
            grid = '1',
            layer_thick = '0.05',
            start_time = '0',
            end_time = '0',
            has_design_parm = '0'
            ):
        
        self.id = id #element ID, by default: BS7040_001 
        self.description = description #Project description
        self.database = database #path to database
        self.tstep = tstep #timesteps in simulation
        self.options = options #binary options
        self.scale = scale #view scale in BSim, default: 50
        self.grid = grid #gridsize in BSim, default: 1
        self.layer_thick = layer_thick #calculated layer thickness for simulation
        self.start_time = start_time #start date for simulation
        self.end_time = end_time #end date for simulation
        self.has_design_parm = has_design_parm #unknown parameter

        self.XML = ET.Element("DIS_PROJECT")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_description = ET.SubElement(self.XML,"description")
        self.XML_description.text = description
        self.XML_database = ET.SubElement(self.XML,"database")
        self.XML_database.text = database
        self.XML_tstep = ET.SubElement(self.XML,"tstep")
        self.XML_tstep.text = tstep
        self.XML_options = ET.SubElement(self.XML,"options")
        self.XML_options.text = options
        self.XML_scale = ET.SubElement(self.XML,"scale")
        self.XML_scale.text = scale
        self.XML_grid = ET.SubElement(self.XML,"grid")
        self.XML_grid.text = grid
        self.XML_layer_thick = ET.SubElement(self.XML,"layer_thick")
        self.XML_layer_thick.text = layer_thick
        self.XML_start_time = ET.SubElement(self.XML,"start_time")
        self.XML_start_time.text = start_time
        self.XML_end_time = ET.SubElement(self.XML,"end_time")
        self.XML_end_time.text = end_time
        self.XML_has_design_parm = ET.SubElement(self.XML,"has_design_parm")
        self.XML_has_design_parm.text = has_design_parm

        self.XML_hierachy = []
        self.XML_hierachy.append(self.XML)


class BUILDING:
    #This class contains the 'Building' element.
    #The building is a child of DIS_PROJECT and a parent of thermal zones and rooms    
    def __init__(
            self,
            id = 'Building',
            rotation = '0',
            current = '0',
            height = '0',
            room = None,
            thermalzone = None,
            located_on_site = '',
            has_thermal_zones = ''
            ):
        
        self.id = id #Building name
        self.rotation = rotation #Relative rotation
        self.current = current #Unknown parameter
        self.height = height #Height parameter for nat-vent purposes
        self.composed_of = '' #Rid(s) of rooms in building !TEMPORARILY DEPRECATED
        self.located_on_site = located_on_site #Rid of site
        self.has_thermal_zones = '' #Rid(s) of thermal zones in building !TEMPORARILY DEPRECATED

        self.rooms = []
        self.thermalzones = []

        self.XML = ET.Element("BUILDING")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_rotation = ET.SubElement(self.XML,"rotation")
        self.XML_rotation.text = rotation
        self.XML_current = ET.SubElement(self.XML,"current")
        self.XML_current.text = current
        self.XML_height = ET.SubElement(self.XML,"height")
        self.XML_height.text = height
        self.XML_composed_of = ET.SubElement(self.XML,"composed_of")
        self.XML_located_on_site = ET.SubElement(self.XML,"located_on_site")
        self.XML_located_on_site.text = located_on_site
        self.XML_has_thermal_zones = ET.SubElement(self.XML,"has_thermal_zones")
    
        self.XML_hierachy = []
        self.XML_hierachy.append(self.XML)
    
    
    def addRoom(self,room):
        for element in room.XML_hierachy:
            if element.tag == 'ROOM':
                self.rooms.append(element.get("rid"))
            self.XML_hierachy.append(element)
        self.XML_composed_of.text = " ".join(self.rooms)
        
        
        
    def addThermalZone(self,thermalzone):
        self.thermalzones.append(thermalzone.XML.get("rid"))
        self.XML_has_thermal_zones.text = " ".join(self.thermalzones)
        for element in thermalzone.XML_hierachy:
            self.XML_hierachy.append(element)
        



class THERMAL_ZONE:
    #This class contains the 'Thermal Zone' element. The thermal zone
    #is a child of Building and parent of Room.
    def __init__(
            self,
            id = 'Thermalzone',
            solar_to_air_fact = 0.2,
            solar_to_ceil_ratio = 0.15,
            solar_to_wall_ratio = 0.3,
            solar_to_floor_ratio = 0.55,
            solar_lost_fact = 0.1,
            kappa = 1,
            top_height = 1.1,
            top_frac = 0.5,
            room = None,
            has_service = ''
            ):
        
        self.id = id #Thermal Zone name
        self.solar_to_air_fact = solar_to_air_fact 
        self.solar_to_ceil_ratio = solar_to_ceil_ratio
        self.solar_to_wall_ratio = solar_to_wall_ratio
        self.solar_to_floor_ratio = solar_to_floor_ratio
        self.solar_lost_fact = solar_lost_fact
        self.kappa = kappa
        self.top_height = top_height
        self.top_frac = top_frac
        self.composed_of = '' #Rid(s) of Rooms in thermal zone !TEMPORARILY DEPRECATED
        self.has_service = has_service #Rid(s) of thermal zone services
        
        self.rooms = []
        
        self.XML = ET.Element("THERMAL_ZONE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_solar_to_air_fact = ET.SubElement(self.XML,"solar_to_air_fact")
        self.XML_solar_to_air_fact.text = str(solar_to_air_fact)
        self.XML_solar_to_ceil_ratio = ET.SubElement(self.XML,"solar_to_ceil_ratio")
        self.XML_solar_to_ceil_ratio.text = str(solar_to_ceil_ratio)
        self.XML_solar_to_wall_ratio = ET.SubElement(self.XML,"solar_to_wall_ratio")
        self.XML_solar_to_wall_ratio.text = str(solar_to_wall_ratio)
        self.XML_solar_to_floor_ratio = ET.SubElement(self.XML,"solar_to_floor_ratio")
        self.XML_solar_to_floor_ratio.text = str(solar_to_floor_ratio)
        self.XML_solar_lost_fact = ET.SubElement(self.XML,"solar_lost_fact")
        self.XML_solar_lost_fact.text = str(solar_lost_fact)
        self.XML_kappa = ET.SubElement(self.XML,"kappa")
        self.XML_kappa.text = str(kappa)
        self.XML_top_height = ET.SubElement(self.XML,"top_height")
        self.XML_top_height.text = str(top_height)
        self.XML_top_frac = ET.SubElement(self.XML,"top_frac")
        self.XML_top_frac.text = str(top_frac)
        self.XML_composed_of = ET.SubElement(self.XML,"composed_of")
        self.XML_has_service = ET.SubElement(self.XML,"has_service")
        self.XML_has_service.text = str(has_service)

        self.XML_hierachy = []
        self.XML_hierachy.append(self.XML)

    def addRoom(self,room):
        for element in room.XML_hierachy:
            if element.tag == "ROOM":
                self.rooms.append(element.get("rid"))
            self.XML_hierachy.append(element)
        self.XML_composed_of.text = " ".join(self.rooms)
            

class CreateRoom:
    def __init__(self):
        
        self.XML_hierachy = []
        
        self.Room = ROOM()
        self.Cell = CELL()
        
        self.Cell_bounded_by = []
        self.Room.XML_represented_by_cell.text = self.Cell.XML.get("rid")
        
        
        self.XML_hierachy.append(self.Room.XML)
        self.XML_hierachy.append(self.Cell.XML)

    def addFace(self):
        FaceHierachy = CreateFace().XML_hierachy
        self.Cell_bounded_by.append(FaceHierachy[2].get("rid"))
        self.Cell.XML_bounded_by.text = " ".join(self.Cell_bounded_by)
        for element in FaceHierachy:
            self.XML_hierachy.append(element)


class ROOM:
    #This class contains the 'Room' element.
    #Room is a parent of the 'Face' element and a sibling of Cell.
    def __init__(
            self,
            id = 'Room',
            represented_by_cell = '',
            ref_x = 0,
            ref_y = 0,
            ref_z = 0,
            has_temp = '',
            behave_like = '',
            has_type = '',
            has_inner_shell = '',
            has_refpoint = ''
            ):
        
        self.id = id #Room name
        self.represented_by_cell = represented_by_cell #Rid of cell
        self.ref_x = ref_x #Reference X-coordinate
        self.ref_y = ref_y #Reference Y-coordinate
        self.ref_z = ref_z #Reference Z-coordinate
        self.has_temp = has_temp 
        self.behave_like = behave_like
        self.has_type = has_type
        self.has_inner_shell = has_inner_shell
        self.has_refpoint = has_refpoint
        
        self.XML = ET.Element("ROOM")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_represented_by_cell = ET.SubElement(self.XML,"represented_by_cell")
        self.XML_represented_by_cell.text = represented_by_cell
        self.XML_ref_x = ET.SubElement(self.XML,"ref_x")
        self.XML_ref_x.text = str(ref_x)
        self.XML_ref_y = ET.SubElement(self.XML,"ref_y")
        self.XML_ref_y.text = str(ref_y)
        self.XML_ref_z = ET.SubElement(self.XML,"ref_z")
        self.XML_ref_z.text = str(ref_z)
        self.XML_has_temp = ET.SubElement(self.XML,"has_temp")
        self.XML_has_temp.text = has_temp
        self.XML_behave_like = ET.SubElement(self.XML,"behave_like")
        self.XML_behave_like.text = behave_like
        self.XML_has_type = ET.SubElement(self.XML,"has_type")
        self.XML_has_type.text = has_type
        self.XML_has_inner_shell = ET.SubElement(self.XML,"has_inner_shell")
        self.XML_has_inner_shell.text = has_inner_shell
        self.XML_has_refpoint = ET.SubElement(self.XML,"has_refpoint")
        self.XML_has_refpoint.text = has_refpoint

        self.XML_hierachy = []
        self.XML_hierachy.append(self.XML)

class CELL:
    #This class contains the 'Cell' element
    #Cell is a sibling of room. Each room has an equivilent cell.
    def __init__(
            self,
            id = 'Cell',
            volume = '',
            bounded_by = ''
            ):
        self.id = id #Cell id/name
        self.volume = volume #Cell volume
        self.bounded_by = bounded_by #Rids of bounding FACE_SIDEs
        
        self.XML = ET.Element("CELL")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_volume = ET.SubElement(self.XML,"volume")
        self.XML_volume.text = volume
        self.XML_bounded_by = ET.SubElement(self.XML,"bounded_by")
        self.XML_bounded_by.text = bounded_by


class CreateFace:
    def __init__(
            self
            ):
        
        self.XML_hierachy = []
        self.Face = FACE()
        self.Construction = CONSTRUCTION()
        self.FaceSide1 = FACE_SIDE()
        self.Finish1 = FINISH()
        self.FaceSide2 = FACE_SIDE()
        self.Finish2 = FINISH()


        self.EdgeRids = []
        
        self.Face.XML_has_face_side.text = self.FaceSide1.XML.get("rid") + ' ' + self.FaceSide2.XML.get("rid")
        self.Construction.XML_represented_by.text = self.Face.XML.get("rid")
        self.FaceSide1.XML_has_face.text = self.Face.XML.get("rid")
        self.Finish1.XML_represented_by.text = self.FaceSide1.XML.get("rid")
        self.FaceSide2.XML_has_face.text = self.Face.XML.get("rid")
        self.Finish2.XML_represented_by.text = self.FaceSide2.XML.get("rid")


        self.XML_hierachy.append(self.Face.XML)
        self.XML_hierachy.append(self.Construction.XML)
        self.XML_hierachy.append(self.FaceSide1.XML)
        self.XML_hierachy.append(self.Finish1.XML)
        self.XML_hierachy.append(self.FaceSide2.XML)
        self.XML_hierachy.append(self.Finish2.XML)


    def addEdge(self,startX,startY,startZ,endX,endY,endZ):
        for element in CreateEdge(startX=startX,startY=startY,startZ=startZ,endX=endX,endY=endY,endZ=endZ).XML_hierachy:
            if element.tag == "EDGE":
                self.EdgeRids.append(element.get("rid"))
            self.XML_hierachy.append(element)
        self.Face.XML_has_edge.text = " ".join(self.EdgeRids)


class CreateWindoor:
    def __init__(self):
        
        self.XML_hierachy = []
        self.Windoor = WINDOOR()
        self.Face = FACE()
        self.FaceSide1 = FACE_SIDE()
        self.Finish1 = FINISH()
        self.FaceSide2 = FACE_SIDE()
        self.Finish2 = FINISH()
        
        self.EdgeRids = []
        
        self.Face.XML_has_face_side.text = self.FaceSide1.XML.get("rid") + ' ' + self.FaceSide2.XML.get("rid")
        self.Windoor.XML_represented_by.text = self.Face.XML.get("rid")
        self.Windoor.XML_has_finish.text = self.Finish1.XML.get("rid") + ' ' + self.Finish2.XML.get("rid")
        self.FaceSide1.XML_has_face.text = self.Face.XML.get("rid")
        self.Finish1.XML_represented_by.text = self.FaceSide1.XML.get("rid")
        self.FaceSide2.XML_has_face.text = self.Face.XML.get("rid")
        self.Finish2.XML_represented_by.text = self.FaceSide2.XML.get("rid")
        
        self.XML_hierachy.append(self.Face.XML)
        self.XML_hierachy.append(self.Windoor.XML)
        self.XML_hierachy.append(self.FaceSide1.XML)
        self.XML_hierachy.append(self.Finish1.XML)
        self.XML_hierachy.append(self.FaceSide2.XML)
        self.XML_hierachy.append(self.Finish2.XML)
        
    def addEdge(self,startX,startY,startZ,endX,endY,endZ):
        for element in CreateEdge(startX=startX,startY=startY,startZ=startZ,endX=endX,endY=endY,endZ=endZ).XML_hierachy:
            if element.tag == "EDGE":
                self.EdgeRids.append(element.get("rid"))
            self.XML_hierachy.append(element)
        self.Face.XML_has_edge.text = " ".join(self.EdgeRids)
        



class FACE:
    #This class contains the 'Face' element. 
    #Each face has an equivilent Construction, 2 Face sides and 2 Finishes
    def __init__(
            self,
            id = 'Face',
            area = '',
            round = '',
            has_edge = '',
            has_face_side = ''
            ):
        self.id = id #Face Name
        self.area = area #Surface area
        self.round = round #Surface circumferance
        self.has_edge = has_edge #Rids of edges
        self.has_face_side = has_face_side #Rid of FACE_SIDE
        
        self.XML = ET.Element("FACE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_area = ET.SubElement(self.XML,"area")
        self.XML_area.text = area
        self.XML_round = ET.SubElement(self.XML,"round")
        self.XML_round.text = round
        self.XML_has_edge = ET.SubElement(self.XML,"has_edge")
        self.XML_has_edge.text = has_edge
        self.XML_has_face_side = ET.SubElement(self.XML,"has_face_side")
        

class CONSTRUCTION:
    def __init__(
            self,
            id = 'Construction',
            displacement = 0,
            hz0 = '',
            sfb = '',
            u_value = '',
            exposure = '',
            represented_by = '',
            includes_segments = '',
            has_finish = '',
            thickness = '',
            of_type = '',
            has_thermal_bridge = ''
            ):
        self.id = id #Construction name
        self.displacement = displacement #Displacement of construction
        self.hz0 = hz0 #Unknown parameter
        self.sfb = sfb #sfb number of construction (from db)
        self.u_value = u_value #u-value of construction
        self.exposure = exposure #Unknown parameter
        self.represented_by = represented_by #Rid of FACE
        self.includes_segments = includes_segments #Rid(s) of windoors
        self.has_finish = has_finish #Rid of FINISH
        self.thickness = thickness #Construction thickness
        self.u_value = u_value #u-value of construction (don't know why there's two parameters for this)
        self.of_type = of_type
        self.has_thermal_bridge = has_thermal_bridge
        
        self.XML = ET.Element("CONSTRUCTION")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_displacement = ET.SubElement(self.XML,"displacement")
        self.XML_displacement.text = str(displacement)
        self.XML_hz0 = ET.SubElement(self.XML,"hz0")
        self.XML_hz0.text = hz0
        self.XML_sfb = ET.SubElement(self.XML,"sfb")
        self.XML_sfb.text = sfb
        self.XML_u_value = ET.SubElement(self.XML,"u_value")
        self.XML_u_value.text = u_value
        self.XML_exposure = ET.SubElement(self.XML,"exposure")
        self.XML_exposure.text = exposure
        self.XML_represented_by = ET.SubElement(self.XML,"represented_by")
        self.XML_represented_by.text = represented_by
        self.XML_includes_segments = ET.SubElement(self.XML,"includes_segments")
        self.XML_includes_segments.text = includes_segments
        self.XML_has_finish = ET.SubElement(self.XML,"has_finish")
        self.XML_has_finish.text = has_finish
        self.XML_thickness = ET.SubElement(self.XML,"thickness")
        self.XML_thickness.text = thickness
        self.XML_of_type = ET.SubElement(self.XML,"thickness")
        self.XML_of_type.text = of_type
        self.XML_has_thermal_bridge = ET.SubElement(self.XML,"has_thermal_bridge")
        self.XML_has_thermal_bridge.text = has_thermal_bridge
        


class FACE_SIDE:
    def __init__(
            self,
            id = 'Face side',
            locked = '',
            has_normal = '',
            faces_cell = '',
            has_face = ''
            ):
        self.id = id #Face side name
        self.locked = locked #Unknown parameter
        self.has_normal = has_normal #Rid of Normal Vector
        self.faces_cell = faces_cell #Rid of Cell the face is facing
        self.has_face = has_face #Rid of Face
        
        self.XML = ET.Element("FACE_SIDE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_locked = ET.SubElement(self.XML,"locked")
        self.XML_locked.text = locked
        self.XML_has_normal = ET.SubElement(self.XML,"has_normal")
        self.XML_has_normal.text = has_normal
        self.XML_faces_cell = ET.SubElement(self.XML,"faces_cell")
        self.XML_faces_cell.text = faces_cell
        self.XML_has_face = ET.SubElement(self.XML,"has_face")
        self.XML_has_face.text = has_face


class FINISH:
    def __init__(
            self,
            id = 'Finish',
            r = '',
            z = '',
            rc = '',
            filtration = '',
            represented_by = '',
            made_of = '',
            facing = '$'
            ):
        self.id = id #Finish name
        self.r = r #Unknown parameter
        self.z = z #Unknown parameter
        self.rc = rc #Unknown parameter
        self.filtration = filtration #Filtration through finish
        self.represented_by = represented_by #Rid of Face side
        self.made_of = made_of #Unknown parameter
        self.facing = facing #Unknown parameter
        
        self.XML = ET.Element("FINISH")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_r = ET.SubElement(self.XML,"r")
        self.XML_r.text = r
        self.XML_z = ET.SubElement(self.XML,"z")
        self.XML_z.text = z
        self.XML_rc = ET.SubElement(self.XML,"rc")
        self.XML_rc.text = rc
        self.XML_filtration = ET.SubElement(self.XML,"filtration")
        self.XML_filtration.text = filtration
        self.XML_represented_by = ET.SubElement(self.XML,"represented_by")
        self.XML_represented_by.text = represented_by
        self.XML_made_of = ET.SubElement(self.XML,"made_of")
        self.XML_made_of.text = made_of
        self.XML_facing = ET.SubElement(self.XML,"made_of")
        self.XML_facing.text = facing




class WINDOOR:
    def __init__(
            self,
            id = 'Windoor',
            displacement = '',
            hz0 = '',
            sfb = '',
            u_value = '',
            exposure = '',
            represented_by = '',
            includes_segments = '',
            has_finish = '',
            thickness = '',
            of_type = '',
            has_thermal_bridge = '',
            offset = '',
            frame_area = '',
            panel_area = '',
            sf1 = '',
            sf2 = '',
            sf3 = '',
            round = '',
            cd_coeff = '',
            cnt_frac = '',
            a_frac = '',
            ka_coeff = '',
            overhang = '',
            left_sidefin = '',
            right_sidefin = ''
            ):
        self.id = id #Windoor name
        self.displacement = displacement 
        self.hz0 = hz0 
        self.sfb = sfb
        self.u_value = u_value #U-value of windoor
        self.exposure = exposure
        self.represented_by = represented_by #Rid of FACE
        self.includes_segments = includes_segments 
        self.has_finish = has_finish #Rid of FINISH
        self.thickness = thickness
        self.u_value = u_value
        self.of_type = of_type
        self.has_thermal_bridge = has_thermal_bridge
        self.offset = offset
        self.frame_area = frame_area
        self.panel_area = panel_area
        self.sf1 = sf1
        self.sf2 = sf2
        self.sf3 = sf3
        self.round = round
        self.cd_coeff = cd_coeff
        self.cnt_frac = cnt_frac
        self.a_frac = a_frac
        self.ka_coeff = ka_coeff
        self.overhang = overhang
        self.left_sidefin = left_sidefin
        self.right_sidefin = right_sidefin        

        self.XML = ET.Element("WINDOOR")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_displacement = ET.SubElement(self.XML,"displacement")
        self.XML_displacement.text = displacement
        self.XML_hz0 = ET.SubElement(self.XML,"hz0")
        self.XML_hz0.text = hz0
        self.XML_sfb = ET.SubElement(self.XML,"sfb")
        self.XML_sfb.text = sfb
        self.XML_u_value = ET.SubElement(self.XML,"u_value")
        self.XML_u_value.text = u_value
        self.XML_exposure = ET.SubElement(self.XML,"exposure")
        self.XML_exposure.text = exposure
        self.XML_represented_by = ET.SubElement(self.XML,"represented_by")
        self.XML_represented_by.text = represented_by
        self.XML_includes_segments = ET.SubElement(self.XML,"includes_segments")
        self.XML_includes_segments.text = includes_segments
        self.XML_has_finish = ET.SubElement(self.XML,"has_finish")
        self.XML_has_finish.text = has_finish
        self.XML_thickness = ET.SubElement(self.XML,"thickness")
        self.XML_thickness.text = thickness
        self.XML_of_type = ET.SubElement(self.XML,"of_type")
        self.XML_of_type.text = of_type
        self.XML_has_thermal_bridge = ET.SubElement(self.XML,"has_thermal_bridge")
        self.XML_has_thermal_bridge.text = has_thermal_bridge
        self.XML_offset = ET.SubElement(self.XML,"offset")
        self.XML_offset.text = offset
        self.XML_frame_area = ET.SubElement(self.XML,"frame_area")
        self.XML_frame_area.text = frame_area
        self.XML_panel_area = ET.SubElement(self.XML,"panel_area")
        self.XML_panel_area.text = panel_area
        self.XML_sf1 = ET.SubElement(self.XML,"sf1")
        self.XML_sf1.text = sf1
        self.XML_sf2 = ET.SubElement(self.XML,"sf2")
        self.XML_sf2.text = sf2
        self.XML_sf3 = ET.SubElement(self.XML,"sf3")
        self.XML_sf3.text = sf3
        self.XML_round = ET.SubElement(self.XML,"round")
        self.XML_round.text = round
        self.XML_cd_coeff = ET.SubElement(self.XML,"cd_coeff")
        self.XML_cd_coeff.text = cd_coeff
        self.XML_cnt_frac = ET.SubElement(self.XML,"cnt_frac")
        self.XML_cnt_frac.text = cnt_frac
        self.XML_a_frac = ET.SubElement(self.XML,"a_frac")
        self.XML_a_frac.text = a_frac
        self.XML_ka_coeff = ET.SubElement(self.XML,"ka_coeff")
        self.XML_ka_coeff.text = ka_coeff
        self.XML_overhang = ET.SubElement(self.XML,"overhang")
        self.XML_overhang.text = overhang
        self.XML_left_sidefin = ET.SubElement(self.XML,"left_sidefin")
        self.XML_left_sidefin.text = left_sidefin
        self.XML_right_sidefin = ET.SubElement(self.XML,"right_sidefin")
        self.XML_right_sidefin.text = right_sidefin
        

class CreateEdge:
    def __init__(
            self,
            startX=None,
            startY=None,
            startZ=None,
            endX=None,
            endY=None,
            endZ=None
            ):
        self.Edge = EDGE()
        self.StartPoint = CreatePoint(startX,startY,startZ)
        self.EndPoint = CreatePoint(endX,endY,endZ)
        
        self.Edge.XML_has_vertex.text = self.StartPoint.Vertex.XML.get("rid") + ' ' + self.EndPoint.Vertex.XML.get("rid")
        
        self.XML_hierachy = []
        self.XML_hierachy.append(self.Edge.XML)
        for element in self.StartPoint.XML_hierachy:
            self.XML_hierachy.append(element)
        for element in self.EndPoint.XML_hierachy:
            self.XML_hierachy.append(element)



class CreatePoint:
    def __init__(
            self,
            x=None,
            y=None,
            z=None
            ):
        
        self.XML_hierachy = []
        self.Vector = VECTOR3D(x=x,y=y,z=z)
        self.Vertex = VERTEX()
        self.Vertex.XML_has_geometry.text = self.Vector.XML.get("rid")
        
        self.XML_hierachy.append(self.Vector.XML)
        self.XML_hierachy.append(self.Vertex.XML)


class EDGE:
    def __init__(
            self,
            id = 'Edge',
            edge_length = '',
            has_vertex = ''
            ):
        self.id = id #Name of edge (irrelevant)
        self.edge_length = edge_length #length of edge
        self.has_vertex = has_vertex #Rids of start- and endpoint (VERTEX)
        
        self.XML = ET.Element("EDGE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_edge_length = ET.SubElement(self.XML,"edge_length")
        self.XML_edge_length.text = edge_length
        self.XML_has_vertex = ET.SubElement(self.XML,"has_vertex")
        self.XML_has_vertex.text = has_vertex

        self.XML_hierachy = []
        self.XML_hierachy.append(self.XML)
        
        

class VECTOR3D:
    def __init__(
            self,
            id = 'Vector3D',
            x = None,
            y = None,
            z = None
            ):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        
        self.XML = ET.Element("VECTOR3D")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_x = ET.SubElement(self.XML,"x")
        self.XML_x.text = str(x)
        self.XML_y = ET.SubElement(self.XML,"y")
        self.XML_y.text = str(y)
        self.XML_z = ET.SubElement(self.XML,"z")
        self.XML_z.text = str(z)


class VERTEX:
    def __init__(
            self,
            id = 'Vertex',
            has_geometry = ''
            ):
        self.id = id #Vertex name (irrelevant)
        self.has_geometry = has_geometry #Rid of VECTOR3D

        self.XML = ET.Element("VERTEX")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_has_geometry = ET.SubElement(self.XML,"has_geometry")
        self.XML_has_geometry.text = has_geometry


class SYSTEM:
    def __init__(
            self,
            id = '',
            active = 1,
            has_component = '',
            has_schedule = '',
            system_type = ''
            ):
        self.id = id
        self.active = active
        self.has_component = has_component
        self.has_schedule = has_schedule
        self.system_type = system_type
        
        self.XML = ET.Element("SYSTEM")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_active = ET.SubElement(self.XML,"active")
        self.XML_active.text = str(active)
        self.XML_has_component = ET.SubElement(self.XML,"has_component")
        self.XML_has_component.text = has_component
        self.XML_has_schedule = ET.SubElement(self.XML,"has_schedule")
        self.XML_has_schedule.text = has_schedule
        self.XML_system_type = ET.SubElement(self.XML,"system_type")
        self.XML_system_type.text = system_type

        
class EQUIPMENT:
    def __init__(
            self,
            id = 'Equipment',
            heat_load = 0.3,
            part_to_air = 0.5
            ):
        self.id = id
        self.heat_load = heat_load
        self.part_to_air = part_to_air
        
        self.XML = ET.Element("EQUIPMENT")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_heat_load = ET.SubElement(self.XML,"heat_load")
        self.XML_heat_load.text = str(heat_load)
        self.XML_part_to_air = ET.SubElement(self.XML,"part_to_air")
        self.XML_part_to_air.text = str(part_to_air)
        

class SCHEDULE:
    def __init__(
            self,
            id = 'Schedule',
            has_control = '',
            has_time_definition = ''
            ):
        self.id = id
        self.has_control = has_control
        self.has_time_definition = has_time_definition
        
        self.XML = ET.Element("SCHEDULE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_has_control = ET.SubElement(self.XML,"has_control")
        self.XML_has_control.text = has_control
        self.XML_has_time_definition = ET.SubElement(self.XML,"has_time_definition")
        self.XML_has_time_definition.text = has_time_definition
        
        
class DAY_PROFILE:
    def __init__(
            self,
            id = "Day Profile",
            hour = '',
            percent = '',
            protect = 0
            ):
        self.id = id
        self.hour = hour
        self.percent = percent
        self.protect = protect
        
        self.XML = ET.Element("DAY_PROFILE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_hour = ET.SubElement(self.XML,"hour")
        self.XML_hour.text = hour
        self.XML_percent = ET.SubElement(self.XML,"percent")
        self.XML_percent.text = percent
        self.XML_protect = ET.SubElement(self.XML,"protect")
        self.XML_protect.text = protect


class TIME_DEFINITION:
    def __init__(
            self,
            id = 'Time definition',
            hour = '',
            day = '',
            week = '',
            month = '',
            tariff_class = 0,
            protect = 0
            ):
        self.id = id
        self.hour = hour
        self.day = day
        self.week = week
        self.month = month
        self.tariff_class = tariff_class
        self.protect = protect
        
        self.XML = ET.Element("TIME_DEFINITION")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_hour = ET.SubElement(self.XML,"hour")
        self.XML_hour.text = hour
        self.XML_day = ET.SubElement(self.XML,"day")
        self.XML_day.text = day
        self.XML_week = ET.SubElement(self.XML,"week")
        self.XML_week.text = week
        self.XML_month = ET.SubElement(self.XML,"month")
        self.XML_month.text = month
        self.XML_tariff_class = ET.SubElement(self.XML,"tariff_class")
        self.XML_tariff_class.text = tariff_class
        self.XML_protect = ET.SubElement(self.XML,"protect")
        self.XML_protect.text = protect


class HEATING:
    def __init__(
            self,
            id = 'Heating',
            max_power = 1,
            fixed_part = 0,
            part_to_air = 0.6,
            unit = 0,
            central = '.F.'
            ):
        self.id = id
        self.max_power = max_power
        self.fixed_part = fixed_part
        self.part_to_air = part_to_air
        self.unit = unit
        self.central = central
        
        self.XML = ET.Element("HEATING")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_max_power = ET.SubElement(self.XML,"max_power")
        self.XML_max_power.text = str(max_power)
        self.XML_fixed_part = ET.SubElement(self.XML,"fixed_part")
        self.XML_fixed_part.text = str(fixed_part)
        self.XML_part_to_air = ET.SubElement(self.XML,"part_to_air")
        self.XML_part_to_air.text = str(part_to_air)
        self.XML_unit = ET.SubElement(self.XML,"unit")
        self.XML_unit.text = str(unit)
        self.XML_central = ET.SubElement(self.XML,"central")
        self.XML_central.text = central
        

class HEATING_CTRL:
    def __init__(
            self,
            id = 'Heating Control',
            factor = 1,
            set_point = 20,
            design_temp = -12,
            min_power = 0.5,
            te_min = 17,
            sensor = ''
            ):
        self.id = id
        self.factor = factor
        self.set_point = set_point
        self.design_temp = design_temp
        self.min_power = min_power
        self.te_min = te_min
        self.sensor = sensor
        
        self.XML = ET.Element("HEATING_CTRL")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_factor = ET.SubElement(self.XML,"factor")
        self.XML_factor.text = str(factor)
        self.XML_set_point = ET.SubElement(self.XML,"set_point")
        self.XML_set_point.text = str(set_point)
        self.XML_design_temp = ET.SubElement(self.XML,"design_temp")
        self.XML_design_temp.text = str(design_temp)
        self.XML_min_power = ET.SubElement(self.XML,"min_power")
        self.XML_min_power.text = str(min_power)
        self.XML_te_min = ET.SubElement(self.XML,"te_min")
        self.XML_te_min.text = str(te_min)
        self.XML_sensor = ET.SubElement(self.XML,"sensor")
        self.XML_sensor.text = sensor


class INFILTRATION:
    def __init__(
            self,
            id = 'Infiltration',
            basic_air_change = 0.5,
            temp_factor = 0,
            temp_power = 0.5,
            wind_factor = 0
            ):
        self.id = id
        self.basic_air_change = basic_air_change
        self.temp_factor = temp_factor
        self.temp_power = temp_power
        self.wind_factor = wind_factor
        
        self.XML = ET.Element("INFILTRATION")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_basic_air_change = ET.SubElement(self.XML,"basic_air_change")
        self.XML_basic_air_change.text = str(basic_air_change)
        self.XML_temp_factor = ET.SubElement(self.XML,"temp_factor")
        self.XML_temp_factor.text = str(temp_factor)
        self.XML_temp_power = ET.SubElement(self.XML,"temp_power")
        self.XML_temp_power.text = str(temp_power)
        self.XML_wind_factor = ET.SubElement(self.XML,"wind_factor")
        self.XML_wind_factor.text = str(wind_factor)

        

class SITE:
    def __init__(
            self,
            id = 'Site',
            weather_file = '/path',
            refl_rad = 0.2,
            refl_light = 0.1,
            horizon = 7,
            emissivity = 0.9,
            co2 = 350,
            terrain = 0,
            has_location = '',
            has_ground = ''
            ):
        self.id = id
        self.weather_file = weather_file
        self.refl_rad = refl_rad
        self.refl_light = refl_light
        self.horizon = horizon
        self.emissivity = emissivity
        self.co2 = co2
        self.terrain = terrain
        self.has_location = has_location
        self.has_ground = has_ground
        
        self.XML = ET.Element("SITE")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_weather_file = ET.SubElement(self.XML,"weather_file")
        self.XML_weather_file.text = weather_file
        self.XML_refl_rad = ET.SubElement(self.XML,"refl_rad")
        self.XML_refl_rad.text = str(refl_rad)
        self.XML_refl_light = ET.SubElement(self.XML,"refl_light")
        self.XML_refl_light.text = str(refl_light)
        self.XML_horizon = ET.SubElement(self.XML,"horizon")
        self.XML_horizon.text = str(horizon)
        self.XML_emissivity = ET.SubElement(self.XML,"emissivity")
        self.XML_emissivity.text = str(emissivity)
        self.XML_co2 = ET.SubElement(self.XML,"co2")
        self.XML_co2.text = str(co2)
        self.XML_terrain = ET.SubElement(self.XML,"terrain")
        self.XML_terrain.text = str(terrain)
        self.XML_has_location = ET.SubElement(self.XML,"has_location")
        self.XML_has_location.text = has_location
        self.XML_has_ground = ET.SubElement(self.XML,"has_ground")
        self.XML_has_ground.text = has_ground


class LOCATION:
    def __init__(
            self,
            id = 'Location',
            latitude = 55.793,
            longitude = 12.16,
            time_zone = 1,
            elevation = 10
            ):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.elevation = elevation
        
        self.XML = ET.Element("LOCATION")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_latitude = ET.SubElement(self.XML,"latitude")
        self.XML_latitude.text = str(latitude)
        self.XML_longitude = ET.SubElement(self.XML,"longitude")
        self.XML_longitude.text = str(longitude)
        self.XML_time_zone = ET.SubElement(self.XML,"time_zone")
        self.XML_time_zone.text = str(time_zone)
        self.XML_elevation = ET.SubElement(self.XML,"elevation")
        self.XML_elevation.text = str(elevation)


class GROUND:
    def __init__(
            self,
            id = 'Ground',
            represented_by_cell = '',
            max_temp = 12,
            max_humidity = 0.0058,
            max_at_date = 10.8,
            min_temp = 9,
            min_humidity = 0.004
            ):
        self.id = id
        self.represented_by_cell = represented_by_cell
        self.max_temp = max_temp
        self.max_humidity = max_humidity
        self.max_at_date = max_at_date
        self.min_temp = min_temp
        self.min_humidity = min_humidity
        
        self.XML = ET.Element("GROUND")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_represented_by_cell = ET.SubElement(self.XML,"represented_by_cell")
        self.XML_represented_by_cell.text = represented_by_cell
        self.XML_max_temp = ET.SubElement(self.XML,"max_temp")
        self.XML_max_temp.text = str(max_temp)
        self.XML_max_humidity = ET.SubElement(self.XML,"max_humidity")
        self.XML_max_humidity.text = str(max_humidity)
        self.XML_max_at_date = ET.SubElement(self.XML,"max_at_date")
        self.XML_max_at_date.text = str(max_at_date)
        self.XML_min_temp = ET.SubElement(self.XML,"min_temp")
        self.XML_min_temp.text = str(min_temp)
        self.XML_min_humidity = ET.SubElement(self.XML,"min_humidity")
        self.XML_min_humidity.text = str(min_humidity)

class CONSTRUCTION_ELEMENT:
    def __init__(
            self,
            id = 'Construction Element',
            name = 'Construction Element',
            sfb = None,
            unit = None,
            lifetime = 0,
            thickness = None,
            resistance = None,
            composed_of = None
            ):
        
        self.id = id
        self.name = name
        self.sfb = sfb
        self.unit = unit
        self.lifetime = lifetime
        self.thickness = thickness
        self.resistance = resistance
        self.composed_of = composed_of
        
        self.XML = ET.Element("CONSTRUCTION_ELEMENT")
        self.XML.set("rid",createRid())
        self.XML_id = ET.SubElement(self.XML,"id")
        self.XML_id.text = id
        self.XML_name = ET.SubElement(self.XML,"name")
        self.XML_name.text = name
        self.XML_sfb = ET.SubElement(self.XML,"sfb")
        self.XML_sfb.text = sfb
        self.XML_unit = ET.SubElement(self.XML,"unit")
        self.XML_unit.text = str(unit)
        self.XML_lifetime = ET.SubElement(self.XML,"lifetime")
        self.XML_lifetime.text = str(lifetime)
        self.XML_thickness = ET.SubElement(self.XML,"thickness")
        self.XML_thickness.text = str(thickness)
        self.XML_resistance = ET.SubElement(self.XML,"resistance")
        self.XML_resistance.text = str(resistance)
        self.XML_composed_of = ET.SubElement(self.XML,"composed_of")
        self.XML_composed_of.text = composed_of
        


