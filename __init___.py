# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "LiDAR-Tools",
    "author": "Brian Hynds",
    "version": (1, 0, 1),
    "blender": (2, 93, 0),
    "location": "File > Import > LAS data",
    "description": "LiDAR Importer",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
import laspy
import numpy as np
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
from mathutils import Vector

def get_attribute(header, attr_name, default="N/A"):
    if hasattr(header, attr_name):
        return str(getattr(header, attr_name))
    else:
        return default

class IMPORT_OT_las_data(Operator, ImportHelper):
    bl_idname = "import_scene.las_data"
    bl_label = "Import LAS/LAZ data"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".las;.laz"  # Add support for LAZ files
    filter_glob: StringProperty(default="*.las;*.laz", options={'HIDDEN'})  # Update the filter_glob to include LAZ files

class IMPORT_OT_las_data(Operator, ImportHelper):
    bl_idname = "import_scene.las_data"
    bl_label = "Import LAS/LAZ data"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".las;.laz"  # Add support for LAZ files
    filter_glob: StringProperty(default="*.las;*.laz", options={'HIDDEN'})  # Update the filter_glob to include LAZ files

    def execute(self, context):
        # Read LAS/LAZ file
        with laspy.open(self.filepath) as infile:
            # Get LAS points
            num_points_to_read = infile.header.point_count
            all_points = infile.read_points(n=num_points_to_read)
            points = np.array([(point['X'] * infile.header.x_scale + infile.header.x_offset,
                                point['Y'] * infile.header.y_scale + infile.header.y_offset,
                                point['Z'] * infile.header.z_scale + infile.header.z_offset)
                                for point in all_points])

            # Prepare LiDAR info
            lidar_info = {
                'filepath': self.filepath,
                'point_format': infile.header.point_format,
                'point_count': num_points_to_read,
                'header': infile.header
            }

        # Import LAS points as a mesh
        self.import_points_as_mesh(context, points, lidar_info)

        return {'FINISHED'}

    def import_points_as_mesh(self, context, points, lidar_info):
        # Create a new mesh object
        mesh = bpy.data.meshes.new("LAS Data")
        obj = bpy.data.objects.new("LAS Data", mesh)

        # Link the mesh to the scene
        context.collection.objects.link(obj)
    
        # Store LiDAR info in the object as separate custom properties
        obj['lidar_filepath'] = lidar_info['filepath']
        obj['lidar_point_format'] = lidar_info['point_format'].id
        obj['lidar_point_count'] = lidar_info['point_count']
        obj['lidar_version'] = get_attribute(lidar_info['header'], 'version')
        obj['lidar_min'] = get_attribute(lidar_info['header'], 'min')
        obj['lidar_max'] = get_attribute(lidar_info['header'], 'max')
        obj['lidar_scale'] = get_attribute(lidar_info['header'], 'scale')
        obj['lidar_offset'] = get_attribute(lidar_info['header'], 'offset')
        obj['lidar_creation_date'] = get_attribute(lidar_info['header'], 'creation_date')
        obj['lidar_gps_time_type'] = get_attribute(lidar_info['header'], 'gps_time_type')
        obj['lidar_point_count_by_return'] = get_attribute(lidar_info['header'], 'point_count_by_return')

        # Create mesh vertices from points
        mesh.from_pydata(points, [], [])

        # Set mesh object's origin to the center of its bounding box and location to (0, 0, 0)
        min_coords = [min(points, key=lambda coord: coord[i])[i] for i in range(3)]
        max_coords = [max(points, key=lambda coord: coord[i])[i] for i in range(3)]
        center = Vector([(min_coords[i] + max_coords[i]) / 2 for i in range(3)])
        
        for vertex in mesh.vertices:
            vertex.co -= center

        obj.location = Vector((0, 0, 0))

        # Update mesh
        mesh.update()

class LIDAR_PT_InfoPanel(bpy.types.Panel):
    bl_label = "LiDAR Info"
    bl_idname = "LIDAR_PT_InfoPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LiDAR'

    def draw(self, context):
        layout = self.layout

        # Retrieve custom properties from the object
        obj = context.active_object
        if obj and obj.get('lidar_filepath') and obj.get('lidar_point_format') and obj.get('lidar_point_count'):

            # Display additional attributes with default values if not found
            layout.label(text=f"Point Format: {obj.get('lidar_point_format', 'N/A')}")
            layout.label(text=f"LAS Version: {obj.get('lidar_version', 'N/A')}")
            layout.label(text=f"Min Coordinates: {obj.get('lidar_min', 'N/A')}")
            layout.label(text=f"Max Coordinates: {obj.get('lidar_max', 'N/A')}")
            layout.label(text=f"Scale Factors: {obj.get('lidar_scale', 'N/A')}")
            layout.label(text=f"Offsets: {obj.get('lidar_offset', 'N/A')}")
            layout.label(text=f"Creation Date: {obj.get('lidar_creation_date', 'N/A')}")
            layout.label(text=f"GPS Time Type: {obj.get('lidar_gps_time_type', 'N/A')}")
            layout.label(text=f"Point Count by Return: {obj.get('lidar_point_count_by_return', 'N/A')}")
        else:
            layout.label(text="No LiDAR data available")

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_las_data.bl_idname, text="LAS/LAZ data (.las, .laz)")

def register():
    bpy.utils.register_class(IMPORT_OT_las_data)
    bpy.utils.register_class(LIDAR_PT_InfoPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_las_data)
    bpy.utils.unregister_class(LIDAR_PT_InfoPanel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()