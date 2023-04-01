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

        # Import LAS points as a mesh
        self.import_points_as_mesh(context, points)

        return {'FINISHED'}

    def import_points_as_mesh(self, context, points):
        # Create a new mesh object
        mesh = bpy.data.meshes.new("LAS Data")
        obj = bpy.data.objects.new("LAS Data", mesh)

        # Link the mesh to the scene
        context.collection.objects.link(obj)

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

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_las_data.bl_idname, text="LAS/LAZ data (.las, .laz)")

def register():
    bpy.utils.register_class(IMPORT_OT_las_data)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_las_data)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()